import json
from datetime import datetime


def generate_report(result: dict):

    findings = result.get(
        "findings",
        []
    )

    report = {
        "summary": {
            "issues_detected": len(findings),
            "valid": result.get("valid")
        },
        "findings": findings,
        "timestamp": datetime.utcnow().isoformat()
    }

    filename = (
        f"reports/report_"
        f"{datetime.utcnow().timestamp()}.json"
    )

    with open(filename, "w") as file:
        json.dump(
            report,
            file,
            indent=2
        )

    return report