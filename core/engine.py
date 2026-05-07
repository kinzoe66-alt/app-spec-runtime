from core.continuation import Continuation
from core.state import State
from core.decision import Decision
from runtime.transitions import TRANSITIONS


class SequenceEngine:

    def __init__(self):
        self.active_continuation = None

    def activate(self, continuation: Continuation):
        self.active_continuation = continuation

    def current(self):
        return self.active_continuation

    def terminate(self):
        self.active_continuation = None

    def register_capability(self, state: State, capability):
        exists = any(c.name == capability.name for c in state.capabilities)
        if not exists:
            state.capabilities.append(capability)
        return state

    def advance(self, state: State, decision: Decision):

        state.memory["last_decision"] = decision.action
        state.memory["last_reason"] = decision.reason

        if decision.action == "TERMINATE":
            state.complete = True
            return state

        next_phase = TRANSITIONS.get(state.phase)

        if not next_phase:
            state.complete = True
            return state

        state.phase = next_phase
        return state

    def decide(self, state: State) -> Decision:

        if state.phase == "COMPLETE":
            return Decision(
                action="TERMINATE",
                reason="runtime_complete"
            )

        return Decision(
            action="ADVANCE",
            reason=f"phase_{state.phase.lower()}"
        )