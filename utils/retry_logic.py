def is_transient_error(e: Exception) -> bool:
    """
    Determine if an exception is a transient error that should be retried.
    Transient errors are typically UI-related timing issues, not logic bugs.
    """
    msg = str(e).lower()
    transient_indicators = [
        "timeout",
        "stale element reference",
        "element not interactable",
        "element click intercepted",
        "element is not clickable",
        "no such element",
        "unable to locate element"
    ]
    return any(indicator in msg for indicator in transient_indicators)