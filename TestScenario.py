from ScenarioForBot import PizzaScenario
from telebot import types
def to_next_step_transition(current_user,message):
    next_trans_label = current_user.get_next_transitions()
    next_trans_desc  = current_user.get_next_description(next_trans_label)
    button_data=list(filter(lambda x: x['format']=='button',next_trans_desc.values()))
    updated = False
    for button in button_data:
        if(button['action']==message):

            try:
                key = get_key(next_trans_desc,button)

                trig = current_user.trigger(key,message)
                if( trig):
                    if_next_step_transition(current_user,message)
                    updated = True
                    break
            except Exception as e:
                print('error1 ', e)
    text_data = list(filter(lambda x: x['format']=='text',next_trans_desc.values()))
    if not updated:
        for data in text_data:

            try:

                key = get_key(next_trans_desc,data)
                trig = current_user.trigger(key,message)
                if( trig):
                    if_next_step_transition(current_user,message)
                    updated = True
                    break
            except Exception as e:
                print('error2 ', e)
            if not updated:
                print("Бот отправит: ", data['error'])
def if_next_step_transition(current_user,message):
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
            #print(button)
            reply_markup.add(types.KeyboardButton(button.get('action')))
            actions_text.append(current_user.get_data_for_view_client(button['for_client']))
    if(len(sendet_text)==0):
        if len(actions_text)>0:
            sendet_text+=actions_text
    print("Бот отправил: ",sendet_text,reply_markup)
def get_key(my_dict,val):

    for key, value in my_dict.items():
        if val == value:
            return key
    raise Exception("key doesn't exist")
client = PizzaScenario.generate_scenario()
print("При подключении к боту отправляется /start")
if_next_step_transition(client,'/start')
print('Пользователь отвечает Большую')
to_next_step_transition(client,'Большую')
print('Пользователь отвечает Наличкой')
to_next_step_transition(client,'Наличкой')
print('Пользователь отвечает Да')
to_next_step_transition(client,'Да')
