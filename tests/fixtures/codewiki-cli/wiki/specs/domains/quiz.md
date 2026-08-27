# Quiz

## Intent

Create quizzes only from valid input and report invalid input clearly.

## Requirements

### `QUIZ-R001`

Quiz validation must run before quiz creation input is stored.

### `QUIZ-R002`

퀴즈 입력 검증은 제목과 질문이 비어 있는 요청을 거부해야 한다.

## Acceptance Criteria

### `QUIZ-AC001`

Invalid input must return a validation error before persistence.

### `QUIZ-AC002`

제목이 비어 있으면 퀴즈 입력 검증 오류가 반환된다.

## Required Context

## See Also
