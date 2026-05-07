"""
Analyze route — handles syllabus uploads, parsing, ranking, and MongoDB persistence.
"""
import os
import logging
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from bson import ObjectId
from services.parser import extract_text, extract_topics, allowed_file
from services.ranker import rank_topics
from services.database import get_collection, is_connected
from utils.auth_middleware import token_required

logger = logging.getLogger(__name__)

analyze_bp = Blueprint("analyze", __name__)


@analyze_bp.route("/analyze", methods=["POST"])
@token_required
def analyze(current_user_id):
    """Upload a syllabus file, extract topics, rank them, and optionally save to MongoDB."""

    file = request.files.get("file")

    if not file or file.filename == "":
        return jsonify({"error": "No file uploaded"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only PDF and TXT are supported."}), 400

    try:
        # 1. Extract text from file
        text = extract_text(file)

        if not text or len(text.strip()) < 20:
            return jsonify({"error": "Could not extract meaningful text from the file."}), 422

        # 2. Extract topics from text
        raw_topics = extract_topics(text)

        if not raw_topics:
            return jsonify({"error": "No topics found in the syllabus."}), 422

        # 3. Rank topics
        result = rank_topics(raw_topics)

        # 4. Save to MongoDB (if connected)
        analysis_id = None
        if is_connected():
            collection = get_collection("analyses")
            if collection is not None:
                doc = {
                    "user_id": current_user_id,
                    "filename": file.filename,
                    "topics": result["topics"],
                    "summary": result["summary"],
                    "raw_text_length": len(text),
                    "created_at": datetime.now(timezone.utc)
                }
                insert_result = collection.insert_one(doc)
                analysis_id = str(insert_result.inserted_id)
                logger.info(f"Analysis saved to MongoDB with ID: {analysis_id}")

        # 5. Return result
        response = {
            "topics": result["topics"],
            "summary": result["summary"]
        }
        if analysis_id:
            response["analysis_id"] = analysis_id

        return jsonify(response), 200

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        return jsonify({"error": "Analysis failed. Please try again."}), 500


@analyze_bp.route("/analysis/<analysis_id>/topic/<int:topic_id>", methods=["PATCH"])
@token_required
def update_topic_status(current_user_id, analysis_id, topic_id):
    """Update the status of a specific topic within a saved analysis."""

    if not is_connected():
        return jsonify({"error": "Database not available"}), 503

    data = request.get_json()
    if not data or "status" not in data:
        return jsonify({"error": "Missing 'status' field"}), 400

    new_status = data["status"]
    if new_status not in ("pending", "completed"):
        return jsonify({"error": "Status must be 'pending' or 'completed'"}), 400

    try:
        collection = get_collection("analyses")
        # Ensure the user only updates their own analysis
        result = collection.update_one(
            {"_id": ObjectId(analysis_id), "user_id": current_user_id, "topics.id": topic_id},
            {"$set": {"topics.$.status": new_status}}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Analysis or topic not found"}), 404

        return jsonify({"message": "Status updated", "topic_id": topic_id, "status": new_status}), 200

    except Exception as e:
        logger.error(f"Failed to update topic status: {e}")
        return jsonify({"error": "Failed to update status"}), 500