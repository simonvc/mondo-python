import requests
import json

API_ERRORS = {
    400: "400: Bad Req. Your request has missing parameters or is malformed",
    401: "401: Unauthorized. Your request is not authenticated.",
    403: "403: Forbidden. Your request is authenticated \
          but has insufficient permissions.",
    405: "405: Method Not Allowed. You are using the incorrect HTTP verb. \
        Double check whether it should be POST/GET/DELETE/etc.",
    404: "404: Page Not Found. The endpoint requested does not exist.",
    406: "406: Not Acceptable. Your application does not accept the content \
        format returned according to the Accept headers sent in the request.",
    429: "425: Too Many Requests. Your application is exceeding its rate limit. \
          Back off, buddy.",
    500: "500: Internal Server Error. Something is wrong on our end. Whoopsie",
    504: "504 - Gateway Timeout Something has timed out on our end. Whoopsie"
}

class MondoClient():
    """
    Create a client connection and get the token for a specific account
    using either data in config.json or an account email / password in the class call
    e.g. connection = MondoClient('johnny@apple.com', 'passw0rd') or
    connection = MondoClient() - which uses info from config.json
    """
    url = 'https://production-api.gmon.io/'

    def __init__(self, account_id=None, acc_password=None, url=None):
        if url is not None:
            self.url = url

        # grab the access token on instantiating the class
        # Using config.json to supply client, secret
        # ... and optionally account & password
        try:
            with open('./config.json') as data_file:
                config = json.load(data_file)
        except IOError:
            raise Exception('No config.json file found')

        try:
            self.client = config['client']
            self.secret = config['secret']
        except KeyError:
            raise Exception('define client / secret in config.json')

        if account_id is None:
            if 'account' in config:
                self.account = config['account']
            else:
                raise Exception('No account email supplied')
        else:
            self.account = account_id

        if acc_password is None:
            if 'password' in config:
                self.password = config['password']
            else:
                raise Exception('No account password supplied')
        else:
            self.password = acc_password

        try:
            token_response = self.get_token()
            self.token = token_response['access_token']
            self.refresh_token = token_response['refresh_token']
            self.token_expires = token_response['expires_in']
        except TypeError:
            raise Exception(token_response)

    def get_token(self, client_id=None, client_secret=None,
                  username=None, password=None):
        """
        Acquire an access token - uses config.JSON file for data by default
        """
        if client_id is None:
            client_id = self.client
        if client_secret is None:
            client_secret = self.secret
        if username is None:
            username = self.account
        if password is None:
            password = self.password

        payload = {'grant_type': 'password',
                   'client_id': client_id,
                   'client_secret': client_secret,
                   'username': username,
                   'password': password}
        r = requests.post(self.url + '/oauth2/token', payload)

        if r.status_code == 200:
            response = r.json()
            self.token = response['access_token']
            self.refresh_token = response['refresh_token']
            return response
        else:
            return (API_ERRORS[r.status_code], r.json())

    def refresh_access_token(self, client_id=None, client_secret=None,
                             refresh_token=None):
        """
        Refresh a previously acquired token
        use config.json data by default
        """

        if client_id is None:
            client_id = self.client
        if client_secret is None:
            client_secret = self.secret
        if refresh_token is None:
            refresh_token = self.refresh_token

        payload = {'grant_type': 'refresh_token',
                   'client_id': client_id,
                   'client_secret': client_secret,
                   'refresh_token': refresh_token}
        r = requests.post(self.url + '/oauth2/token', payload)

        if r.status_code == 200:
            response = r.json()
            self.token = response['access_token']
            self.refresh_token = response['refresh_token']
            return response
        else:
            return (API_ERRORS[r.status_code], r.json())

    def get_transaction(self, transaction_id, access_token=None, merchant=True):
        """
        Get details about a transaction
        Uses config.json secrets by default
        """

        if access_token is None:
            access_token = self.token

        headers = {'Authorization': 'Bearer ' + access_token}
        params = {}

        if merchant:
            params['expand[]'] = 'merchant'

        r = requests.get(self.url + '/transactions/' + transaction_id,
                         params=params, headers=headers)

        if r.status_code == 200:
            return r.json()['transaction']
        else:
            return (API_ERRORS[r.status_code], r.json)

    def get_transactions(self, account_id, limit=100, since=None,
                         before=None, access_token=None):
        """
        List transactions
        """

        if access_token is None:
            access_token = self.token

        headers = {'Authorization': 'Bearer ' + access_token}
        params = {'limit': limit, "account_id": account_id}

        if since is not None:
            params['since'] = since
        if before is not None:
            params['before'] = before

        r = requests.get(self.url + '/transactions',
                         params=params, headers=headers)

        if r.status_code == 200:
            return r.json()['transactions']
        else:
            return (API_ERRORS[r.status_code], r.json())

    def authenticate(self, access_token=None, client_id=None, user_id=None):
        """
        authenticate user
        """

        if access_token is None:
            access_token = self.token
        if client_id is None:
            client_id = self.client
        if user_id is None:
            user_id = self.account

        headers = {'Authorization': 'Bearer ' + str(access_token)}
        r = requests.get(self.url + '/ping/whoami', headers=headers)

        if r.status_code == 200:
            return r.json()
        else:
            return (API_ERRORS[r.status_code], r.json())

    def get_accounts(self, access_token=None):
        """
        detailed information about customer's accounts
        uses config.json data by default
        """
        if access_token is None:
            access_token = self.token

        headers = {'Authorization': 'Bearer ' + access_token}

        r = requests.get(self.url + '/accounts', headers=headers)

        if r.status_code == 200:
            return r.json()['accounts']
        else:
            return (API_ERRORS[r.status_code], r.json())

    def get_primary_accountID(self, access_token=None):
        """
        Get ID from the first account listed against an access token
        """

        if access_token is None:
            access_token = self.token

        headers = {'Authorization': 'Bearer ' + access_token}

        r = requests.get(self.url + '/accounts', headers=headers)

        if r.status_code == 200:
            return r.json()['accounts'][0]['id']
        else:
            return (API_ERRORS[r.status_code], r.json())

    def create_feed_item(self, access_token, account_id, title, image_url,
                         background_color='#FCF1EE', body_color='#FCF1EE',
                         title_color='#333', body=''):
        """
        publish a new feed entry
        """
        headers = {'Authorization': 'Bearer ' + access_token}

        payload = {
            "account_id": account_id,
            "type": "basic",
            "params[title]": title,
            "params[image_url]": image_url,
            "params[background_color]": background_color,
            "params[body_color]": body_color,
            "params[title_color]": title_color,
            "params[body]": body
        }

        r = requests.post(self.url + '/feed', data=payload, headers=headers)

        if r.status_code == 200:
            return r.json()
        else:
            return (API_ERRORS[r.status_code], r.json())

    def register_webhook(self, account_id, url, access_token):
        """
        register a webhook
        instance.register_webhook(account_id, url, [access_token])
        """
        if access_token is None:
            access_token = self.token

        headers = {'Authorization': 'Bearer ' + access_token}
        payload = {"account_id": account_id, "url": url}

        r = requests.post(self.url + '/feed', data=payload, headers=headers)

        if r.status_code == 200:
            return r.json()
        else:
            return (API_ERRORS[r.status_code], r.json())
