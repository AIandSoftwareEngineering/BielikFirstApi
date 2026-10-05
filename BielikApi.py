import json
import urllib.request


def chat_with_bielik():
    url = "http://localhost:11434/api/chat"
    model_name = "SpeakLeash/bielik-minitron-7b-v3.0-instruct:Q4_K_M"

    # Maintain conversation history across turns
    messages = []

    print("--- Czat z Bielikiem (wpisz 'exit' lub 'q' aby zakończyć) ---")

    while True:
        try:
            user_input = input("\nTy: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "q", "quit"]:
                print("Do zobaczenia!")
                break

            # Append user message to memory
            messages.append({"role": "user", "content": user_input})

            payload = {
                "model": model_name,
                "messages": messages,
                "stream": False,
            }

            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url, data=data, headers={"Content-Type": "application/json"}
            )

            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                assistant_response = result["message"]["content"]

                print(f"\nBielik: {assistant_response}")

                # Save assistant response to memory
                messages.append(
                    {"role": "assistant", "content": assistant_response}
                )

        except urllib.error.URLError as e:
            print(
                f"\nBłąd połączenia z Ollama. Upewnij się, że usługa działa: {e}"
            )
            break
        except Exception as e:
            print(f"\nWystąpił błąd: {e}")


if __name__ == "__main__":
    chat_with_bielik()