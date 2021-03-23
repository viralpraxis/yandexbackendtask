## Описание
Реализация RESTful веб-сервиса на основе фреймворка Django (3.1.7).<br>
В качестве базы данных используется PostgreSQL (12.6).<br>
Список библиотек, используемых в проекте, расположен в файле `requirements.txt`

## Локальная установка
Для локальной установки необходимо установить копию репозитория и установить зависимости:<br> `pip3 install -r requirements.txt`

## Запуск на виртуальной машине

На виртуальное машине создан сервис systemd (djangoserver.service).<br>
Соответственно, запустить сервер можно командой<br>
`sudo systemctl start djangoserver`<br>(запуск на сокете 0.0.0.0:8080).<br>
Для django.service включен автозапуск, сервер должен запускаться после перезагрузки<br>
виртуальной машины. 

Либо напрямую, выполнив`python3 manage.py runserver` из корня проекта

## Тестирование

Юнит-тесты и request-тесты покрывают все эндпоинты и основные сценарии.
Запуск тестов - `python3 manage.py test`
