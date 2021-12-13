from TelegramBot import TelegramBot
from ScenarioForBot import PizzaScenario
from BotBuilder import BotBuilder


bot = BotBuilder().add_bot(TelegramBot('5053329276:AAErOa5dvMqnpsbl-di9YXlvbY5hjCh-L7A',PizzaScenario.generate_scenario))
bot.start()
