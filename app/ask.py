import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str,chat) -> str:
    response = chat.send_message(question)

    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count if usage is not None else None
    output_tokens = usage.candidates_token_count if usage is not None else None
    print(
        f"[使用量] 入力: {input_tokens if input_tokens is not None else '不明'} tokens, "
        f"出力: {output_tokens if output_tokens is not None else '不明'} tokens"
    )

    return response.text or ""


def main() -> None:
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")

    question = args.question
    while True:
        try:
            question = input("次の質問（exitで終了）: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n終了します。")
            break
        if question.lower() == "exit":
            break
        while not question:
            question = input("質問を入力してください: ").strip()
            if question.lower() == "exit":
                return

if __name__ == "__main__":
    main()
