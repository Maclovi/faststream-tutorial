# Тестирование приложения 🧪

Вы создали приложение FastStream, которое обрабатывает структурированные JSON-сообщения с помощью Pydantic! 🎉 Теперь пора убедиться, что оно работает правильно. В этом разделе мы научимся тестировать приложение с помощью `TestBroker`, который эмулирует RabbitMQ в памяти, без необходимости запускать реальный брокер. Мы также используем моки для проверки вызовов обработчиков. Это быстро, удобно и идеально для новичков! 😊 Готовы проверить ваш код? Погнали! 🚀

## Зачем тестировать FastStream? 🤔

Тестирование позволяет убедиться, что ваше приложение обрабатывает сообщения как ожидалось. С FastStream тестирование особенно удобно, потому что:

- **Эмуляция брокера** 🔄: `TestBroker` имитирует RabbitMQ, не требуя реального подключения, что ускоряет тесты.
- **Проверка валидации** ✅: Мы можем убедиться, что Pydantic правильно обрабатывает корректные и некорректные сообщения.
- **Мокирование** 🤖: Использование моков позволяет проверить, как вызываются обработчики, без сложной логики.

Мы напишем тесты для приложения из предыдущего раздела, которое обрабатывает сообщения с полями `username` и `message`.

## Шаг 1: Установка pytest 📦

Для тестирования будем использовать **pytest** и **pytest-asyncio**. Установите их в вашу виртуальную среду (если ещё не установлено):

```bash
pip install pytest pytest-asyncio
```

Проверьте установку:

```bash
pytest --version
```

Вы должны увидеть версию, например, `pytest 8.x.x`. Теперь мы готовы писать тесты! 💻

## Шаг 2: Создание тестов ✍️

Создайте файл `test_app.py` в папке `faststream-tutorial` и добавьте следующий код:

```python
{!./tests/test_app.py!}
import pytest
from unittest.mock import AsyncMock, patch
from pydantic import BaseModel, ValidationError
from faststream.rabbit import RabbitBroker, TestBroker

# Определяем модель для тестов (копия из app.py)
class UserMessage(BaseModel):
    username: str
    message: str

@pytest.mark.asyncio
async def test_correct_message():
    # Создаем брокер
    broker = RabbitBroker()

    # Мокируем обработчики
    handle_message = AsyncMock()
    check_result = AsyncMock()

    @broker.subscriber("input-queue")
    async def handle_message_mock(data: UserMessage):
        await handle_message(data)
        await broker.publish(
            UserMessage(username=data.username, message=data.message.upper()),
            queue="output-queue"
        )

    @broker.subscriber("output-queue")
    async def check_result_mock(data: UserMessage):
        await check_result(data)

    # Тестируем с эмуляцией брокера
    async with TestBroker(broker):
        # Отправляем корректное сообщение
        await broker.publish(
            UserMessage(username="Alice", message="Hello"),
            queue="input-queue"
        )

        # Проверяем вызов handle_message
        handle_message.assert_called_once_with(UserMessage(username="Alice", message="Hello"))
        # Проверяем вызов check_result
        check_result.assert_called_once_with(UserMessage(username="Alice", message="HELLO"))

@pytest.mark.asyncio
async def test_invalid_message():
    broker = RabbitBroker()

    @broker.subscriber("input-queue")
    async def handle_message(data: UserMessage):
        pass

    # Тестируем с эмуляцией брокера
    async with TestBroker(broker):
        # Отправляем некорректное сообщение
        with pytest.raises(ValidationError):
            await broker.publish(
                {"username": "Alice", "wrong_field": "Hello"},
                queue="input-queue"
            )
```

**Что здесь происходит?** 🔍

- **`TestBroker`** 🔄: Эмулирует RabbitMQ в памяти, не подключаясь к реальному брокеру. Контекстный менеджер (`async with`) вызывает `broker.connect()` и `broker.close()`, что подходит для тестирования без реальных подписчиков.
- **`AsyncMock`** 🤖: Используется для мокирования обработчиков `handle_message` и `check_result`, чтобы проверить, какие данные они получают.
- **`test_correct_message`** ✅: Отправляет корректное сообщение, проверяет, что `handle_message` вызван с входным `UserMessage`, и подтверждает, что `check_result` получил обработанный результат с `message` в верхнем регистре.
- **`test_invalid_message`** 🚫: Отправляет некорректное сообщение (с `wrong_field`) и проверяет, что Pydantic выбросил ошибку валидации.
- **`pytest.mark.asyncio`** ⚡: Позволяет использовать `async/await` в тестах.

**Напоминание** 📝: Контекстный менеджер в `TestBroker` вызывает только `broker.connect()` и `broker.close()`, что идеально для тестирования. Для реального приложения с подписчиками используется `broker.start()` (как в `faststream run app:app`).

## Шаг 3: Запуск тестов ▶️

Убедитесь, что файлы `app.py` и `test_app.py` находятся в папке `faststream-tutorial`. Запустите тесты:

```bash
pytest test_app.py -v
```

Вы увидите вывод, например:

```
============================= test session starts ==============================
test_app.py::test_correct_message PASSED                                 [ 50%]
test_app.py::test_invalid_message PASSED                                [100%]
=========================== 2 passed in 0.XXs ==============================
```

Оба теста прошли успешно! 🎉 Это подтверждает, что:
- Корректное сообщение обрабатывается, и результат передается в `output-queue` с измененным `message`.
- Некорректное сообщение вызывает ошибку валидации Pydantic.

## Шаг 4: Разбираемся с `TestBroker` и мокированием 🛠️

`TestBroker` и мокирование делают тестирование мощным и гибким:

- **Эмуляция очередей** 🗄️: `TestBroker` обрабатывает сообщения в памяти, не требуя реального RabbitMQ.
- **Мокирование обработчиков** 🔎: `AsyncMock` позволяет проверить, какие данные передаются в обработчики, без выполнения их логики.
- **Поддержка валидации** 🛡️: Pydantic работает так же, как в реальном приложении, обеспечивая проверку данных.

Этот подход, вдохновленный [примерами FastStream](https://github.com/airtai/faststream/tree/main/examples), позволяет тестировать сложные сценарии с минимальным кодом.

## Шаг 5: Практическое задание 📚

Закрепите знания с помощью заданий:

1. Добавьте тест, который проверяет, что `message` в `output-queue` всегда в верхнем регистре (например, `HELLO` для входного `Hello`).
2. Создайте тест для проверки обработки сообщения с пустой строкой в поле `message`, если вы добавили `min_length=1` в модель `UserMessage`.
3. (Дополнительно) Напишите тест, который использует `AsyncMock` для проверки, что `handle_message` вызывается только один раз для одного сообщения.

## Что дальше? 🗺️

Вы научились тестировать FastStream-приложения с использованием `TestBroker` и мокирования! 🎉 Это важный навык для создания надежных микросервисов. В следующем разделе мы узнаем, как генерировать красивую документацию в формате **AsyncAPI**, чтобы делиться спецификацией вашего приложения. Перейдите к [**Генерация документации**](./documentation.md), чтобы освоить этот процесс.

Если у вас есть идеи, вопросы или нужна помощь, загляните в [официальную документацию FastStream](https://faststream.airt.ai/latest/), пишите в [Telegram](https://t.me/python_faststream) или [Discord](https://discord.gg/qFm6aSqq59). Продолжайте тестировать и кодить! 🚀
