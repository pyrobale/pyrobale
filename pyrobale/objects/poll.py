from typing import TYPE_CHECKING, Optional, List, Union
from .polloption import PollOption


class Poll:
    def __init__(
        self,
        id: int,
        question: str,
        options: Union[List[PollOption], List],
        total_voter_count: int,
        is_closed: bool,
        is_anonymous: bool,
        type: str,
        allows_multiple_answers: bool,
        allows_revoting: bool,
        members_only: bool,
        **kwargs
    ):
        self.id = id
        self.question = question
        if isinstance(options, list):
            self.options = [PollOption(**option) for option in options]
        self.total_voter_count = total_voter_count
        self.is_closed = is_closed
        self.is_anonymous = is_anonymous
        self.type = type
        self.allows_multiple_answers = allows_multiple_answers
        self.allows_revoting = allows_revoting
        self.members_only = members_only
