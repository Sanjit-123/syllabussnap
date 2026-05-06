"""
Topic ranking engine.
Produces output in the exact format the frontend expects.
"""
import re
import logging

logger = logging.getLogger(__name__)


# --- Scoring Functions ---

def keyword_weight(topic: str) -> float:
    """Score a topic based on academic keyword importance."""
    keywords = {
        "introduction": 5, "basics": 4, "advanced": 5,
        "important": 5, "concept": 3, "applications": 4,
        "case study": 5, "theory": 3, "analysis": 4,
        "design": 4, "architecture": 5, "implementation": 4,
        "algorithm": 5, "data structure": 5, "optimization": 4,
        "security": 4, "network": 3, "database": 4,
        "programming": 3, "system": 3, "model": 4,
        "protocol": 3, "framework": 4, "pattern": 3,
    }
    score = 0
    lower = topic.lower()
    for word, weight in keywords.items():
        if word in lower:
            score += weight
    return min(score, 10)  # Cap at 10


def detect_unit(topic: str) -> int:
    """Detect which unit/module/chapter a topic belongs to."""
    lower = topic.lower()
    match = re.search(r"(?:unit|module|chapter)\s*(\d+)", lower)
    if match:
        return int(match.group(1))
    return 1  # Default to unit 1


def unit_weight(unit_num: int) -> float:
    """Earlier units typically carry more weight."""
    weights = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
    return weights.get(unit_num, 2)


def length_score(topic: str) -> float:
    """Longer, more descriptive topics tend to be more important."""
    return min(len(topic.split()) / 5, 5)


def frequency_score(topic: str, all_topics: list) -> int:
    """Count how many times keywords from this topic appear across all topics."""
    words = set(topic.lower().split())
    # Remove common stop words
    stop_words = {"the", "a", "an", "in", "of", "to", "and", "for", "is", "on", "with", "by", "at", "from"}
    words -= stop_words

    if not words:
        return 1

    count = 0
    for other in all_topics:
        other_lower = other.lower()
        for w in words:
            if len(w) > 3 and w in other_lower:
                count += 1
                break

    return max(1, count)


def calculate_priority(topic: str, unit: int, freq: int) -> float:
    """
    Calculate a numeric priority score (0-10 scale).
    Formula: (keyword * 0.35) + (unit_weight * 0.25) + (length * 0.2) + (frequency * 0.2)
    """
    kw = keyword_weight(topic)
    uw = unit_weight(unit)
    ls = length_score(topic)
    fs = min(freq, 10)

    score = (kw * 0.35) + (uw * 0.25) + (ls * 0.20) + (fs * 0.20)
    return round(score, 2)


# --- Main Ranking Function ---

def rank_topics(raw_topics: list) -> dict:
    """
    Rank topics and return data in the EXACT format the frontend expects.

    Returns:
    {
        "topics": [
            {
                "id": 1,
                "title": "...",
                "unit": 1,
                "frequency": 3,
                "priority": 7.5,
                "difficulty": 5,
                "status": "pending",
                "confidence": 0
            }
        ],
        "summary": {
            "total_topics": 20,
            "high_priority": 5,
            "estimated_study_time": "40 hours"
        }
    }
    """
    ranked = []

    for i, topic in enumerate(raw_topics):
        unit = detect_unit(topic)
        freq = frequency_score(topic, raw_topics)
        priority = calculate_priority(topic, unit, freq)

        ranked.append({
            "id": i + 1,
            "title": topic,
            "unit": unit,
            "frequency": freq,
            "priority": priority,
            "difficulty": 5,  # Default — could be enhanced later
            "status": "pending",
            "confidence": 0
        })

    # Sort by priority descending
    ranked.sort(key=lambda x: x["priority"], reverse=True)

    # Re-assign IDs after sorting (so #1 = highest priority)
    for i, item in enumerate(ranked):
        item["id"] = i + 1

    # Limit to top 25 topics
    ranked = ranked[:25]

    # Build summary
    high_priority = len([t for t in ranked if t["priority"] > 6])
    total = len(ranked)
    est_hours = total * 2  # ~2 hours per topic

    summary = {
        "total_topics": total,
        "high_priority": high_priority,
        "estimated_study_time": f"{est_hours} hours"
    }

    logger.info(f"Ranked {total} topics — {high_priority} high priority")

    return {
        "topics": ranked,
        "summary": summary
    }