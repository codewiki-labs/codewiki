# Quiz

## Feature Coverage

### Feature: `quiz-creation`

- Spec Basis: `QUIZ-R001`, `QUIZ-R002`.
- API or Event: `POST /api/quizzes` is handled in `src/services/quiz.py`.
- Service And Provider: `QuizService.create_quiz` in `src/services/quiz.py` validates input before returning the quiz.
- Failure And Recovery: invalid input raises a validation error without persistence.
- Exact Tests: `tests/test_quiz.py` covers successful creation and validation behavior.
