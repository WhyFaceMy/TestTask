from abc import ABCMeta, abstractmethod,abstractproperty
from transitions import Machine
from Scenario import Scenario
class PizzaScenario(Scenario):
    def generate_scenario():
        return PizzaScenario()

    __available_payment = ["наличкой", "по карте"]
    __available_food_sizes = ["маленькую", "большую"]
    __available_confirm = ['да',]
    __states = ['start','confirm','choose_size','choose_payment','end'] #['start','confirm','choose_size','choose_payment','end']
    __transitions = [
        #{'trigger':'cancel_order','source':['choose_size','choose_payment'],'dest':'cancel'},
        {'trigger':'start_of_order_assembly','source':'start','dest':'choose_size','conditions':'setted_size','prepare':'save_size'},
        {'trigger':'choose_a_payment_method','source':'choose_size','dest':'choose_payment','conditions':'setted_payment','prepare':'save_payment'},
        {'trigger':'confirm_order','source':'choose_payment','dest':'confirm','conditions':'confirm_o','prepare':'order_confirm'},
        {'trigger':'end_order','source':'confirm','dest':'end'},
        #{'trigger':'new_order','source':['cancel'],'dest':'start','prepare':'reset'},
        #{'trigger':'new_order','source':['confirm','cancel'],'dest':'start','prepare':'reset'},
    ]
    __view_element={

        'start_of_order_assembly':{'for_client':'Какую вы хотите пиццу? Большую или маленькую?','format':'text','action':"",'error':'Пожалуйста, выберите из вариантов: '+",".join(__available_food_sizes)},
        'choose_a_payment_method':{'for_client':'Как вы будете платить?','format':'text','action':"",'error':'Пожалуйста, выберите из вариантов: '+",".join(__available_payment)},
        'confirm_order':{'for_client':'Вы хотите {self.food_size} пиццу, оплата - {self.payment}?','format':'text','action':"",'error':'Вам необходимо написать в чат '+' '.join(__available_confirm)+" чтобы подтвердить заказ"},
        #'cancel_order':{'for_client':'Вы произвели отмену заказа','format':'button','action':"Отменить заказ",'error':'На этом этапе невозможно отменить заказ'},
        'end_order':{'for_client':'Спасибо за заказ','format':'text','action':"",'error':'Напишите /start чтобы начать заново'},
        'new_order':{'for_client':'Новый заказ начат','format':'button','action':"Начать заказ",'error':'На этом этапе невозможно отменить заказ'},
    }
    __initial = 'start'

    def __init__(self):
        self.machine = Machine(model=self,states=PizzaScenario.__states,transitions=PizzaScenario.__transitions,initial=PizzaScenario.__initial,auto_transitions=False,ignore_invalid_triggers=True)
        self.refresh_prop()
    def refresh_prop(self):
        self.payment = None
        self.food_size= None
        self.confirm=False
    def reset(self,message):
        '''Обновление данных'''
        self.payment = None
        self.food_size= None
        self.confirm=False
        self.new_order(message)

    def setted_size(self,message):
        return self.food_size!=None

    def setted_payment(self,message):
        return self.payment!=None
    def confirm_o(self,message):
        return self.confirm
    def order_confirm(self,message):
        '''Подтверждение заказа'''
        text = message.lower().strip()

        if(text in PizzaScenario.__available_confirm):

            self.confirm=True
            return


    def save_size(self,message_text):
        '''Сохранение размера'''
        if(isinstance(message_text,str)):
            text = message_text.lower().strip()
            if(text in  PizzaScenario.__available_food_sizes):
                self.food_size=text

    def save_payment(self,message_text):
        '''Сохранения типа оплаты'''
        if(isinstance(message_text,str)):
            text = message_text.lower().strip()
            if(text in  PizzaScenario.__available_payment):
                self.payment=text


    def get_data_for_view_client(self,text):
        return text.format(self=self)


    def get_next_transitions(self):
        returned_obj = []
        for label, event in self.machine.events.items():
            for event_transitions in event.transitions.values():
                for transition in event_transitions:
                    if(transition.source==self.state):
                        returned_obj.append(label)

        return returned_obj

    def get_next_description(self,labels):
        return {key:PizzaScenario.__view_element.get(key) for key in labels}
