class PollOption:
    def __init__(
        self,
        persistent_id: str,
        text: str,
        voter_count: int,
        **kwargs
    ):
        self.persistent_id = persistent_id
        self.text = text
        self.voter_count = voter_count