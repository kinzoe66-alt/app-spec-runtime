from core.engine import SequenceEngine
from core.state import State
from core.continuation import Continuation

from runtime.pipeline import execute_phase

from specs.api_security_probe import AppSpec


engine = SequenceEngine()

workflow = AppSpec["workflow"]

state = State(
    phase=workflow[0],
    complete=False
)

continuation = Continuation(
    id="root",
    objective=AppSpec["intent"]
)

engine.activate(continuation)

print("app_spec:", AppSpec)

while not state.complete:

    if state.phase not in workflow:
        state.complete = True
        break

    decision = engine.decide(state)

    print("state:", state.phase)
    print("decision:", decision)

    result = execute_phase(
        state.phase,
        AppSpec
    )

    print("execution:", result)

    state = engine.advance(state, decision)

    print("memory:", state.memory)

print("DONE")