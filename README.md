Bot assistent 
=================================

The web-service uses Telegram BOT API to send message with the homework status from https://praktikum.yandex.ru/api/user_api/homework_statuses/  to the specified chat in Telegram (CHAT_ID, file .env).
If the homework status has changed during specified time interval, then the response will be data in JSON format. The interval is set from time, in the from_date parameter, to the current moment. The time is passed in Unix time format.

There were used OAuth(Open Authorization), package telegram(that contains methods of Bot API), library request and loggin.
The project was deploed on https://www.heroku.com/.

Getting Started
===============

1.  You can build it in steps:
    1.  ``cd ...wherever...``
    2.  ``git clone https://github.com/volhadounar/api_sp1_bot.git``
    3.  ``cd api_sp1_bot``
    4.  ``touch .env`` -- Creates file to keep secret data.
        You have to be registed on https://telegram.org/ to run the app.
        File .env should contain: 
        1. PRACTICUM_TOKEN=    -- Yandex practikum token
        2. TELEGRAM_TOKEN=     -- Telegram token [ use @BotFather to create a bot in Telegram, then it sends to you the token access the Bot API]
        3. CHAT_ID=            -- Your chat id in telegram [ask @userinfobot] or any other Telegram id that will recieves message
    5.  ``pip install -r requirements.txt``  -- Should install everything you need.
    6.  ``python3 homework`` -- Running localy
