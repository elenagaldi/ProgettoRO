
class Task:
    def __init__(self, t_id, duration, state=False): # settare un task a False significa che quel determinato task non è ancora stato usato nel batch
        self.t_id = t_id
        self.duration = duration
        self.state = state

    def set_state(self, new_state):
        self.state = new_state

    def get_state(self):
        return self.state

