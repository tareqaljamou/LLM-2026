from whitson_knowledge_assistant.answer import answer_question


def main() -> None:
    print("Whitson Knowledge Assistant")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nQuestion: ").strip()

        if question.lower() == "exit":
            print("Goodbye.")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            answer = answer_question(question)
            print("\n" + answer)
        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()
