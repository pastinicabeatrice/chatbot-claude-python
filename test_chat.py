import unittest
from types import SimpleNamespace

from chat import Chat


class FakeStream:
    def __init__(self, chunks, stop_reason, error=None):
        self.text_stream = iter(chunks)
        self.reply = SimpleNamespace(stop_reason=stop_reason, content=[{"type": "text", "text": "".join(chunks)}])
        self.error = error

    def __enter__(self):
        if self.error:
            raise self.error
        return self

    def __exit__(self, *exc):
        return False

    def get_final_message(self):
        return self.reply


class FakeClient:
    def __init__(self, *streams):
        self.streams = list(streams)
        self.requests = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(stream=self.stream))

    def stream(self, **request):
        self.requests.append({**request, "messages": list(request["messages"])})
        return self.streams.pop(0)


class ChatTest(unittest.TestCase):
    def test_streams_text_and_keeps_history(self):
        client = FakeClient(FakeStream(["Salut", "!"], "end_turn"), FakeStream(["Bine"], "end_turn"))
        chat = Chat(client)
        received = []

        chat.ask("Buna", on_text=received.append)
        chat.ask("Ce faci?", on_text=received.append)

        self.assertEqual(received, ["Salut", "!", "Bine"])
        self.assertEqual([m["role"] for m in chat.messages], ["user", "assistant", "user", "assistant"])
        self.assertEqual(len(client.requests[1]["messages"]), 3)

    def test_request_uses_model_and_fallbacks(self):
        client = FakeClient(FakeStream(["ok"], "end_turn"))
        Chat(client).ask("test", on_text=lambda _: None)
        request = client.requests[0]
        self.assertEqual(request["model"], "claude-opus-5-5")
        self.assertEqual(request["fallbacks"], "default")

    def test_refusal_is_not_added_to_history(self):
        chat = Chat(FakeClient(FakeStream([], "refusal")))
        chat.ask("ceva", on_text=lambda _: None)
        self.assertEqual(chat.messages, [])

    def test_error_removes_unanswered_message(self):
        chat = Chat(FakeClient(FakeStream([], "end_turn", error=ConnectionError())))
        with self.assertRaises(ConnectionError):
            chat.ask("ceva", on_text=lambda _: None)
        self.assertEqual(chat.messages, [])

    def test_reset(self):
        chat = Chat(FakeClient(FakeStream(["ok"], "end_turn")))
        chat.ask("test", on_text=lambda _: None)
        chat.reset()
        self.assertEqual(chat.messages, [])


if __name__ == "__main__":
    unittest.main()
