from db.models.conversation import ConversationState

class ConversationStateMachine:
    # Определяем переходы: текущий_статус -> список допустимых следующих статусов
    transitions = {
        ConversationState.NEW: [ConversationState.QUALIFYING, ConversationState.CLOSED, ConversationState.LOST],
        ConversationState.QUALIFYING: [ConversationState.HOT, ConversationState.TRANSFERRED, ConversationState.LOST],
        ConversationState.HOT: [ConversationState.APPOINTMENT, ConversationState.TRANSFERRED, ConversationState.LOST],
        ConversationState.TRANSFERRED: [ConversationState.HUMAN_ACTIVE, ConversationState.CLOSED, ConversationState.LOST],
        ConversationState.HUMAN_ACTIVE: [ConversationState.APPOINTMENT, ConversationState.CLOSED, ConversationState.LOST],
        ConversationState.APPOINTMENT: [ConversationState.CLOSED, ConversationState.LOST],
        ConversationState.CLOSED: [],
        ConversationState.LOST: [],
    }

    def __init__(self, current_state: ConversationState):
        self.current_state = current_state

    def can_transition(self, new_state: ConversationState) -> bool:
        allowed_states = self.transitions.get(self.current_state, [])
        return new_state in allowed_states

    def transition(self, new_state: ConversationState) -> ConversationState:
        if self.can_transition(new_state):
            self.current_state = new_state
            return self.current_state
        else:
            raise ValueError(f"Invalid state transition from {self.current_state} to {new_state}")