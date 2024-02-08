<h1 align="center">s3_upload_bot</h1>

## Описание

Бот для загрузки файлов на S3 + запись данных в 1С

## Стек
Core: python 3, aiogram 2.x<br/>
Database: mysql<br/>
S3 client: Boto3<br/>

## Установка

1. Скачайте репозиторий<br/>

    ```bash
    git clone https://github.com/wilgood/s3_upload_bot.git && cd s3_upload_bot
    ```

2. Устанавливаем виртуальное окружение<br/>

    ```bash
    apt install -y python3-venv
    ```
    ```bash
    python3 -m venv env
    ```

3. Активируем её <br/>

    ```bash
    source env/bin/activate
    ```

4. Скачиваем и устанавливаем нужные библиотеки<br/>

    ```bash
    pip install -r requirements.txt
    ```

5. Изменить в скрипте mysql-setup.sh следующие параметры: <br/>
    
    Пользователь: bot_user
    Пароль: password1!
    База данных: s3_upload_bot

6. Запустить скрипт mysql-setup.sh<br/>
    даем права 
    ```bash
    chmod +x mysql-setup.sh
    ```
    запускаем скрипт
    ```bash
    /root/s3_upload_bot/mysql-setup.sh
    ```

7. Создаем .env файл с вашими данными, можно создать из шаблона и просто поправить поля <br/>

    ```bash
    cp .env.sample .env
    nano .env
    ```

8. Создаем .service файл для вашего бота 
    sudo nano /etc/systemd/system/s3_upload_bot.service<br/>

    ```ini
    [Unit]
    Description='Service for s3_upload_bot'
    After=network.target

    [Service]
    Type=idle
    Restart=on-failure
    StartLimitBurst=2
    # Restart, but not more than once every 30s (for testing purposes)
    StartLimitInterval=120
    User=root
    ExecStart=/bin/bash -c 'cd ~/s3_upload_bot/ && source env/bin/activate && python3 app.py'

    [Install]
    WantedBy=multi-user.target

    ```

9. Включаем сервис и запускаем<br/>

    ```bash
    systemctl enable s3_upload_bot.service
    systemctl start s3_upload_bot.service
    ```

10. Бот готов к использованию 

## Дополнительно

Для регистрации в 1С, у пользователя сотрудника должна быть установлена роль "Вложения Данные По Ремонту Добавление"

