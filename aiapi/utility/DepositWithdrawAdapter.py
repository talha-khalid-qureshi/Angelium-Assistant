import sys,logging
logging.basicConfig(filename='sora_transaction_bot.log',level=logging.INFO)
from chatterbot.logic import LogicAdapter
import random
from chatterbot.conversation import Statement

action = ""
currency_type = ""
currency = ""
final_result = 'not-sure'
check_flag = False
variable_flag = False
a_flag,c_flag,ct_flag = False,False,False
v_flag=-1

class DepositWithdraw(LogicAdapter):
    
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
    
    # Only Run when User Enter Exchange related Text

    def can_process(self, statement):
        check_list = ['deposit','transfer', 'change','withdraw']
        statement = statement.text
        if check_flag == True:
            return True
        elif check_flag == False:
            for i in check_list:
                    if i in statement and ('how' not in statement) and ('fees' not in statement) and ('not' not in statement):
                #     logging.info('%s is processabel in depossit/withdraw module',statement)
                        return True
        else:
            return False

    def check_from_list(self,selected_statement,list_values):
        for i in list_values:
            if i in selected_statement:
                return i
        return ''


    def get_cardinal(self,selected_statement):
        try:
            import re
            total_amount = re.findall(r"[-+]?\d*\.\d+|\d+", selected_statement)[0]
            return total_amount
               
        except IndexError:
            try:
                # Get Numerical Data from String
                from word2number import w2n
                total_amount = w2n.word_to_num(selected_statement)
                return total_amount
            except:
                total_amount = ''
                return total_amount


    def process(self, input_statement, additional_response_selection_parameters):      

        global check_flag,final_result,variable_flag
        global action,currency_type,currency
        global v_flag
        
        selected_statement = input_statement.text

        temp_action,temp_currency_type,temp_currency = '','',''
        currency_list = ['anx','bitcoin','btc','usdt','eth','etherium']
        action_list = ['to xchange','to exchange','from exchange','from xchange','to wallet','from wallet']
        another_actionlist = ['wallet','walet','xchange','exchange','x-change','ex-change']

        if final_result == 'interested':
            final_result = 'not-sure'
            action = ''
            currency = ''
            currency_type = ''
            v_flag = -1
        
        if (action == 'invalid-response') or (currency_type == 'invalid-response') or (currency == 'invalid-response'):
            print('i entered in invalid wali jgah')
            action = ''
            currency = ''
            currency_type = ''
            final_result = 'not-sure'
            v_flag = -1
       
        if v_flag==-1:
            temp_action = self.check_from_list(selected_statement,action_list)
            if action == '':
                action = temp_action

            temp_currency_type = self.check_from_list(selected_statement,currency_list)
            if currency_type == '':
                currency_type = temp_currency_type
            
            temp_currency = self.get_cardinal(selected_statement)
            if currency == '' :
                currency = temp_currency
        
        if v_flag == 0 :
            
            temp_action = self.check_from_list(selected_statement,another_actionlist)
            if (action == '') and (temp_action!=''):
                action = 'to ' + temp_action
             #   action = temp_action
            
            elif (action =='') and (temp_action == ''):
                action = 'invalid-response'
                check_flag = False
        
        if v_flag ==1:
            temp_action = self.check_from_list(selected_statement,another_actionlist)
            if (action == '') and (temp_action!=''):
                action = 'to ' + temp_action
              #  action = temp_action

            elif (action != '') and (temp_action == ''):

                temp_currency_type = self.check_from_list(selected_statement,currency_list)
                if (currency_type == '') and (temp_currency_type!=''):
                    currency_type = temp_currency_type
                    check_flag = True
                elif (currency_type!='') and (temp_currency_type!=''):
                    currency_type = 'invalid-response'
                    check_flag = False
                elif (currency_type!='') and (temp_currency_type==''):
                    temp_currency = self.get_cardinal(selected_statement)
                    if (currency=='') and (temp_currency !=''):
                        currency = temp_currency
                        check_flag = True
                    elif (currency=='') and (temp_currency==''):
                        currency = 'invalid-response'
                        check_flag =False
                    elif (currency!='') and (temp_currency!=''):
                        currency = 'invalid-response'
                        check_flag =False

                elif (currency_type=='') and (temp_currency_type==''):
                    currency_type = 'invalid-response'
                    check_flag = False

            elif (action != '') and (temp_action != ''):
                action = 'invalid-response'
                check_flag = False
            
            elif (action =='') and (temp_action == ''):
                action = 'invalid-response'
                check_flag = False
        
        if (action== '') and (currency_type== '') and (currency == ''):
            v_flag = 0      # all are empty
            check_flag = True

        if (action=='') or (currency_type == '') or (currency == ''):
            check_flag = True
            v_flag = 1      # someone empty
        
        print('before entering final_result - >',final_result)
        if (action != '') and (currency_type != '') and (currency != '') and (final_result== 'not-sure'):
            v_flag = 2
            print('enter in not sure')
            final_result = 'may-interested'
            check_flag = True

        elif (action != '') and (currency_type != '') and (currency != '') and (final_result== 'not-interested'):
            print('enter in may-interested')
            v_flag = 2
            final_result = 'may-interested'
            check_flag = True

        elif (action != '') and (currency_type != '') and (currency != '') and (final_result == 'may-interested'):
            
            if selected_statement in ['yes','sure','y','ok']:
                print('enter in interested')
                final_result = 'interested'
            else :
                print('enter in not interested')
                final_result = 'not-interested'
            check_flag = False    

        print('After entering final_result - >',final_result)
        if (action == 'invalid-response') or (currency_type == 'invalid-response') or (currency == 'invalid-response'):
            print('invalid may aya wa hn')
            check_flag = False

        response_statement = {
                        'action' : action,
                        'currency_type': currency_type,
                        'currency': currency,
                        'final_result' : final_result
                    }
        print('Response from Adapter Direct ' ,response_statement)
        print('flag value ',v_flag)
        confidence = 1.0 
        text = Statement(str(response_statement),confidence)
        
        return  text

