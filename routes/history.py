"""
History route — retrieve and manage past analyses from MongoDB.
"""
import logging
from flask import Blueprint, jsonify
from bson import ObjectId
from services.database import get_collection, is_connected

logger = logging.getLogger(__name__)

history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
def get_history():
    """Retrieve all past analyses, sorted by most recent."""

    if not is_connected():
        return jsonify({"error": "Database not available", "history": []}), 503

    try:
        collection = get_collection("analyses")
        analyses = list(
            collection.find(
                {},
                {"raw_text_length": 0}  # Exclude raw text length from listing
            )
            .sort("created_at", -1)
            .limit(50)
        )

        # Convert ObjectId to string for JSON serialization
        for a in analyses:
            a["_id"] = str(a["_id"])
            if "created_at" in a:
                a["created_at"] = a["created_at"].isoformat()

        return jsonify({"history": analyses}), 200

    except Exception as e:
        logger.error(f"Failed to fetch history: {e}")
        return jsonify({"error": "Failed to fetch history", "history": []}), 500


@history_bp.route("/history/<analysis_id>", methods=["GET"])
def get_analysis(analysis_id):
    """Retrieve a single analysis by ID."""

    if not is_connected():
        return jsonify({"error": "Database not available"}), 503

    try:
        collection = get_collection("analyses")
        analysis = collection.find_one({"_id": ObjectId(analysis_id)})

        if not analysis:
            return jsonify({"error": "Analysis not found"}), 404

        analysis["_id"] = str(analysis["_id"])
        if "created_at" in analysis:
            analysis["created_at"] = analysis["created_at"].isoformat()

        return jsonify(analysis), 200

    except Exception as e:
        logger.error(f"Failed to fetch analysis: {e}")
        return jsonify({"error": "Failed to fetch analysis"}), 500


@history_bp.route("/history/<analysis_id>", methods=["DELETE"])
def delete_analysis(analysis_id):
    """Delete a single analysis."""

    if not is_connected():
        return jsonify({"error": "Database not available"}), 503

    try:
        collection = get_collection("analyses")
        result = collection.delete_one({"_id": ObjectId(analysis_id)})

        if result.deleted_count == 0:
            return jsonify({"error": "Analysis not found"}), 404

        logger.info(f"Deleted analysis: {analysis_id}")
        return jsonify({"message": "Analysis deleted"}), 200

    except Exception as e:
        logger.error(f"Failed to delete analysis: {e}")
        return jsonify({"error": "Failed to delete analysis"}), 500
