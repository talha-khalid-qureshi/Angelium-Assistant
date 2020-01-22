from chatterbot import ChatBot,response_selection
from chatterbot.trainers import ListTrainer,ChatterBotCorpusTrainer
import logging,datetime
from chatterbot.comparisons import levenshtein_distance,JaccardSimilarity,sentiment_comparison

from .RatcliffObershelp import ratcliffobershelp
from chatterbot.logic import LogicAdapter,DepositWithdrawAdapter
from chatterbot.conversation import Statement
import logging
logging.basicConfig(filename='sora_bot.log',level=logging.INFO)

#from chatterbot.logic.DepositWithdrawAdapter import DepositWithdraw
import chatterbot

action = ""
currency_type = ""
currency = ""
currency_list = ['anx','bitcoin','btc','usdt','eth','etherium']
action_list = ['to xchange','to exchange','from exchange','from xchange','to wallet','from wallet']
d_response=["i am in beta version, i don't know a lot.",
            "Maybe you can ask something else.",
            "i am sorry but i didn't really get your point."]

chat_bot = ChatBot(
    'Angelium',
    read_only=True,
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.convert_to_ascii',
        'chatterbot.preprocessors.unescape_html'
    ],
    logic_adapters=[
       {
           'import_path':'chatterbot.logic.DepositWithdrawAdapter.DepositWithdraw'},
            {
               'import_path' : 'chatterbot.logic.BestMatch',
                'statement_comparison_function' : ratcliffobershelp,
                "response_selection_method": response_selection.get_random_response,
                "default_response":d_response,
                "maximum_similarity_threshold":0.80,
            },
            
    ]
)
trainer = ChatterBotCorpusTrainer(chat_bot)


def train_data():
    trainer = ChatterBotCorpusTrainer(chat_bot)
    trainer.train('/home/angelium/dev/AI-API/my-api/aiapi/utility/Data_1.1.yml')
    print("training completed")

#train_data()


def is_balance(text):
	words = ['my', 'balance']
	if all(x in text.split() for x in words):
		return True
	else:
		return False

def final_response(text):
    global action,currency,currency_type
    text = str(text.lower())
    if is_balance(text):
        return "Your total balance is $##TOTAL_BALANCE##"

    else :
        response = chat_bot.get_response(text)
        try:
            print('In Try Block :',response)
            Dict = eval(str(response))
            print('eval Evaluated')
            print(Dict)
            if Dict['action'] == '':
                return "Where do you want to transfer?\n [to Wallet |to Xchange]"
            elif Dict['action']== 'invalid-response':
                return 'Invalid Key Entered against Action '
            
            if Dict['currency_type'] == '':
                # currency_type = Dict['currency_type']
                print('in currency_type')
                return "Which currency you would like to transfer \nANX \nBTC \nUSDT \nETH"
            elif Dict['currency_type']== 'invalid-response':
                return 'Invalid Currency Type Entered'

            if Dict['currency'] == '':
                a = "How much %s would you like to transfer "%(Dict['currency_type'])
                return a
            elif Dict['currency']== 'invalid-response':
                return 'Invalid Currency Entered'
            
            if (Dict['action'] != '') and (Dict['currency_type'] != '') and (Dict['currency'] != '') and (Dict['final_result'] == 'may-interested'):
                print('every thing found')
                a = "We are transfering %s %s %s \n Are you sure to proceed [Yes/No] "%(Dict['currency'],Dict['currency_type'],Dict['action'])
                print('every thing found %s %s %s'%(Dict['currency'],Dict['currency_type'],Dict['action']))
                return a
            

            if (Dict['action'] != '') and (Dict['currency_type'] != '') and (Dict['currency'] != '') and (Dict['final_result'] == 'interested'):
                b = ("We have transfered {0} {1} {2} \n ######Hun MOja'n Karo #######] ".format(Dict['currency'],Dict['currency_type'],Dict['action']))
                return b
            elif (Dict['action'] != '') and (Dict['currency_type'] != '') and (Dict['currency'] != '') and (Dict['final_result'] == 'not-interested'):
                b = "No problem, Let me know if you change your mind"
                return b
    
        except:
           # print('Evaluating Response of except {0} now'.format(response))
            print('eval not Evaluated')
            return response



def exporting_data():
	trainer.export_for_training('./{}export.json'.format(datetime.datetime.now()))
