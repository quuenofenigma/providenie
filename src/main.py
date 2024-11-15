from bot.core import logger  # noqa
from bot.services import init_bot
from telegram import Update


def main() -> None:
    application = init_bot()
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
