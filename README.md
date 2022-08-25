## Установка и запуск redis и celery:

Устанавливаем docker

В консоли выпоняем команду:

```bash
docker pull redis
```

Запускаем редис:

```bash
docker run -d -p 6379:6379 redis
```

Запустить веб-сервер проекта:

```bash
python manage.py runserver
```

Запускаем celery:

Из папки, где у нас manage.py
```bash
celery -A marketplace worker -l info
```
