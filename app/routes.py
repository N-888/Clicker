# -*- coding: utf-8 -*-
# Указываем кодировку UTF-8 для поддержки русских символов

"""
Маршруты (роуты) Flask приложения.
Здесь определяются все URL адреса и их обработчики.
"""

from flask import render_template, redirect, url_for, flash, request
# render_template: рендерит HTML шаблоны с переданными данными
# redirect: перенаправляет пользователя на другой URL
# url_for: генерирует URL по имени функции-обработчика
# flash: показывает одноразовые сообщения пользователю
# request: объект с данными текущего HTTP запроса

from flask_login import login_user, logout_user, login_required, current_user
# login_user: выполняет вход пользователя (создает сессию)
# logout_user: выполняет выход пользователя (удаляет сессию)
# login_required: декоратор для защиты маршрутов (только для авторизованных)
# current_user: объект текущего пользователя (даже если не авторизован)

# Импортируем базу данных из текущего пакета
from app import db
# db: объект базы данных из __init__.py

# Импортируем модели и формы
from app.models import User
# User: модель пользователя из models.py
from app.forms import LoginForm, RegisterForm
# LoginForm, RegisterForm: формы из forms.py

# Импортируем app из __init__.py
from app import app


# app: экземпляр Flask приложения из __init__.py


@app.route('/')
@app.route('/index')
def index():
    """
    Обработчик главной страницы.
    URL: http://ваш-сайт/

    Returns:
        Response: HTML страница index.html
    """
    return render_template('index.html', title='Главная')
    # Рендерим шаблон index.html с заголовком


@app.route('/game')
@login_required
def game():
    """
    Страница игры-кликера.
    Доступна только авторизованным пользователям.
    """
    return render_template('game.html', title='Игра')
    # Шаблон game.html нужно будет создать


@app.route('/click')
@login_required
def click():
    """
    Обработчик клика. Увеличивает счетчик кликов пользователя на 1.
    URL: http://ваш-сайт/click

    Returns:
        Response: Перенаправление на главную страницу с сообщением
    """
    # Увеличиваем счетчик кликов текущего пользователя на 1
    current_user.clicks += 1
    # current_user.clicks: обращаемся к полю clicks объекта пользователя

    # Увеличиваем монеты (например, 1 клик = 1 монета)
    current_user.coins += 1

    # Проверяем, не пора ли повысить уровень (например, каждые 10 кликов)
    if current_user.clicks % 10 == 0:
        current_user.level += 1
        flash(f'🎉 Поздравляем! Вы достигли уровня {current_user.level}!', 'success')

    # Сохраняем изменения в базе данных
    db.session.commit()
    # db.session: сессия базы данных
    # commit(): сохраняет все изменения в БД

    # Показываем сообщение об успешном клике
    flash('+1 клик! +1 монета! 💰', 'success')

    # Перенаправляем пользователя на главную страницу
    return redirect(url_for('index'))
    # redirect: отправляет браузеру команду перейти на другой URL
    # url_for('index'): генерирует URL для функции index()


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Обработчик страницы входа.
    GET: показывает форму входа
    POST: обрабатывает данные формы
    URL: http://ваш-сайт/login

    Returns:
        Response: HTML страница login.html или перенаправление
    """
    # Если пользователь уже авторизован, перенаправляем на главную
    if current_user.is_authenticated:
        flash('Вы уже вошли в систему!', 'info')
        return redirect(url_for('index'))

    # Создаем объект формы для входа
    form = LoginForm()

    # Проверяем, была ли форма отправлена и прошла ли валидацию
    if form.validate_on_submit():
        # Получаем данные из формы
        username = form.username.data
        password = form.password.data

        # Ищем пользователя в базе данных по имени
        user = User.query.filter_by(username=username).first()

        # Проверяем, существует ли пользователь и правильный ли пароль
        if user and user.check_password(password):
            # Если пользователь найден и пароль верный
            login_user(user, remember=True)
            # login_user: создает сессию для пользователя
            # remember=True: запоминает пользователя (использует cookies)

            # Показываем сообщение об успешном входе
            flash(f'Добро пожаловать, {username}! 🎊', 'success')

            # Перенаправляем на главную страницу
            return redirect(url_for('index'))
        else:
            # Если пользователь не найден или пароль неверный
            flash('Неверное имя пользователя или пароль', 'danger')

    # Рендерим страницу входа с формой
    return render_template('login.html', title='Вход', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Обработчик страницы регистрации.
    GET: показывает форму регистрации
    POST: обрабатывает данные формы и создает пользователя
    URL: http://ваш-сайт/register

    Returns:
        Response: HTML страница register.html или перенаправление
    """
    # Если пользователь уже авторизован, перенаправляем на главную
    if current_user.is_authenticated:
        flash('Вы уже вошли в систему!', 'info')
        return redirect(url_for('index'))

    # Создаем объект формы для регистрации
    form = RegisterForm()

    # Проверяем, была ли форма отправлена и прошла ли валидацию
    if form.validate_on_submit():
        try:
            # Получаем данные из формы
            username = form.username.data
            password = form.password.data

            # Проверяем, не существует ли уже пользователь с таким именем
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Это имя пользователя уже занято', 'danger')
                return render_template('register.html', form=form)

            # Создаем нового пользователя
            user = User(username=username)
            user.set_password(password)  # Хешируем пароль

            # Добавляем пользователя в базу данных
            db.session.add(user)
            db.session.commit()

            # Автоматически входим под новым пользователем
            login_user(user, remember=True)

            # Показываем сообщение об успешной регистрации
            flash(f'Регистрация успешна! Добро пожаловать, {username}! 🎉', 'success')

            # Перенаправляем на главную страницу
            return redirect(url_for('index'))

        except Exception as e:
            # Если произошла ошибка
            db.session.rollback()
            flash(f'Ошибка при регистрации: {str(e)}', 'danger')

    # Рендерим страницу регистрации с формой
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    """
    Обработчик выхода из системы.
    URL: http://ваш-сайт/logout

    Returns:
        Response: Перенаправление на главную страницу
    """
    # Выполняем выход пользователя
    logout_user()

    # Показываем сообщение о выходе
    flash('Вы вышли из системы. Возвращайтесь скорее! 👋', 'info')

    # Перенаправляем на главную страницу
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    """
    Страница профиля пользователя.
    Показывает статистику игрока.
    """
    return render_template('profile.html',
                           title='Профиль',
                           user=current_user)