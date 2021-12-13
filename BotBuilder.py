from BotInterface import BotInterface
from TelegramBot import TelegramBot
from ScenarioForBot import PizzaScenario

class BotBuilder:
    def __init__(self):
        self.bot=None
        self.__threads=[]
    def add_bot(self,bot:BotInterface):
        self.bot=bot
        return self

    def start(self):
        self.bot.start()


if( __name__ == '__main__'):
    bot = BotBuilder().add_bot(TelegramBot('5053329276:AAErOa5dvMqnpsbl-di9YXlvbY5hjCh-L7A',PizzaScenario.generate_scenario))
    bot.start()
