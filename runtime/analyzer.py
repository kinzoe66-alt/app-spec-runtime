def analyze_response(response: dict):

    findings = []

    status = response.get("status_code")

    if status != 200:
        findings.append("unexpected_status")

    headers = response.get("headers", {})

    if "Server" in headers:
        findings.append("server_header_exposed")

    return {
        "valid": len(findings) == 0,
        "findings": findings
    }