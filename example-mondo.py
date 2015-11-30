import json, pprint
from mondo import MondoClient

pp = pprint.PrettyPrinter(indent = 4)
account = MondoClient()

# Client, secret, account, and password should be stored
# as json in config.json which is loaded here

with open('./config.json') as data_file:    
    config = json.load(data_file)

token = account.token(config['CLIENT'], config['SECRET'], config['ACCOUNT'], config['PASSWORD'])
accessToken = token['access_token']

# get account ID
accountID = account.accounts(accessToken)['accounts'][0]['id']

# get transactions from that account
trx = account.transactions(accessToken, accountID)
# print first transaction
pp.pprint(trx['transactions'][0])

# get more information about that transaction
singleID = trx['transactions'][1]['id']
single = account.transaction(singleID, accessToken)
pp.pprint(single['transaction'])