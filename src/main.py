from dispatcher import bot
from bot_logger import init_logger
from settings import CRM_TOKEN


logger = init_logger(__name__)


if __name__ == "__main__":
    print(CRM_TOKEN)
    print("Polling has started")
    bot.run_forever()