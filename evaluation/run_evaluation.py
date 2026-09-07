from __future__ import annotations

import json
from pathlib import Path

from whitson_knowledge_assistant.answer import answer_question


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_FILE = ROOT / "evaluation" / "questions.json"


def main() -> None:
    questions = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))

    passed = 0

    for item in questions:
        question = item["question"]
        should_answer = item["should_answer"]

        print("=" * 80)
        print(f"Question: {question}")

        try:
            answer = answer_question(question)
            answered = "I could not find relevant information" not in answer
            answered = answered and "I don't know based on the indexed sources." not in answer

            if answered == should_answer:
                result = "PASS"
                passed += 1
            else:
                result = "FAIL"

            print(f"Result: {result}")
            print(answer[:600])

        except Exception as error:
            print("Result: ERROR")
            print(error)

    print("=" * 80)
    print(f"Passed: {passed}/{len(questions)}")


if __name__ == "__main__":
    main()
