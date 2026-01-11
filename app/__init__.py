# -*- coding: utf-8 -*-
# Указываем кодировку UTF-8 для поддержки русских символов

"""
Файл инициализации Flask приложения.
Этот файл создает и настраивает экземпляр Flask приложения.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Создаем экземпляр базы данных
db = SQLAlchemy()

# Создаем менеджер аутентификации
login_manager = LoginManager()

# Глобальная переменная app (будет инициализирована в create_app)
app = None


def create_app():
    """
    Фабричная функция для создания Flask приложения.
    """
    global app
    app = Flask(__name__)

    # Настройки конфигурации
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-123')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clicker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализируем расширения
    db.init_app(app)
    login_manager.init_app(app)

    # Настройки Flask-Login
    login_manager.login_view = 'login'  # Страница для входа
    login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице.'
    login_manager.login_message_category = 'info'

    # ВАЖНО: Функция для загрузки пользователя (user_loader)
    @login_manager.user_loader
    def load_user(user_id):
        """
        Загружает пользователя по ID из сессии.
        Flask-Login вызывает эту функцию при каждом запросе.
        """
        from app.models import User
        return User.query.get(int(user_id))

    # Импортируем маршруты
    from app import routes

    return app
