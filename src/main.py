from telegram import Update

from bot.core import logger  # noqa
from bot.services import init_bot


def main() -> None:
    """Run application."""
    application = init_bot()
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
