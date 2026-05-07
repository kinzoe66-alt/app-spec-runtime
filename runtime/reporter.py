import json

from uuid import uuid4

from datetime import datetime


def generate_report(
    result: dict,
    app_spec: dict
):

    findings = result.get(
        "findings",
        []
    )

    report = {

        "target": app_spec["target"],

        "summary": {
            "issues_detected": len(findings),
            "valid": result.get("valid")
        },

        "rules": app_spec[
            "analysis_rules"
        ],

        "findings": findings,

        "timestamp": (
            datetime.utcnow()
            .isoformat()
        )
    }

    filename = (
        f"reports/"
        f"report_{uuid4().hex}.json"
    )

    with open(filename, "w") as file:

        json.dump(
            report,
            file,
            indent=2
        )

    return {
        "report_file": filename,
        "report": report
    }