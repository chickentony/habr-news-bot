# habr-news-bot
Бот для мониторинга новостей на хабре

### Список команд:
`make build` - собрать docker образ с приложением.

`make start` - запустить docker контейнер с приложением. 
Предварительно нужно прокинуть токен бота: `export BOT_TOKEN="your telegram bot token here"`

`make test` - запустить unit тесты.

`make lint` - запустить линтер.
