# celery_app.py
import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# Загружаем конфигурацию из переменных окружения
broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# Создаем экземпляр Celery
# Указываем имя основного модуля, где будут задачи (tasks)
app = Celery(
    'neuro_social_analyzer',
    broker=broker_url,
    backend=result_backend,
    include=['tasks'] # Список модулей с задачами для автообнаружения
)

# Опциональная конфигурация Celery (можно добавить таймауты, сериализаторы и т.д.)
app.conf.update(
    result_expires=3600, # Время хранения результатов задач (в секундах)
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC', # Или ваш часовой пояс, например 'Europe/Moscow'
    enable_utc=True,
    # Ограничение скорости выполнения задач (опционально)
    # task_annotations = {'tasks.update_person_from_vk': {'rate_limit': '10/m'}} # Не более 10 задач в минуту
)

if __name__ == '__main__':
    app.start()