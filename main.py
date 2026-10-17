import anthropic

from chat import Chat

ERRORS = (
    (anthropic.AuthenticationError, "Cheie API invalida. Seteaza variabila ANTHROPIC_API_KEY."),
    (anthropic.RateLimitError, "Prea multe cereri. Incearca din nou peste putin timp."),
    (anthropic.APIConnectionError, "Nu ma pot conecta la API. Verifica internetul."),
    (anthropic.APIStatusError, "Eroare de la API."),
)


def main():
    chat = Chat(anthropic.Anthropic())
    print("Chat cu Claude. Comenzi: /nou (conversatie noua), /iesire\n")
    while True:
        try:
            text = input("Tu: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if text == "/iesire":
            break
        if text == "/nou":
            chat.reset()
            print("Conversatie noua.\n")
            continue
        if not text:
            continue

        print("Claude: ", end="", flush=True)
        try:
            reply = chat.ask(text, on_text=lambda chunk: print(chunk, end="", flush=True))
            if reply.stop_reason == "refusal":
                print("(Claude a refuzat sa raspunda la acest mesaj.)", end="")
        except anthropic.APIError as error:
            print(next((message for kind, message in ERRORS if isinstance(error, kind)), "Eroare neasteptata."), error, sep="\n")
        print("\n")


if __name__ == "__main__":
    main()
