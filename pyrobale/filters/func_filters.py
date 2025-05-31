def equals(expected_text: str):
    def check(event):
        return getattr(event, "text", None) == expected_text or getattr(event, "caption", None) == expected_text
    return check