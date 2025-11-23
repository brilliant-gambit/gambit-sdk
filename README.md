# Gambit Platform Integration SDK

[![PyPI version](https://badge.fury.io/py/gambit-sdk.svg?v=1)](https://badge.fury.io/py/gambit-sdk)
[![Python Version](https://img.shields.io/pypi/pyversions/gambit-sdk)](https://pypi.org/project/gambit-sdk/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

**Gambit SDK** — это официальный инструментарий для разработки **Адаптеров Платформ** для системы автоматизации Gambit. Этот SDK предоставляет все необходимые контракты, схемы данных и утилиты, чтобы вы могли интегрировать любую образовательную платформу с ядром Gambit.

## Философия

SDK спроектирован по принципу **"Адаптер как Плагин"**. Это означает, что вы, как разработчик, фокусируетесь исключительно на бизнес-логике взаимодействия с конкретной платформой (реверс-инжиниринг её API, парсинг данных). Всю сложную инфраструктурную работу (взаимодействие с RabbitMQ, управление состоянием, логирование) берет на себя хост-система Gambit (`AdapterRunner`), которая будет запускать ваш код.

Ваша задача — реализовать простой и понятный интерфейс (`BaseAdapter`), который работает как "драйвер" для целевой платформы.

## Установка

Для начала работы установите пакет с помощью pip:

```bash
pip install gambit-sdk
```

## Быстрый старт

Ниже приведен пример реализации адаптера. Обратите внимание на разделение данных на статические (`Details`) и динамические (`Attempt`).

```python
# my_platform_adapter.py

from datetime import datetime
from httpx import AsyncClient

from gambit_sdk import (
    BaseAdapter,
    ExerciseType,
    UnifiedAssignmentPreview,
    UnifiedAssignmentDetails,
    UnifiedAttempt,
    UnifiedExercise,
    UnifiedGrade,
    UnifiedSolution,
    UnifiedCredentials,
    UnifiedAuthSession,
    StringAnswer,
)

class MyPlatformAdapter(BaseAdapter):
    def __init__(self, session: AsyncClient) -> None:
        # SDK передает уже сконфигурированный HTTP-клиент
        super().__init__(session)
        self.base_url = "https://api.my-platform.com"

    async def login(self, credentials: UnifiedCredentials) -> UnifiedAuthSession:
        """
        Логинимся на платформе.
        Возвращаем сессию, которую сервис сохранит и будет применять к запросам.
        """
        response = await self.session.post(
            f"{self.base_url}/auth/login",
            json={"username": credentials.username, "password": credentials.password}
        )
        response.raise_for_status()
        
        # Возвращаем данные сессии (токены, куки)
        return UnifiedAuthSession(
            headers={"Authorization": f"Bearer {response.json()['token']}"},
            cookies=dict(response.cookies),
            refresh_data={"refresh_token": response.json()['refresh_token']}
        )

    async def refresh_session(self) -> UnifiedAuthSession:
        """Обновляем токен, используя данные из текущей сессии."""
        # self.session уже содержит старые куки/хедеры
        # Но refresh_token может лежать отдельно, его нужно достать из self.refresh_data
        pass

    async def get_assignment_previews(self) -> list[UnifiedAssignmentPreview]:
        """Получаем легкий список заданий."""
        response = await self.session.get(f"{self.base_url}/homeworks")
        response.raise_for_status()
        
        previews = []
        for hw_data in response.json()["data"]:
            preview = UnifiedAssignmentPreview(
                platform_assignment_id=str(hw_data["id"]),
                title=hw_data["title"],
                assigned_date=datetime.fromisoformat(hw_data["assigned_at"]).date(),
                deadline=datetime.fromisoformat(hw_data["deadline_at"]),
                # Сохраняем данные для получения деталей в "черный ящик"
                context_data={"details_url": hw_data["_links"]["details"]}
            )
            previews.append(preview)
        return previews

    async def get_assignment_details(
        self, 
        assignment: UnifiedAssignmentPreview
    ) -> tuple[UnifiedAssignmentDetails, UnifiedAttempt]:
        """
        Получаем полную информацию.
        ВАЖНО: Возвращаем кортеж (Статика, Контекст Попытки).
        """
        details_url = assignment.context_data["details_url"]
        response = await self.session.get(details_url)
        response.raise_for_status()
        data = response.json()

        # 1. Формируем статические детали задания (кэшируются)
        exercises = [
            UnifiedExercise(
                platform_exercise_id=str(ex["id"]),
                type=ExerciseType.INPUT_STRING,
                question=ex["question_text"],
                max_score=float(ex["points"]),
                structure=None 
            ) for ex in data["exercises"]
        ]
        
        details = UnifiedAssignmentDetails(
            platform_assignment_id=assignment.platform_assignment_id,
            title=assignment.title,
            assigned_date=assignment.assigned_date,
            deadline=assignment.deadline,
            description=data.get("description"),
            exercises=exercises
        )

        # 2. Формируем контекст попытки (НЕ кэшируется, содержит токены)
        attempt = UnifiedAttempt(
            platform_assignment_id=assignment.platform_assignment_id,
            platform_attempt_id=None,
            # Данные, нужные для POST запроса (отправки)
            submission_context={
                "submit_url": data["_links"]["submit"],
                "csrf_token": data["csrf_token"],
                "attempt_id": data["attempt_id"]
            },
            # Данные, нужные для GET запроса (проверки оценки)
            grade_context={
                "grade_url": data["_links"]["grade"]
            }
        )

        return details, attempt

    async def submit_solution(
        self, 
        attempt: UnifiedAttempt, 
        solution: UnifiedSolution
    ) -> UnifiedGrade | None:
        """
        Отправляем решение, используя данные из attempt.submission_context.
        """
        context = attempt.submission_context
        
        # Формируем пейлоад для платформы
        platform_payload = {
            "attempt_id": context["attempt_id"],
            "csrf": context["csrf_token"],
            "answers": {
                ans.platform_exercise_id: ans.answer.value
                for ans in solution.answers 
                if isinstance(ans.answer, StringAnswer)
            }
        }
        
        response = await self.session.post(context["submit_url"], json=platform_payload)
        response.raise_for_status()
        
        # Если платформа сразу вернула оценку
        if grade_data := response.json().get("grade"):
            return UnifiedGrade(
                platform_assignment_id=attempt.platform_assignment_id,
                score=float(grade_data["score"]),
                max_score=float(grade_data["max_score"]),
                is_passed=grade_data["is_passed"]
            )
        return None

    async def get_grade(self, attempt: UnifiedAttempt) -> UnifiedGrade | None:
        """
        Проверяем оценку, используя данные из attempt.grade_context.
        """
        grade_url = attempt.grade_context["grade_url"]
        response = await self.session.get(grade_url)
        
        if response.status_code == 404:
            return None # Оценка еще не готова
            
        data = response.json()
        return UnifiedGrade(
            platform_assignment_id=attempt.platform_assignment_id,
            score=float(data["score"]),
            max_score=float(data["max_score"]),
            is_passed=data["is_passed"]
        )
```

## Воркфлоу взаимодействия

Хост-система `AdapterRunner` взаимодействует с адаптером в строгом порядке:

1.  **`login`**: Аутентификация. Адаптер возвращает `UnifiedAuthSession`.
2.  **`load_session`**: Перед каждым действием сервис вызывает этот метод, чтобы применить сохраненные куки/хедеры к `self.session`.
3.  **`get_assignment_previews`**: Получение списка доступных заданий.
4.  **`get_assignment_details`**: Запрос деталей для конкретного задания.
    *   Возвращает **два** объекта: `Details` (текст задания) и `Attempt` (технические токены).
    *   `Details` сохраняются в кэш. `Attempt` используется для текущей сессии решения.
5.  **`submit_solution`**: Отправка решения. Принимает `Attempt` (для токенов) и `Solution` (ответы).
6.  **`get_grade`**: Проверка статуса. Принимает `Attempt`.

## Справочник по API

### `BaseAdapter`

Абстрактный класс, который необходимо реализовать.

- **`__init__(self, session: AsyncClient)`**: Принимает готовую сессию.
- **`load_session(self, auth_session: UnifiedAuthSession)`**: Применяет сессию. Реализован в базовом классе, но может быть переопределен.
- **`login(self, credentials: UnifiedCredentials) -> UnifiedAuthSession`**: Аутентификация.
- **`refresh_session(self) -> UnifiedAuthSession`**: Обновление токена.
- **`get_assignment_previews(self) -> list[UnifiedAssignmentPreview]`**: Получение списка.
- **`get_assignment_details(self, assignment) -> tuple[UnifiedAssignmentDetails, UnifiedAttempt]`**: Получение деталей и контекста попытки.
- **`submit_solution(self, attempt, solution) -> UnifiedGrade | None`**: Отправка решения.
- **`get_grade(self, attempt) -> UnifiedGrade | None`**: Получение оценки.

### `ExerciseType` (Enum)

Типы упражнений, поддерживаемые системой:
- `CHOICE_SINGLE`: Выбор одного варианта.
- `CHOICE_MULTIPLE`: Выбор нескольких вариантов.
- `INPUT_STRING`: Ввод короткой строки.
- `INPUT_TEXT`: Ввод длинного текста.
- `TEXT_FILE`: Загрузка файла.
- `MATCHING_PAIRS`: Сопоставление.
- `SEQUENCE_ORDERING`: Упорядочивание.
- `UNSUPPORTED`: Неподдерживаемый тип.

### Схемы данных (Pydantic)

- **`UnifiedAssignmentPreview`**:
  - `context_data` (`dict`): Данные для перехода к деталям (например, URL).
- **`UnifiedAssignmentDetails`**:
  - `exercises` (`list[UnifiedExercise]`): Список упражнений.
- **`UnifiedAttempt`**:
  - `submission_context` (`dict`): Данные для POST-запроса (csrf, form_id).
  - `grade_context` (`dict`): Данные для проверки оценки.
- **`UnifiedExercise`**:
  - `structure`: Строго типизированная структура (например, `ChoiceStructure` с вариантами ответов).
- **`UnifiedSolutionExercise`**:
  - `answer`: Строго типизированный ответ (например, `ChoiceAnswer` или `StringAnswer`). Валидируется на соответствие `ExerciseType`.

## Лицензия

Использование данного SDK регулируется **проприетарной лицензией**. Пожалуйста, ознакомьтесь с полным текстом в файле [LICENSE](LICENSE) перед использованием. Ключевое ограничение: SDK может быть использован **исключительно** для создания адаптеров для платформы Gambit.
