
Для работы потребуется:

Установить питон 3.6;

Установить фреймворк Python Eve:

pip3 install eve

Для проверки содержимого базы данных из консоли рекомендуется скачать инструмент HTTPie:

pip3 install httpie

команда вывода содержимого базы:

http http://0.0.0.0:5000/users


Для начала работы необходимо запустить сервер с помощью команды:

python3 run.py

Далее в другом окне консоли выполнить запуск клиентской части сервиса:

python3 main.py

Далее следовать подсказкам в «интерфейсе» программы…