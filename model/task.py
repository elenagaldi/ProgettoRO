class Task:
    def __init__(self, t_id, duration,
                 processed=False):  # settare un task a False significa che quel determinato task non è ancora stato usato nel batch
        self.t_id = t_id
        self.duration = duration
        self.processed = processed

    def set_processed(self, new_state):
        self.processed = new_state

    def is_processed(self):
        return self.processed

    def __repr__(self):
        return f'"Task ID:{self.t_id} Duration:{self.duration} State: {self.processed}"'

    def __str__(self):
        return self.__repr__()
