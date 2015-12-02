# Mondo simple python SDK

A simple python SDK for dealing with the Mondo API
It deals with tokens and token refreshing behind the scenes
See the docs https://getmondo.co.uk/docs for details.

1. Download the repository
2. edit the config.json-editMe- 
    enter your API credentials in that file
    (you can also put your account details there as defaults)
    rename it config.json
3. Use the SDK for fun and profit

## How do I load the SDK

If you have your API credentials in config.json
and your account email address and password you can just do this:
```
from mondo import MondoClient
account = MondoClient()
```

you can also specify the account details in MondoClient() to access a different account
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

Look at the code and https://getmondo.co.uk/docs for information on what parameters to use

## What about tokens and refreshing them?
It's all taken care of.
If a token expires the code will use the refresh call to get a new one

## Example code
```
from mondo import MondoClient
account = MondoClient()

trx = account.get_transactions(account.get_primary_accountID(), limit=10)
print trx

singleID = trx[1]['id']
single = account.get_transaction(singleID)
print single

# this autorefreshes tokens as needed

```


Evolved from original code by Tito Miguel Costa ( https://bitbucket.org/titomiguelcosta/mondo )

