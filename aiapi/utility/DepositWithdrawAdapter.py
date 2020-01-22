from chatterbot.logic import LogicAdapter
import random
from chatterbot.conversation import Statement

action = ""
currency_type = ""
currency = ""
final_result = 'not-sure'
check_flag = False

class DepositWithdraw(LogicAdapter):
    
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
    
    # Only Run when User Enter Exchange related Text

    def can_process(self, statement):
        check_list = ['deposit','transfer', 'change','withdraw']
        statement = statement.text
        # print('i am inside class -> can_process')
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
           
            # print('Currency from RE : ',total_amount)
            return total_amount
               
        except IndexError:
            try:
                # Get Numerical Data from String
                from word2number import w2n
                total_amount = w2n.word_to_num(selected_statement)
                # print('Currency from w2n : ',total_amount)
                return total_amount
            except:
                total_amount = ''
                return total_amount


    def process(self, input_statement, additional_response_selection_parameters):      

        global check_flag,final_result
        global action,currency_type,currency
        
        selected_statement = input_statement.text
        temp_action,temp_currency_type,temp_currency = '','',''
        currency_list = ['anx','bitcoin','btc','usdt','eth','etherium']
        action_list = ['to xchange','to exchange','from exchange','from xchange','to wallet','from wallet']
        temp_action,temp_currency_type,temp_currency = '','',''

        if final_result == 'interested':
            final_result = 'not-sure'
            action = ''
            currency = ''
            currency_type = ''
       
        temp_action = self.check_from_list(selected_statement,action_list)
        if (action == '') and (temp_action != ''):
            action = temp_action
        elif (action != '') and (temp_action != ''):
            action = 'invalid-response'
            
        
        temp_currency_type = self.check_from_list(selected_statement,currency_list)
        if (currency_type == '') and temp_currency_type != '':
            currency_type = temp_currency_type
        elif (currency_type != '') and (temp_currency_type != ''):
            currency_type = 'invalid-response'
        
        temp_currency = self.get_cardinal(selected_statement)
        if (currency == '') and temp_currency != '':
            currency = temp_currency
        elif (currency != '') and (temp_currency != ''):
            currency = 'invalid-response'

        if (action == "") or (currency_type == "") or (currency == ""):
            print('Variable abi empty hain')
            check_flag =True

        if (action != '') and (currency_type != '') and (currency != '') and (final_result== 'not-sure') or (final_result== 'not-interested'):
            final_result = 'may-interested'
            check_flag = True

        elif (action != '') and (currency_type != '') and (currency != '') and (final_result == 'may-interested'):
            
            if selected_statement in ['yes','sure','y','ok']:
                final_result = 'interested'
            else :
                final_result = 'not-interested'
                    
            check_flag = False    
    
        response_statement = {
                        'action' : action,
                        'currency_type': currency_type,
                        'currency': currency,
                        'final_result' : final_result
                    }
        print('Response from Adapter Direct ' ,response_statement)
        confidence = 1.0 
        text = Statement(str(response_statement),confidence)
        
     #   logging.info('results : %s ',response_statement)
        return  text


#another_v13.final_response('please transfer 10 btc to wallet')