from adapters.http_adapter import send_request
from runtime.analyzer import analyze_response
from runtime.reporter import generate_report


runtime_memory = {}


def execute_phase(
    phase: str,
    app_spec: dict
):

    handlers = {

        "INTERPRET": lambda: "interpreting input",

        "PROBE": lambda: runtime_memory.update({
            "response": send_request(
                app_spec["target"]
            )
        }) or runtime_memory["response"],

        "COMPARE": lambda: runtime_memory.update({
            "analysis": analyze_response(
                runtime_memory["response"]
            )
        }) or runtime_memory["analysis"],

        "EVALUATE": lambda: generate_report(
            runtime_memory["analysis"]
        ),

        "COMPLETE": lambda: "execution complete"
    }

    handler = handlers.get(
        phase,
        lambda: "unknown phase"
    )

    return handler()