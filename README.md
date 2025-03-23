# wiremock-demo
Wiremock — это инструмент с открытым исходным кодом, предназначенный для создания HTTP заглушек (моков) для веб-сервисов.
Он широко используется в юнит-тестировании и тестировании API, предоставляя разработчикам и тестировщикам возможность задать заранее определенные ответы на HTTP-запросы.

Текущий проект представляет собой небольшой фреймворк, который демонстрирует работу с моками с использованием Wiremock.

Используемый стек: Python, pytest, pytest-cases, requests.

Дополнительные ссылки:
- Официальный сайт Wiremock: https://wiremock.org/
- Коллекция Postman с демо-запросами: [wiremock-demo.postman_collection.json](./wiremock-demo.postman_collection.json)

Основные фичи:
1. Реализованы тесты для демонстрации использования WireMock. Тесты написаны с помощью pytest и параметризованы с использованием pytest-cases.
2. Поддержка создания сложных маппингов с использованием шаблонов для генерации ответов.
3. Структуры данных описаны с помощью BaseModel из библиотеки pydantic для удобства и надежности работы с JSON данными.
4. Поддержка конфигурации и настройки маппингов через API WireMock, включая работу с заголовками, параметрами и телом запроса.

<br />

### 1. Конфигурация проекта

#### 1.1. Установите Python (3.12)

#### 1.2. Установите poetry
```commandline
brew install poetry
```
или
```commandline
pip install poetry
```

#### 1.3. Клонируйте Git репозиторий
```commandline
git clone https://github.com/t-kutenkova/wiremock-demo.git
```

#### 1.4. Установите внешние библиотеки, используя poetry (они перечислены в pyproject.toml)
```commandline
cd wiremock-demo
poetry env use 3.12
poetry install
```

#### 1.5. Включите pre-commit хуки
Pre-commit хуки позволяют автоматически проверять код на наличие синтаксических ошибок и нарушений Code Style.
В проекте уже есть готовый конфиг для хуков, необходимо только их включить:
```commandline
poetry run pre-commit install
```
Чтобы убедиться, что хуки работают, можно выполнить следующую команду:
```commandline
poetry run pre-commit run --all-files
```
Теперь каждый раз, когда вы будете пытаться сделать коммит, будет выполняться набор проверок ваших изменений.

<br />

### 2. Запуск Wiremock

Запуск Wiremock внутри Docker контейнера:
```commandline
docker compose up wiremock-server
```
После старта контейнера Wiremock станет доступен по адресу http://localhost:8080.
Чтобы убедиться, что сервер поднялся, выполните команду получения всех существующих маппингов:

```commandline
curl http://localhost:8080/__admin/mappings
```

<br />

### 3. Запуск тестов

Запуск всех тестов:
```commandline
poetry run pytest  -s -v -rxX --color yes --show-capture all --tb short --disable-warnings --log-cli-level=INFO
```
