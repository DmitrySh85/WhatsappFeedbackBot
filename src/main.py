from dispatcher import bot
from bot_logger import init_logger


logger = init_logger(__name__)


if __name__ == "__main__":

    print("Polling has started")
    bot.run_forever()