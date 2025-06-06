# Структурированные сообщения с Pydantic ✅

В предыдущем разделе вы научились создавать сервисы, которые взаимодействуют через очереди RabbitMQ. Теперь пора сделать приложение мощнее! В этом разделе мы добавим **Pydantic** — фреймворк для структурирования и валидации данных. Это позволит обрабатывать JSON-сообщения с четкой структурой и автоматически проверять их корректность. Мы также настроим приложение для отправки данных в две очереди, чтобы взаимодействовать с другим сервисом. Готовы улучшить ваше приложение? Погнали! 🚀

## Зачем нужен Pydantic? 🤔

Когда вы работаете с брокерами сообщений, данные часто приходят в формате JSON. Без проверки легко получить ошибки, если, например, в сообщении отсутствует нужное поле или поле имеет неверный тип. **Pydantic** решает эту проблему:

- **Структурирует данные** 📋: Вы определяете, как должны выглядеть сообщения (например, `{ "username": str, "message": str }`).
- **Валидирует автоматически** 🛡️: Если сообщение не соответствует структуре, FastStream выбросит ошибку.
- **Упрощает код** ✨: Вы работаете с типизированными объектами, а не с сырыми словарями.

В FastStream Pydantic интегрирован "из коробки", что делает работу с JSON-сообщениями удобной и безопасной. 😎

## Шаг 1: Обновление приложения ✍️

Обновим приложение из `app.py`, чтобы оно обрабатывало JSON-сообщения с полями `username` и `message` и отправляло результаты в `output-queue` и `final-queue`. Откройте `app.py` и замените код:

```python linenums="1" title="app.py" hl_lines="7-9 18-19 23-24 29"
--8<-- "src/tutorial/pydantic/app.py"
```

**Что изменилось?** 🔍

- **Модель `UserMessage`**: Класс Pydantic с полями `username` и `message`. Метаданные (`Field`) добавим позже в разделе про AsyncAPI.
- **`@broker.subscriber`**: Декораторы, регистрирующие функции как подписчиков на очереди `input-queue` и `output-queue`.
- **`handle_message`**: Принимает объект `UserMessage`, логирует данные и отправляет новый `UserMessage` с `message` в верхнем регистре в `output-queue` и `final-queue`.
- **`broker.publish`**: Отправляет структурированное сообщение в обе очереди, чтобы первый сервис (`app.py`) мог обработать промежуточный результат, а второй (`app2.py`) — финальный.
- **`check_result`**: Валидирует структуру UserMessage на соответствие правильных полей и логирует результат из `output-queue`, показывая, как первый сервис потребляет промежуточные данные.

**Примечание** 🌐: Сообщения из `final-queue` обрабатываются вторым сервисом (`app2.py`), как описано в разделе про взаимодействие сервисов.

**Альтернативный способ отправки** 📤  
Вместо `broker.publish` можно использовать `@broker.publisher`:

```python
@broker.subscriber("input-queue")
@broker.publisher("output-queue")
@broker.publisher("final-queue")
async def handle_message(data: UserMessage, logger: Logger) -> UserMessage:
    logger.info(f"Получено: {data.username} сказал {data.message!r}")
    return UserMessage(username=data.username, message=data.message.upper())
```

Порядок декораторов важен: `@broker.subscriber` — внешний, `@broker.publisher` — внутренний, так как первый регистрирует подписчика, а второй обрабатывает возвращаемое значение. Несколько `@broker.publisher` позволяют отправлять данные в разные очереди.

## Шаг 2: Обновление отправки сообщений 📬

Чтобы протестировать приложение с Pydantic, обновите файл `send_message.py` в папке `faststream-tutorial`, чтобы он отправлял структурированное сообщение с использованием Pydantic:

```python linenums="1" title="send_message.py" hl_lines="7-9 14 18"
--8<-- "src/tutorial/pydantic/send_message.py"
```

**Что здесь происходит?** 🔍

- **`UserMessage`**: Pydantic-модель, соответствующая модели в `app.py`, для согласованности (в реальном проекте её можно вынести в общий модуль).
- **`broker.publish`**: Отправляет объект `UserMessage`, который FastStream автоматически сериализует в JSON `{ "username": "Alice", "message": "Hello" }`.
- **Контекстный менеджер**: Используется `async with` для одноразового подключения к RabbitMQ и отправки сообщения.

## Шаг 3: Запуск и публикация сообщений ▶️

1. **Запустите RabbitMQ** (если не запущен):
   ```bash
   docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```

2. **Запустите оба сервиса** в отдельных терминалах:
   - **Для первого сервиса (`app.py`)**:
     ```bash
     faststream run app:app
     ```
     Вывод:
     ```
     INFO     - FastStream app starting...
     INFO     - input-queue  |            - `handle_message` waiting for messages
     INFO     - output-queue |            - `check_result` waiting for messages
     INFO     - FastStream app started successfully! To exit press CTRL+C
     ```

   - **Для второго сервиса (`app2.py`)**:
     ```bash
     faststream run app2:app
     ```
     Вывод:
     ```
     INFO     - FastStream app starting...
     INFO     - final-queue  |            - `final_result` waiting for messages
     INFO     - FastStream app started successfully! To exit press CTRL+C
     ```

3. **Отправьте сообщение**:
   ```bash
   python send_message.py
   ```

   **Вывод в терминале `app.py`**:
   ```
   INFO     - input-queue  |            - Получено: Alice сказал 'Hello'
   INFO     - output-queue |            - Промежуточный результат: Alice сказал 'HELLO'
   ```

   **Вывод в терминале `app2.py`**:
   ```
   INFO     - final-queue  |            - Финальный результат: {"username": "Alice", "message": "HELLO"}
   ```

**Что произошло?** 🔄  
FastStream получил JSON из `input-queue`, проверил его через Pydantic, обработал сообщение в `handle_message` и отправил результат в `output-queue` и `final-queue`. Подписчик `check_result` обработал данные из `output-queue`, а `app2.py` — из `final-queue`. Всё работает! 🎉

## Шаг 4: Проверка валидации 🛡️

Pydantic автоматически валидирует сообщения. Проверим, что происходит при отправке неверного JSON. Создайте `send_message_invalid.py`:

```python linenums="1" title="send_message_invalid.py" hl_lines="7"
--8<-- "src/tutorial/pydantic/send_message_invalid.py"
```

Убедитесь, что оба сервиса (`app.py` и `app2.py`) запущены. Запустите:

```bash
python send_message_invalid.py
```

**Что произойдет?** 🔍  
Сообщение `{ "wrong_field": "Hello" }` не соответствует структуре `UserMessage`, так как модель ожидает поля `username` и `message`, оба типа `str`. Pydantic выбросит ошибку валидации, и `handle_message` не обработает сообщение. В терминале `app.py` вы увидите лог ошибки, например:

```
ERROR    - input-queue  |            - ValidationError: ...
```

Сообщение не будет отправлено в `output-queue` или `final-queue`, поэтому `check_result` и `app2.py` ничего не получат. Pydantic защищает приложение от некорректных данных! 🛡️

## Шаг 5: Практическое задание 📚

Закрепите знания:

1. Добавьте в `UserMessage` поле `timestamp: datetime`, обновите `handle_message`, чтобы включать текущую дату (`datetime.now()`), и проверьте результат в логах `check_result` и `app2.py`.
2. Измените `send_message.py`, чтобы отправлять сообщение с `timestamp`, и проверьте валидацию.
3. (Дополнительно) Настройте `message` с `min_length=1` и проверьте, что пустая строка вызывает ошибку валидации.

## Что дальше? 🗺️

Вы научились использовать Pydantic для структурирования и валидации сообщений! 🎉 Это делает ваше приложение надежным. В следующем разделе мы протестируем приложение без реального брокера. Перейдите к [**Тестирование приложения**](./testing.md), чтобы освоить инструменты тестирования FastStream.

Если у вас есть вопросы или нужна помощь, загляните в [официальную документацию FastStream](https://faststream.airt.ai/latest/), пишите в [Telegram](https://t.me/python_faststream) или [Discord](https://discord.gg/qFm6aSqq59). Продолжайте кодить! 🚀
