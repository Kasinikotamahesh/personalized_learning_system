def get_recommendation(score, subject):
    if score < 40:
        return f"You need improvement in {subject}. Recommended: Watch beginner tutorials and practice fundamentals."
    elif 40 <= score < 70:
        return f"Good progress in {subject}! Revise intermediate concepts and solve practice problems."
    else:
        return f"Excellent work in {subject}! Try advanced topics and build a mini project."
