# Mondo simple python SDK

A simple python SDK for dealing with the Mondo API
It deals with tokens and token refreshing behind the scenes

See the docs https://getmondo.co.uk/docs for details.

1. Download the repository
2. edit the config.json-editMe- 
    enter your API credentials in that file
    (you can also put your account details there as defaults)
3. save / rename it config.json and save in same dir as mondo.py
3. Use the SDK for fun, profit, and global domination

## How do I load the SDK

If you have your API credentials in config.json
and have included your Mondo account email address and password you can just do this:
```
from mondo import MondoClient
account = MondoClient()
```
All of the methods in the class can accept different account details as parameters,
should you open up your app / service to other people, but starting with your own account and 
defaults makes it easy to play with.

You can also specify the default account details to use in the instantiation of MondoClient.
```
account = MondoClient('johnny@apple.com','p4ssw0rd')
```
If that goes well and you don't get any errors...

## What can you do?

* account.get_transactions()
* account.get_transaction()
* account.authenticate()
* account.get_accounts()
* account.get_primary_accountID()
* account.create_feed_item()
* account.register_webhook()

* account.deliver_token()
* account.token_refresh() 

deliver_token() returns a token for handrolling requests and refreshes it when necessary

The methods above all return JSON rather than request objects (the previous version)

Look at the code and https://getmondo.co.uk/docs for information on what parameters to use
to refer to other accounts etc.

## What about tokens and refreshing them?
It's all taken care of.
If a token expires the code will use the refresh call to get a new one

## Example starter code
```
from mondo import MondoClient
account = MondoClient()

print account.get_accounts()
first_account_id =  account.get_accounts()[0]['id']

trx = account.get_transactions(account.get_primary_accountID(), limit=10)
print trx

singleID = trx[1]['id']
single = account.get_transaction(singleID)
print single


account.register_webhook(url='http://mydomain.com/transactions')

webhooks = account.list_webhooks()
first_webhook = webhooks[0]['id']

account.delete_webhook(first_webhook)




```

Todo: 
* Add in the functionality to list and remove webhooks

Evolved from original code by Tito Miguel Costa ( https://bitbucket.org/titomiguelcosta/mondo )

