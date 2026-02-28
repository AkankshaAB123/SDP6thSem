import json

def validate_output(output_text):
    try:
        data = json.loads(output_text)

        required_fields = [
            "overall_risk_score",
            "risk_breakdown",
            "risk_level",
            "flagged_clauses"
        ]

        for field in required_fields:
            if field not in data:
                return False, "Missing field"

        return True, data

    except Exception as e:
        return False, str(e)