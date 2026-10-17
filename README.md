# Chatbot cu Claude

Chatbot în linie de comandă care folosește un model de limbaj mare (Claude Opus 5.5) prin API-ul Anthropic.

## Funcționalități

- conversație cu memorie: tot istoricul este trimis la fiecare mesaj, pentru că API-ul nu păstrează starea
- răspunsurile apar pe măsură ce sunt generate (streaming)
- `/nou` începe o conversație nouă, `/iesire` închide programul
- mesaje clare pentru cheie API invalidă, limită de cereri și probleme de rețea
- dacă o cerere eșuează sau modelul refuză să răspundă, mesajul este scos din istoric, ca conversația să rămână validă
- fallback pe server (`fallbacks="default"`): dacă modelul refuză o cerere, API-ul o reia automat cu un model potrivit

## Structură

| Fișier | Rol |
|---|---|
| `chat.py` | clasa `Chat`: istoricul și apelul către API |
| `main.py` | interfața din terminal și tratarea erorilor |
| `test_chat.py` | teste cu un client fals, fără apeluri reale și fără costuri |

## Rulare

Necesită Python 3.10 sau mai nou și o cheie API de la [platform.claude.com](https://platform.claude.com).

```
pip install -r requirements.txt
```

Setarea cheii:

```
export ANTHROPIC_API_KEY=cheia-ta          # Linux / macOS
setx ANTHROPIC_API_KEY cheia-ta            # Windows (se aplică în terminalele deschise după)
```

```
python main.py
python -m unittest
```

Testele nu au nevoie de cheie API și nici de pachetul `anthropic`.
