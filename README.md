### README для Django проекта

Этот проект — это блог с возможностью добавления комментариев к постам, который включает в себя такие функции, как капча для защиты от спама, возможность добавления медиафайлов (изображений, текстовых файлов) в комментарии и поддержка HTML-тегов для форматирования текста в комментариях. Пользователи могут оставлять комментарии после входа в систему, а также имеют возможность регистрироваться.

Ниже приведена подробная инструкция по установке и использованию проекта.

---

## 1. Требования

Перед установкой проекта убедитесь, что у вас установлены следующие компоненты:

- **Python 3.10** или выше
- **Django 4.x**
- **PostgreSQL** (опционально, но рекомендовано для работы в production)
- **Virtualenv** (опционально, но рекомендовано для изоляции окружений)
- **Pip** — менеджер пакетов Python

## 2. Установка проекта

### 2.1. Клонирование репозитория

Сначала клонируйте репозиторий проекта с помощью `git`:

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### 2.2. Создание и активация виртуального окружения

Для изоляции зависимостей создайте виртуальное окружение:

```bash
python3 -m venv venv
```

Активируйте окружение:

- На Windows:
  ```bash
  venv\Scripts\activate
  ```

- На Linux или macOS:
  ```bash
  source venv/bin/activate
  ```

### 2.3. Установка зависимостей

Установите все зависимости проекта, используя файл `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2.4. Настройка базы данных

Проект использует **PostgreSQL** в качестве базы данных. Для этого выполните следующие шаги:

1. Создайте базу данных в PostgreSQL:
    ```sql
    CREATE DATABASE myproject;
    ```

2. Настройте пользователя и права доступа:
    ```sql
    CREATE USER myprojectuser WITH PASSWORD 'password';
    ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
    ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE myprojectuser SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
    ```

3. Настройте переменные окружения для подключения к базе данных. В корне проекта создайте файл `.env` с содержимым:

    ```
    DATABASE_NAME=myproject
    DATABASE_USER=myprojectuser
    DATABASE_PASSWORD=password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    ```

4. В файле `settings.py` добавьте следующие строки, чтобы читать настройки базы данных из `.env`:

    ```python
    import os
    from dotenv import load_dotenv

    load_dotenv()

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DATABASE_NAME'),
            'USER': os.getenv('DATABASE_USER'),
            'PASSWORD': os.getenv('DATABASE_PASSWORD'),
            'HOST': os.getenv('DATABASE_HOST'),
            'PORT': os.getenv('DATABASE_PORT'),
        }
    }
    ```

### 2.5. Применение миграций

После настройки базы данных выполните миграции для создания необходимых таблиц:

```bash
python manage.py migrate
```

### 2.6. Создание суперпользователя

Для доступа к административной панели создайте суперпользователя:

```bash
python manage.py createsuperuser
```

Следуйте инструкциям и укажите имя пользователя, email и пароль для суперпользователя.

### 2.7. Запуск сервера

Для запуска проекта локально используйте команду:

```bash
python manage.py runserver
```

Теперь проект доступен по адресу `http://127.0.0.1:8000`.

---

## 3. Функционал проекта

### 3.1. Комментарии и форма

Проект включает функционал для добавления комментариев к постам. Основные функции:

- **HTML-теги**: Пользователи могут форматировать комментарии с использованием следующих HTML-тегов:
  - `<i>` — для курсива
  - `<strong>` — для жирного текста
  - `<code>` — для вставки кода
  - `<a>` — для ссылок

- **Медиафайлы**: В комментарии можно добавлять изображения и текстовые файлы.

- **Капча**: Для защиты от спама используется CAPTCHA (Django CAPTCHA).

### 3.2. Поля формы

Поля формы для добавления комментария включают:

- **Имя пользователя (user_name)** — строка, содержащая только буквы и цифры.
- **E-mail** — обязательное поле для ввода электронной почты.
- **Домашняя страница (home_page)** — опциональное поле для ввода URL.
- **Текст комментария (text)** — текстовое поле для ввода комментария.
- **Изображение (image)** — поле для загрузки изображений.
- **Файл (file)** — поле для загрузки текстовых файлов.

### 3.3. Использование HTML-тегов

Для вставки HTML-тегов в комментарии на форме комментария доступны кнопки для быстрого добавления тегов. Эти теги могут быть использованы для форматирования текста комментария, например:

- Тег **[i]** для курсивного текста,
- Тег **[strong]** для выделения текста,
- Тег **[code]** для вставки кода,
- Тег **[a]** для вставки ссылки.

Пример HTML-тегов в тексте комментария:

```html
<i>Курсивный текст</i>
<strong>Жирный текст</strong>
<code>print("Пример кода")</code>
<a href="https://example.com">Ссылка</a>
```

---

## 4. Тестирование проекта

### 4.1. Запуск тестов

Для тестирования проекта используется Django Test Framework. Запустите тесты, выполнив команду:

```bash
python manage.py test
```

---

## 5. Деплой проекта

### 5.1. Настройка в режиме Production

Для работы в режиме production рекомендуем использовать **Gunicorn** в связке с **Nginx**. Убедитесь, что у вас установлен Gunicorn:

```bash
pip install gunicorn
```

### 5.2. Запуск Gunicorn

Запустите Gunicorn:

```bash
gunicorn --workers 3 myproject.wsgi:application
```

### 5.3. Настройка Nginx

Создайте конфигурацию для Nginx:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/static/files;
    }

    location /media/ {
        alias /path/to/your/media/files;
    }
}
```

Перезапустите Nginx:

```bash
sudo systemctl restart nginx
```

---

## 6. Часто задаваемые вопросы

### 6.1. Как добавить пост?

1. Авторизуйтесь в системе.
2. Перейдите на страницу "Добавить пост".
3. Заполните форму, используя теги для форматирования текста.
4. Нажмите "Опубликовать".

### 6.2. Как вставить теги в комментарий?

Для вставки тегов в комментарий используйте кнопки, расположенные над полем ввода текста в форме комментария.

---

### Авторы

- Ваше Имя — [YourGithub](https://github.com/yourusername)

### Лицензия

Проект распространяется под лицензией MIT.