import argparse

from copy import deepcopy

from concurrent.futures import ThreadPoolExecutor

from core.engine import SequenceEngine
from core.state import State
from core.continuation import Continuation

from runtime.pipeline import execute_phase
from runtime.logger import log

from specs.api_security_probe import AppSpec


parser = argparse.ArgumentParser()

parser.add_argument(
    "--targets",
    nargs="+",
    required=True
)

args = parser.parse_args()

engine = SequenceEngine()

workflow = AppSpec["workflow"]

continuation = Continuation(
    id="root",
    objective=AppSpec["intent"]
)

engine.activate(continuation)

log("app_spec:", AppSpec)


def scan_target(target):

    local_spec = deepcopy(AppSpec)

    local_spec["target"] = target

    runtime_memory = {}

    log("\nTARGET:", target)

    state = State(
        phase=workflow[0],
        complete=False
    )

    while not state.complete:

        if state.phase not in workflow:
            state.complete = True
            break

        decision = engine.decide(state)

        log("state:", state.phase)
        log("decision:", decision)

        result = execute_phase(
            state.phase,
            local_spec,
            runtime_memory
        )

        log("execution:", result)

        state = engine.advance(
            state,
            decision
        )

        log("memory:", state.memory)

    return {
        "target": target,
        "last_state": state.phase,
        "memory": state.memory,
        "runtime_memory": runtime_memory
    }


with ThreadPoolExecutor(max_workers=5) as executor:

    results = list(
        executor.map(
            scan_target,
            args.targets
        )
    )

log("\nSCAN SUMMARY")

for result in results:
    log(result)

log("DONE")