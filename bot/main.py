import logging

from app import get_bot


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    bot = get_bot()
    bot.start_polling()
    bot.idle()
