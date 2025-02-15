import traceback


class BaseCallback:
    def __init__(self, data=None):
        self.data = data