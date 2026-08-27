"""Quiz creation fixture used by CodeWiki Core tests."""


class QuizService:
    def create_quiz(self, title: str, questions: list[str]) -> dict[str, object]:
        if not title or not questions:
            raise ValueError("quiz validation failed")
        return {"title": title, "questions": questions}
