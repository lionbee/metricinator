from typing import Any, Callable


def get_topic_send(
    topic: str, send: Callable[[str, Any], None]
) -> Callable[[Any], None]:
    """
    Create a sender function with a set topic

    - param: topic: topic to use in send function
    - param: send: orignial send function that takes topic as the first param
    """

    def _send(payload: Any) -> None:
        send(topic, payload)

    return _send
