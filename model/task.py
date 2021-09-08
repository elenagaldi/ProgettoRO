class Task:
    def __init__(self, t_id, duration,
                 processed=False):  # settare un task a False significa che quel determinato task non è ancora stato
        # usato nel batch
        self.id = t_id
        self.duration = duration
        self.processed = processed

    def set_processed(self, new_state):
        self.processed = new_state

    def is_processed(self):
        return self.processed

    def __repr__(self):
        return f'"ID:{self.id} Duration:{self.duration}"\n'

    def __str__(self):
        return self.__repr__()

    def __key(self):
        return self.id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.__key() == other.__key()
        return NotImplemented
