from src.services.quiz import QuizService


def test_create_quiz() -> None:
    assert QuizService().create_quiz("Basics", ["Question"])["title"] == "Basics"
