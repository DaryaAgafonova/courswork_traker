## Habit Tracker

Django + DRF + Celery + Docker + CI/CD  
Трекер привычек с API, админкой и интеграцией с Telegram.

---

## Быстрый старт

### Клонируйте репозиторий

```bash
git clone https://github.com/DaryaAgafonova/courswork_traker.git
cd cours/coursof
```

### Создайте файл окружения

```bash
cp env.example .env
# Отредактируйте .env под себя (секреты, параметры БД и т.д.)
```

### Запустите проект через Docker

```bash
docker-compose up -d
```

### Примените миграции и создайте суперпользователя

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## Откройте в браузере

- **API:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Админка:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Тесты

```bash
docker-compose exec web python manage.py test
```

---

## CI/CD и деплой

- **CI/CD** реализован через GitHub Actions:
  - Каждый push в ветки `main` или `develop`:
    - Запускает тесты и линтер
    - Собирает и пушит Docker-образ в Docker Hub
    - Деплоит проект на сервер через SSH и `docker-compose.prod.yaml`
- **Secrets** для деплоя (`HOST`, `USERNAME`, `SSH_KEY`, `PORT`, `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`) добавляются в настройки репозитория.
- **На сервере** должен быть установлен Docker и Docker Compose.

### Production запуск на сервере

```bash
docker-compose -f docker-compose.prod.yaml pull
docker-compose -f docker-compose.prod.yaml up -d
```

---

## Swagger доступен по адресу

[http://89.169.35.19/swagger/](http://89.169.35.19/swagger/)

---

## Структура проекта

```
coursof/
├── .github/workflows/      # CI/CD
├── habit_tracker/          # Django settings
├── habits/                 # Приложение привычек
├── users/                  # Пользователи
├── docker-compose.yaml     # Для разработки
├── docker-compose.prod.yaml# Для продакшена
├── Dockerfile.prod         # Production Dockerfile
├── nginx.conf              # Nginx для Docker
└── requirements.txt        # Python-зависимости
```

---

## Полезные команды

- **Логи:**  
  `docker-compose logs -f`
- **Перезапуск:**  
  `docker-compose restart`
- **Остановка:**  
  `docker-compose down`

