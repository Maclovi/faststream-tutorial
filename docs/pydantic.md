# Структурированные сообщения с Pydantic ✅

В предыдущем разделе вы создали приложение, которое обрабатывает простые текстовые сообщения. Теперь пора сделать его мощнее! В этом разделе мы добавим **Pydantic** — библиотеку для структурирования и валидации данных. Это позволит обрабатывать JSON-сообщения с четкой структурой и автоматически проверять их корректность. Готовы улучшить ваше приложение? Погнали! 🚀

## Зачем нужен Pydantic? 🤔

Когда вы работаете с брокерами сообщений, данные часто приходят в формате JSON. Без проверки легко получить ошибки, если, например, в сообщении отсутствует нужное поле или поле имеет неверный тип. **Pydantic** решает эту проблему:

- **Структурирует данные** 📋: Вы определяете, как должны выглядеть сообщения (например, `{ "username": str, "message": str }`).
- **Валидирует автоматически** 🛡️: Если сообщение не соответствует структуре, FastStream выбросит ошибку.
- **Упрощает код** ✨: Вы работаете с типизированными объектами, а не с сырыми словарями.

В FastStream Pydantic интегрирован "из коробки", что делает работу с JSON-сообщениями удобной и безопасной. 😎

## Шаг 1: Обновление приложения ✍️

Давайте модифицируем наше приложение из `app.py`, чтобы оно обрабатывало JSON-сообщения с полями `username` и `message`. Откройте `app.py` и замените код на следующий:

```python
from pydantic import BaseModel, Field
from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker

# Определяем структуру сообщения
class UserMessage(BaseModel):
    username: str = Field(..., examples=["Alice"], description="Имя пользователя")
    message: str = Field(..., examples=["Hello"], description="Текст сообщения")

# Создаем брокер и приложение
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = FastStream(broker)

# Подписываемся на очередь и публикуем результат
@broker.subscriber("input-queue")
@broker.publisher("output-queue")
async def handle_message(data: UserMessage, logger: Logger) -> UserMessage:
    logger.info(f"Получено: {data.username} сказал '{data.message}'")
    return UserMessage(
        username=data.username,
        message=data.message.upper()
    )
```

**Что изменилось?** 🔍

- **Модель `UserMessage`** 📋: Мы создали класс Pydantic с двумя полями: `username` (строка) и `message` (строка). `Field(..., examples=["..."], description="...")` добавляет метаданные для документации.
- **Типизация в `handle_message`** ✅: Функция теперь принимает объект `UserMessage` вместо строки. FastStream автоматически проверяет, что входящее сообщение соответствует модели.
- **Возврат объекта** 📤: Мы возвращаем новый объект `UserMessage` с обработанным сообщением (в верхнем регистре).
- **Логирование** 📜: Лог теперь показывает имя пользователя и сообщение.

## Шаг 2: Обновление отправки сообщений 📬

Чтобы протестировать приложение, обновим скрипт отправки сообщений. Откройте `send_message.py` и замените код:

```python
from faststream.rabbit import RabbitBroker

async def send_message():
    async with RabbitBroker("amqp://guest:guest@localhost:5672/") as broker:
        await broker.publish(
            {"username": "Alice", "message": "Hello"},
            queue="input-queue"
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(send_message())
```

**Почему контекстный менеджер?** 🔌 Как мы узнали ранее, контекстный менеджер (`async with`) идеален для отправки сообщений, так как он вызывает только `broker.connect()` и `broker.close()`, а не `broker.start()`. Это подходит, потому что здесь нет подписчиков.

## Шаг 3: Запуск и тестирование ▶️

1. **Запустите RabbitMQ** (если ещё не запущен):

   ```bash
   docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```

2. **Запустите приложение**:

   ```bash
   faststream run app:app
   ```

   Вы увидите:

   ```
   INFO     - FastStream app starting...
   INFO     - input-queue |            - `handle_message` waiting for messages
   INFO     - FastStream app started successfully! To exit press CTRL+C
   ```

3. **Отправьте сообщение**:

   ```bash
   python send_message.py
   ```

   В терминале приложения появится:

   ```
   INFO     - input-queue |            - Получено: Alice сказал 'Hello'
   ```

   FastStream получил JSON, проверил его через Pydantic и отправил результат (`{"username": "Alice", "message": "HELLO"}`) в `output-queue`. Проверьте это в веб-интерфейсе RabbitMQ (`http://localhost:15672`, раздел **Queues**, очередь `output-queue`, функция **Get Messages**).

## Шаг 4: Проверка валидации 🛡️

Pydantic автоматически валидирует сообщения. Давайте протестируем, что происходит, если отправить неверный JSON. Измените `send_message.py`:

```python
from faststream.rabbit import RabbitBroker

async def send_message():
    async with RabbitBroker("amqp://guest:guest@localhost:5672/") as broker:
        await broker.publish(
            {"username": "Alice", "wrong_field": "Hello"},  # Неверное поле
            queue="input-queue"
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(send_message())
```

Запустите скрипт:

```bash
python send_message.py
```

В терминале приложения вы увидите ошибку валидации, например:

```
ERROR    - input-queue |            - Validation error: ...
```

Pydantic заметил, что поле `wrong_field` не соответствует модели `UserMessage`, и отклонил сообщение. Это защищает ваше приложение от некорректных данных! ✅

## Шаг 5: Практическое задание 📚

Закрепите знания с помощью заданий:

1. Добавьте в модель `UserMessage` новое поле, например, `timestamp: str`, и обновите `handle_message`, чтобы включать его в результат.
2. Измените `send_message.py`, чтобы отправлять сообщение с новым полем, и проверьте результат в `output-queue`.
3. (Дополнительно) Настройте `Field` в модели так, чтобы `message` не мог быть пустой строкой (используйте `min_length=1`).

## Что дальше? 🗺️

Вы научились использовать Pydantic для структурирования и валидации сообщений в FastStream! 🎉 Это делает ваше приложение более надежным и готовым к реальным задачам. В следующем разделе мы узнаем, как тестировать приложение без реального брокера. Перейдите к [**Тестирование приложения**](./testing.md), чтобы освоить инструменты тестирования FastStream.

Если что-то непонятно, задайте вопрос в [Telegram](https://t.me/python_faststream) или [Discord](https://discord.gg/qFm6aSqq59) сообществах FastStream. Продолжайте кодить! 🚀
