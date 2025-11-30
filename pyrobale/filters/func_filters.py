import re
def equals(expected_text: str):
    """
    Check if the event text or caption or callbackQuery data is equal to the expected text.
    
    Args:
        expected_text (str): The expected text to compare with.

    Returns:
        Callable: A function that checks if the event text or caption or callbackQuery data is equal to the expected text.
    """
    def check(event):
        try:
            return getattr(event, "text", None) == expected_text or getattr(event, "caption", None) == expected_text
        except:
            return False
    return check

def regex(pattern: str):
    """
    checks the event text or caption with given pattern using regex
    
    Args:
        pattern (str): The pattern to check with text
    
    Returns:
        Callable: A function that checks if the event text or caption is match with given pattern
    """
    def check(event):
        try:
            return re.search(pattern, getattr(event, "text", None)) or re.search(pattern, getattr(event, "caption", None))
        except:
            return False
    return check

def private():
    """
    checks if the event is happening in a private chat
    """

    def check(event):
        try:
            chat = getattr(event, "chat")
            return getattr(chat, "private")
        except:
            return False
    return check


def group():
    """
    checks if the event is happening in a group chat
    """

    def check(event):
        try:
            chat = getattr(event, "chat")
            return getattr(chat, "group")
        except:
            return False
    return check


def channel():
    """
    checks if the event is happening in a channel
    """

    def check(event):
        try:
            chat = getattr(event, "chat")
            return getattr(chat, "channel")
        except:
            return False
    return check

def admin():
    """
    Checks if the event sender is admin of chat or not
    """

    def check(event):
        try:
            return getattr(event, "is_admin")
        except:
            return False
    return check