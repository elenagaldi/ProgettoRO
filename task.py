import input

class Task:
    def __init__(self, duration, state=True):
        self.duration=duration
        self.state = state

    def set_state(self, new_state):
        self.state = new_state

    def get_state(self):
        return self.state

