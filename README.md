# ivanefremovbot

Ссылка на бота: https://t.me/ivanefremovbot

## Инструкция
* git clone https://github.com/497d2c8f/ivanefremovbot.git
* cd ivanefremovbot
* sed -i 's/your_bot_token/**СЮДА_ВСТАВИТЬ_СВОЙ_ТОКЕН**/g' compose.yaml (в файле compose.yaml Ваш токен присвоится переменной среды BOT_TOKEN сервиса ivanefremovbot-aiogram)
* sudo docker compose up

## Краткое описание архитектуры
Aiogram, Nginx, Django, Postgresql и Redis работают в отдельных контейнерах 
под управлением Docker Compose.
Запрос от телеграм-бота поступает в Aiogram. 
Aiogram в свою очередь либо сразу отправляет ответ боту, 
либо совершает запрос к Django через Nginx. Данные хранятся в Potgresql. 
В одном контейнере с Django-приложением запущен Celery, 
который периодически берет из Postgresql и отправляет в Redis 
задачи с истекшим временем выполнения.
Aiogram читает из Redis'а эти задачи, и отправляет их
авторам задач (на самом деле не отправляет, 
не получилось это сделать, подробности ниже).

## С какими трудностями я столкнулся
* У меня не получилось реализовать периодическую отправку 
сообщений пользователям о просроченных задачах. 
Я настроил передачу сообщений из Celery в Aiogram, 
но саму отправку сообщений конкретному пользователю 
мне сделать не удалось.
* Я пока не знаю как сделать так, чтобы можно было 
красиво отправить дату и время телеграм-боту. 
Я понял, что это всё настраивается через виджеты, 
но т.к. телеграм-бота я пишу впервые, знания об Aiogram 
у меня пока мягко говоря поверхностные)))
* И у меня не получилось не использовать 
целочисленные инкременты в качестве первичного ключа. 
В моих моделях нет уникальных полей.
В Django 5.2 появилось поле CompositePrimaryKey, 
которое позволило бы не использовать целочисленные инкременты, 
но при установке этой версии Django с гитхаба возникла ошибка 
на которую я потратил достаточно времени 
и не стал тратить ещё больше, т.к. его было мало.
* прочие проблемы связанные со случайно допущенными ошибками, 
с тонкостями работы различных библиотек и прочие ошибки. 
Их перечислять здесь уже не буду. Если что, спрашивайте)))

## Примечания
Чтобы можно было пользоваться админ-панелью, мне пришлось добавить Nginx для обработки статики (без статики админ-панель выглядела страшно), и пробросить на него порт 8000, для подключения к админ-панели Django с локального хоста. Из-за того, что появился Nginx, я решил использовать его в качестве прокси между Aiogram и Django.
