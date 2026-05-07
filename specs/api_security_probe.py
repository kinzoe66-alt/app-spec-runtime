AppSpec = {
    "name": "api_security_probe",

    "intent": "analyze API behavior for inconsistencies",

    "target": "https://httpbin.org/get",

    "workflow": [
        "INTERPRET",
        "PROBE",
        "COMPARE",
        "EVALUATE",
        "COMPLETE"
    ],

    "tools": [
        "request_sender",
        "response_analyzer",
        "diff_engine"
    ],

    "constraints": {
        "deterministic": True,
        "trace": True
    }
}