from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..objects import User
    from ..client import Client


class StateMachine:
    def __init__(self):
        self.__states = {}

    def set_state(self, user_id: Union[str, int], state: str):
        """Sets or updates state of a user

        Args:
            user_id (string OR integer): unique id of user for setting the state
            state (string): state of user (it can be anything)
        """
        self.__states[user_id] = state

    def get_state(self, user_id: Union[str, int]) -> str:
        """Gets state of a specified user

        Args:
            user_id (string OR integer): unique id of user for getting the state

        Returns:
            Str: the state of user
        """

        if user_id in self.__states:
            return self.__states[user_id]
        else:
            raise KeyError

    def del_state(self, user_id: Union[str, int]):
        """Deletes the saved state of user

        Args:
            user_id (string OR integer): unique if of user to delete its state
        """
        if user_id in self.__states:
            del self.__states[user_id]
        else:
            raise KeyError
    
    def save_local(self, file_name: str):
        """Saves the state of all users to a file

        Args:
            file_name (string): name of file to save the state of users
        """
        with open(file_name, "w") as f:
            for user_id, state in self.__states.items():
                f.write(f"{user_id} {state}\n")
    
    def load_local(self, file_name: str):
        """Loads the state of all users from a file

        Args:
            file_name (string): name of file to load the state of users
        """
        with open(file_name, "r") as f:
            for line in f:
                user_id, state = line.split()
                self.__states[user_id] = state