def equals(expected_text: str):
    """
    Check if the event text or caption is equal to the expected text.
    
    Args:
        expected_text (str): The expected text to compare with.

    Returns:
        Callable: A function that checks if the event text or caption is equal to the expected text.
    """
    def check(event):
        try:
            return getattr(event, "text", None) == expected_text or getattr(event, "caption", None) == expected_text
        except:
            return False
    return check

