from django_stomp.services.consumer import Payload


def test_callback(payload: Payload) -> None:
    print(payload.body)
    payload.ack()
