MODEL = "claude-opus-5-5"
SYSTEM = "Esti un asistent prietenos si concis. Raspunzi in limba in care ti se scrie."


class Chat:
    def __init__(self, client, system=SYSTEM, model=MODEL):
        self.client = client
        self.system = system
        self.model = model
        self.messages = []

    def ask(self, text, on_text=print):
        self.messages.append({"role": "user", "content": text})
        try:
            with self.client.beta.messages.stream(
                model=self.model,
                max_tokens=64000,
                system=self.system,
                messages=self.messages,
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            ) as stream:
                for chunk in stream.text_stream:
                    on_text(chunk)
                reply = stream.get_final_message()
        except Exception:
            self.messages.pop()
            raise
        if reply.stop_reason == "refusal":
            self.messages.pop()
        else:
            self.messages.append({"role": "assistant", "content": reply.content})
        return reply

    def reset(self):
        self.messages.clear()
