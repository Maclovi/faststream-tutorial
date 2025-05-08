# Структурированные сообщения с Pydantic ✅

В предыдущем разделе вы научились создавать сервисы, которые взаимодействуют через очереди RabbitMQ. Теперь пора сделать приложение мощнее! В этом разделе мы добавим **Pydantic** — фреймворк для структурирования и валидации данных. Это позволит обрабатывать JSON-сообщения с четкой структурой и автоматически проверять их корректность. Готовы улучшить ваше приложение? Погнали! 🚀

## Зачем нужен Pydantic? 🤔

Когда вы работаете с брокерами сообщений, данные часто приходят в формате JSON. Без проверки легко получить ошибки, если, например, в сообщении отсутствует нужное поле или поле имеет неверный тип. **Pydantic** решает эту проблему:

- **Структурирует данные** 📋: Вы определяете, как должны выглядеть сообщения (например, `{ "username": str, "message": str }`).
- **Валидирует автоматически** 🛡️: Если сообщение не соответствует структуре, FastStream выбросит ошибку.
- **Упрощает код** ✨: Вы работаете с типизированными объектами, а не с сырыми словарями.

В FastStream Pydantic интегрирован "из коробки", что делает работу с JSON-сообщениями удобной и безопасной. 😎

## Шаг 1: Обновление приложения ✍️

Обновим приложение из `app.py`, чтобы оно обрабатывало JSON-сообщения с полями `username` и `message`. Откройте `app.py` и замените код:

```python
--8<-- "src/tutorial/pydantic/app.py"
```

**Что изменилось?** 🔍

- **Модель `UserMessage`**: Класс Pydantic с полями `username` и `message`. Метаданные (`Field`) добавим позже в разделе про AsyncAPI.
- **`@broker.subscriber`**: Декораторы, регистрирующие функции как подписчиков на очереди `input-queue` и `output-queue`.
- **`handle_message`**: Принимает объект `UserMessage`, логирует данные и отправляет новый `UserMessage` с `message` в верхнем регистре в `output-queue`.
- **`check_result`**: Логирует результат из `output-queue`, показывая, как второй сервис (внутри того же приложения) потребляет данные.
- **`broker.publish`**: Отправляет структурированное сообщение в `output-queue`.

**Примечание** 🌐: В реальных системах `check_result` может быть в отдельном сервисе, как вы видели в `app2.py` в предыдущем разделе.

**Альтернативный способ отправки** 📤  
Вместо `broker.publish` можно использовать `@broker.publisher`:

```python
@broker.subscriber("input-queue")
@broker.publisher("output-queue")
async def handle_message(data: UserMessage, logger: Logger) -> UserMessage:
    logger.info(f"Получено: {data.username} сказал '{data.message}'")
    return UserMessage(username=data.username, message=data.message.upper())
```

Порядок декораторов важен: `@broker.subscriber` — внешний, `@broker.publisher` — внутренний, так как первый регистрирует подписчика, а второй обрабатывает возвращаемое значение.

## Шаг 2: Обновление отправки сообщений 📬

Обновим скрипт отправки сообщений, используя вашу версию. Создайте или обновите `send_message.py`:

```python
--8<-- "src/tutorial/pydantic/send_message.py"
```

**Почему контекстный менеджер?** 🔌 Контекстный менеджер (`async with`) вызывает только `broker.connect()` и `broker.close()`, что идеально для отправки сообщений без подписчиков.

## Шаг 3: Запуск и публикация сообщений ▶️

1. **Запустите RabbitMQ** (если не запущен):
   ```bash
   docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```

2. **Запустите приложение**:
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

3. **Отправьте сообщение**:
   ```bash
   python send_message.py
   ```
   В терминале приложения:
   ```
   INFO     - input-queue  |            - Получено: Alice сказал 'Hello'
   INFO     - output-queue |            - Промежуточный результат: Alice сказал 'HELLO'
   ```

FastStream получил JSON, проверил его через Pydantic, обработал сообщение и передал результат в `output-queue`, где второй подписчик показал его в логах. Всё работает! 🎉

## Шаг 4: Проверка валидации 🛡️

Pydantic автоматически валидирует сообщения. Проверим, что происходит при отправке неверного JSON. Создайте `send_message_invalid.py`:

```python
--8<-- "src/tutorial/pydantic/send_message_invalid.py"
```

Запустите:
```bash
python send_message.py
```

В терминале приложения вы увидите ошибку валидации:
```
ERROR    - input-queue |            - Validation error: ...
```

Pydantic отклонил сообщение из-за `wrong_field`, защищая приложение от некорректных данных! ✅

## Шаг 5: Практическое задание 📚

Закрепите знания:

1. Добавьте в `UserMessage` поле `timestamp: datetime`, обновите `handle_message`, чтобы включать текущую дату (`datetime.now()`), и проверьте результат в логах `check_result`.
2. Измените `send_message.py`, чтобы отправлять сообщение с `timestamp`, и проверьте валидацию.
3. (Дополнительно) Настройте `message` с `min_length=1` и проверьте, что пустая строка вызывает ошибку валидации.

## Что дальше? 🗺️

Вы научились использовать Pydantic для структурирования и валидации сообщений! 🎉 Это делает ваше приложение надежным. В следующем разделе мы протестируем приложение без реального брокера. Перейдите к [**Тестирование приложения**](./testing.md), чтобы освоить инструменты тестирования FastStream.

Если у вас есть вопросы или нужна помощь, загляните в [официальную документацию FastStream](https://faststream.airt.ai/latest/), пишите в [Telegram](https://t.me/python_faststream) или [Discord](https://discord.gg/qFm6aSqq59). Продолжайте кодить! 🚀
