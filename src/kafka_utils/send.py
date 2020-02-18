from typing import Any, Callable


def get_topic_send(topic: str, send: Callable) -> Callable[[Any], None]:
    def _send(payload: Any) -> None:
        send(topic, payload)

    return _send
