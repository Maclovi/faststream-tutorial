# Добро пожаловать в FastStream: Руководство для новичков 🚀

**FastStream** — это современный Python-фреймворк, который упрощает создание микросервисов для работы с потоками данных через брокеры сообщений, такие как [RabbitMQ](https://www.rabbitmq.com/), [Kafka](https://kafka.apache.org/), [NATS](https://nats.io/) и [Redis](https://redis.io/). Он идеально подходит для тех, кто хочет быстро и без лишних сложностей начать работать с асинхронной обработкой данных. Это руководство создано, чтобы помочь вам плавно погрузиться в мир брокеров сообщений и создать свое первое приложение с FastStream! 🌟 Ознакомьтесь с [официальной документацией](https://faststream.airt.ai/latest/) или [репозиторием на GitHub](https://github.com/airtai/faststream) для получения дополнительной информации.

## Для кого это руководство? 👩‍💻👨‍💻

Это руководство предназначено для:

- **Новичков в программировании**, которые знают основы Python и хотят освоить работу с потоковыми данными. 🐣
- **Разработчиков**, желающих изучить брокеры сообщений и микросервисы. 🛠️
- **Тех, кто ищет простой способ интеграции приложений** с RabbitMQ, Kafka или другими брокерами. 🔗

Независимо от вашего уровня подготовки, мы начнем с азов и постепенно разберем все этапы создания приложения.

## Что вы узнаете? 🎯

В этом руководстве вы:

- Поймете, что такое брокеры сообщений и зачем они нужны. 📬
- Установите FastStream и RabbitMQ для работы с потоками данных. ⚙️
- Создадите простое приложение, которое принимает, обрабатывает и отправляет сообщения. 💻
- Научитесь организовывать взаимодействие между сервисами через брокер. 🤝
- Используете **Pydantic** для структурирования и валидации данных. ✅
- Протестируете приложение без реального брокера. 🧪
- Сгенерируете красивую документацию в формате **AsyncAPI**. 📝

Мы будем использовать **RabbitMQ** как основной брокер, так как он прост в настройке и широко применяется, но навыки, полученные здесь, легко применимы к другим брокерам, поддерживаемым FastStream.

## Предварительные требования 🛠️

Для работы с руководством вам понадобится:

- **Python 3.9+**: Убедитесь, что Python установлен (`python --version`). 🐍
- **Базовые знания Python**: Умение писать функции, работать с модулями и устанавливать пакеты через `pip`. 📚
- **Текстовый редактор или IDE**: Например, VS Code, PyCharm или любой другой. ✍️
- **Docker (рекомендуется)**: Для быстрого запуска RabbitMQ. Если Docker не используется, можно установить RabbitMQ вручную. 🐳

Не волнуйтесь, если что-то из этого звучит сложно — мы подробно разберем установку в следующем разделе! 😊

## Основная терминология 📖

Чтобы начать работу с FastStream и брокерами сообщений, важно понимать ключевые термины. Вот основные понятия, которые мы будем использовать:

- **Брокер сообщений** 📨: Программное обеспечение, которое принимает сообщения от отправителей, хранит их и доставляет получателям. Примеры: RabbitMQ, Kafka, Redis.
- **Publisher** 📤: Компонент, который отправляет сообщения в брокер. В FastStream это декоратор `broker.publisher`, реализованный как метод брокера, используемый для публикации сообщений.
- **Subscriber** 📥: Компонент, который получает сообщения из брокера. В FastStream это декоратор `broker.subscriber`, реализованный как метод брокера, обрабатывающий входящие сообщения.
- **Очередь** 🗄️: Структура данных в брокере (например, в RabbitMQ), где хранятся сообщения до их обработки. Очереди обеспечивают порядок и надежность доставки.
- **Сообщение** 💬: Данные, которые передаются через брокер. Это может быть строка, JSON или другой формат.
- **Асинхронность** ⚡: Подход, при котором отправка и обработка сообщений происходят независимо друг от друга, что повышает производительность и масштабируемость.
- **Pydantic** 🛡️: Библиотека для валидации и структурирования данных в Python. В FastStream используется для определения формата сообщений.
- **AsyncAPI** 📜: Стандарт для документирования асинхронных API. FastStream автоматически генерирует документацию в этом формате.

Эти термины будут встречаться на протяжении всего руководства, и мы будем объяснять их в контексте примеров.

## Навигация по руководству 🗺️

Руководство состоит из следующих разделов:

- [**Что такое брокеры сообщений?**](./ru/introduction.md): Объяснение концепции и роли брокеров. 📚
- [**Установка и настройка**](./ru/setup.md): Подготовка окружения с FastStream и RabbitMQ. ⚙️
- [**Создаем первое приложение**](./ru/first_app.md): Пишем и запускаем приложение для обработки сообщений. 💻
- [**Взаимодействие между сервисами**](./ru/inter_service.md): Организация взаимодействия микросервисов через брокер с использованием нескольких подписчиков. 🤝
- [**Структурированные сообщения с Pydantic**](./ru/pydantic.md): Работа с JSON и валидацией данных. ✅
- [**Тестирование приложения**](./ru/testing.md): Проверка кода без реального брокера. 🧪
- [**Генерация документации**](./ru/documentation.md): Создание AsyncAPI-документации. 📝
- [**Что дальше?**](./ru/next_steps.md): Идеи для дальнейшего изучения FastStream. 🚀

Каждый раздел включает примеры кода, пояснения и практические задания, чтобы закрепить знания.

## Начнем! 🎉

Готовы погрузиться в мир потоковых микросервисов? Перейдите к разделу [**Что такое брокеры сообщений?**](./ru/introduction.md), чтобы узнать, как они работают, или сразу к [**Установка и настройка**](./ru/setup.md), чтобы подготовить окружение.

Если у вас есть идеи, вопросы или нужна помощь, загляните в [официальную документацию FastStream](https://faststream.airt.ai/latest/), пишите в [Telegram](https://t.me/python_faststream) или [Discord](https://discord.gg/qFm6aSqq59). Давайте начнем создавать крутые приложения! 💪
