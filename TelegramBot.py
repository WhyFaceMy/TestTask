
import telebot as tb
from telebot import types
from BotInterface import BotInterface
from ScenarioForBot import PizzaScenario
import sys
sys.setrecursionlimit(1500)
class TelegramBot(BotInterface):

    def __init__(self,token,scenario_generator):
        self.bot = tb.TeleBot(token)
        self.scenario_generator = scenario_generator
        self.clients = {}
        @self.bot.message_handler(commands=['start'])
        def start_bot(message):

            current_user= self.scenario_generator()
            self.clients[message.from_user.id] = current_user
            self.if_next_step_transition(current_user,message)

        @self.bot.message_handler(content_types=['text'])
        def get_text_messages(message):

            current_user = None
            if message.from_user.id in self.clients:
                current_user= self.clients[message.from_user.id]
            else:
                current_user= self.scenario_generator()
                self.clients[message.from_user.id] = current_user
                self.if_next_step_transition(current_user,message)

            self.to_next_step_transition(current_user,message)

    def start(self):
        self.bot.polling(none_stop=True, interval=0)
    def stop(self):
        pass
    def if_next_step_transition(self,current_user,message):
        next_trans_label = current_user.get_next_transitions()
        next_trans_desc  = current_user.get_next_description(next_trans_label)
        text_data = list(filter(lambda x: x['format']=='text',next_trans_desc.values()))
        sendet_text = []
        for data in text_data:
            sendet_text.append(current_user.get_data_for_view_client(data['for_client']))
        button_data=list(filter(lambda x: x['format']=='button',next_trans_desc.values()))
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        actions_text = []
        if len(button_data)>0:

            for button in button_data:

                reply_markup.add(types.KeyboardButton(button.get('action')))
                actions_text.append(current_user.get_data_for_view_client(button['for_client']))
        if(len(sendet_text)==0):
            if len(actions_text)>0:
                sendet_text+=actions_text
        self.bot.send_message(message.from_user.id,sendet_text,reply_markup=reply_markup)


    def to_next_step_transition(self,current_user,message):
        next_trans_label = current_user.get_next_transitions()
        next_trans_desc  = current_user.get_next_description(next_trans_label)
        button_data=list(filter(lambda x: x['format']=='button',next_trans_desc.values()))
        updated = False
        for button in button_data:
            if(button['action']==message.text):

                try:
                    key = TelegramBot.get_key(next_trans_desc,button)

                    trig = current_user.trigger(key,message.text)
                    if( trig):
                        self.if_next_step_transition(current_user,message)
                        updated = True
                        break
                except Exception as e:
                    print('Error ',e)
        text_data = list(filter(lambda x: x['format']=='text',next_trans_desc.values()))
        if not updated:
            for data in text_data:

                try:

                    key = TelegramBot.get_key(next_trans_desc,data)
                    trig = current_user.trigger(key,message.text)
                    if( trig):
                        self.if_next_step_transition(current_user,message)
                        updated = True
                        break
                except Exception as e:
                    print('Error ',e)
                if not updated:
                    self.bot.send_message(message.from_user.id,data['error'])

        #if message.text == "Привет":
        #    bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
        #elif message.text == "/help":
        #    bot.send_message(message.from_user.id, "Напиши привет")
        #else:
        #    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
    def get_key(my_dict,val):

        for key, value in my_dict.items():
            if val == value:
                return key
        raise Exception("key doesn't exist")

if __name__ == '__main__':
    tb = TelegramBot('5053329276:AAErOa5dvMqnpsbl-di9YXlvbY5hjCh-L7A',PizzaScenario.generate_scenario)
    tb.start()
