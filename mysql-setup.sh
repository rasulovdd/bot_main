# Установка MySQL
sudo apt-get update
sudo apt-get install mysql-server -y

# Добавление MySQL в автозагрузку
sudo systemctl enable mysql

# Настройка базы данных
sudo mysql <<EOF
CREATE DATABASE s3_upload_bot;
CREATE USER 'bot_user'@'localhost' IDENTIFIED BY 'bot_password1!';
GRANT ALL PRIVILEGES ON s3_upload_bot.* TO 'bot_user'@'localhost';
FLUSH PRIVILEGES;
EOF

# Создание таблицы 'users' в базе данных 's3_upload_bot'
sudo mysql -e "USE s3_upload_bot;
CREATE TABLE IF NOT EXISTS users (
  id bigint(20) PRIMARY KEY AUTO_INCREMENT,
  user_id bigint(20) UNIQUE,
  status smallint(3)
);
CREATE TABLE IF NOT EXISTS tmp (
  user_id bigint(20) UNIQUE,
  message_id bigint(20),
  orders_guid varchar(50),
  file_ext varchar(10),
  file_type varchar(10),
  file_path varchar(200)
);
CREATE TABLE IF NOT EXISTS orders (
  user_id bigint(20),
  message_id bigint(20),
  docnumber varchar(10),
  docdate varchar(50),
  guid varchar(50),
  model varchar(30),
  regn varchar(10),
  vin varchar(50),
  tmp int(10)
);"

sudo sed -i 's/bind-address.*/bind-address = 127.0.0.1/' /etc/mysql/mysql.conf.d/mysqld.cnf

# Установка часового пояса в Moscow
sudo mysql -e "SET GLOBAL time_zone = '+3:00';"
sudo mysql -e "SET SESSION time_zone = '+3:00';"

# Перезапуск MySQL для применения изменений
sudo systemctl restart mysql

echo "MySQL установлен и настроен успешно."
echo "Пользователь: bot_user"
echo "Пароль: bot_password1!"
echo "База данных: s3_upload_bot"
echo "Таблицы: users, tmp, orders"
echo "......"