# -*- coding: utf-8 -*-
# Указываем кодировку UTF-8 для поддержки русских символов

"""
Модели базы данных.
Здесь определяются таблицы и структура данных приложения.
"""

# Импортируем объект базы данных из текущего пакета
from app import db
# db: объект SQLAlchemy из __init__.py

# Импортируем UserMixin из flask_login для базовой реализации пользователя
from flask_login import UserMixin
# UserMixin: предоставляет стандартные методы для Flask-Login

# Импортируем функции для безопасного хранения паролей
from werkzeug.security import generate_password_hash, check_password_hash
# generate_password_hash: создает безопасный хеш пароля
# check_password_hash: проверяет пароль по хешу
# КРИТИЧЕСКИ ВАЖНО для безопасности!

# Импортируем datetime для отметок времени
from datetime import datetime


class User(UserMixin, db.Model):
    """
    Модель пользователя.
    Наследуется от UserMixin (для Flask-Login) и db.Model (для SQLAlchemy).
    Каждый объект этого класса представляет одну запись в таблице users.
    """

    # Определяем колонки таблицы базы данных

    id = db.Column(db.Integer, primary_key=True)
    # id: уникальный идентификатор пользователя
    # db.Column: создает колонку в таблице
    # db.Integer: тип данных - целое число
    # primary_key=True: это первичный ключ (уникальный для каждой записи)

    username = db.Column(db.String(80), unique=True, nullable=False)
    # username: имя пользователя для входа
    # db.String(80): строка максимальной длины 80 символов
    # unique=True: значение должно быть уникальным (не может быть двух одинаковых)
    # nullable=False: поле обязательно для заполнения (не может быть пустым)

    password_hash = db.Column(db.String(200), nullable=False)
    # password_hash: ХЕШИРОВАННЫЙ пароль пользователя
    # ВАЖНО: Никогда не храните пароли в открытом виде!
    # db.String(200): строка максимальной длины 200 символов (хеш длиннее пароля)
    # nullable=False: поле обязательно для заполнения

    clicks = db.Column(db.Integer, default=0)
    # clicks: количество кликов пользователя
    # db.Integer: целое число
    # default=0: значение по умолчанию - 0 (при создании пользователя)

    coins = db.Column(db.Integer, default=0)
    # coins: количество монет пользователя (добавляем для игры-кликера)
    # default=0: начальное количество монет

    level = db.Column(db.Integer, default=1)
    # level: уровень игрока
    # default=1: начальный уровень

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # created_at: дата и время создания аккаунта
    # default=datetime.utcnow: автоматически устанавливает текущее время UTC

    def set_password(self, password):
        """
        Устанавливает пароль пользователя, хешируя его для безопасного хранения.

        Args:
            password (str): Пароль в открытом виде
        """
        self.password_hash = generate_password_hash(password)
        # generate_password_hash: создает безопасный хеш из пароля
        # Хеширование необратимо - нельзя восстановить пароль из хеша

    def check_password(self, password):
        """
        Проверяет, соответствует ли предоставленный пароль хешу в базе дан-ных.

        Args:
            password (str): Пароль для проверки

        Returns:
            bool: True если пароль верный, False если нет
        """
        return check_password_hash(self.password_hash, password)
        # check_password_hash: сравнивает пароль с хешем
        # Возвращает True если совпадает, False если нет

    def get_id(self):
        """
        Возвращает ID пользователя в виде строки.
        Требуется Flask-Login для работы с сессиями.

        Returns:
            str: ID пользователя как строка
        """
        # Flask-Login требует, чтобы get_id() возвращал строку
        # Преобразуем числовой id в строку с помощью str()
        return str(self.id)

    def __repr__(self):
        """
        Магический метод для строкового представления объекта.
        Используется при выводе объекта в консоли или логах.

        Returns:
            str: Строковое представление пользователя
        """
        return f'<User {self.username}>'