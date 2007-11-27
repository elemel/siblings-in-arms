class TaskState:
    pass

TaskState.CREATED = TaskState()
TaskState.STARTED = TaskState()
TaskState.COMPLETED = TaskState()
TaskState.ABORTED = TaskState()

class TaskStateError(Exception):
    def __init__(self, state = None, message = None):
        self.state = state
        self.message = message

class Task:
    def __init__(self):
        self._state = TaskState.CREATED
        self._progress = 0

    def start(self):
        if self._state != TaskState.CREATED:
            raise TaskStateError(self._state, "cannot start task")
        self._state = TaskState.STARTED
        self._start()

    def update(self):
        if self._state != TaskState.STARTED:
            raise TaskStateError(self._state, "cannot update task")
        self._update()

    def abort(self, facade):
        if self._state == TaskState.CREATED:
            self._state = TaskState.ABORTED
        elif self._state == TaskState.STARTED:
            self._state = TaskState.ABORTED
            self._abort()
        else:
            raise TaskStateError(self._state, "cannot abort task")

    def state(self):
        return self._state

    def progress(self):
        return self._progress

    def _start(self):
        pass

    def _update(self):
        pass
    
    def _abort(self):
        pass
