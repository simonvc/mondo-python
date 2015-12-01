import requests
import json


class MondoClient():
    url = 'https://production-api.gmon.io/'

    def __init__(self, url=None):
        if url is not None:
            self.url = url

        # grab the access token on instantiating the class
        # Using config.json to supply CLIENT, SECRET, ACCOUNT, PASSWORD
        try:
            with open('./config.json') as data_file:
                config = json.load(data_file)
            try:
                self.CLIENT = config['CLIENT']
                self.SECRET = config['SECRET']
                self.ACCOUNT = config['ACCOUNT']
                self.PASSWORD = config['PASSWORD']

                token_response = MondoClient.get_token(self)
                self.token = token_response['access_token']
                self.refresh_token = token_response['refresh_token']
                self.token_expires = token_response['expires_in']
            except KeyError:
                raise Exception('define secret keys in config.json')
        except IOError:
            raise Exception('No config.json file found')

    def get_token(self, client_id=None, client_secret=None,
                  username=None, password=None):
        """
        Acquire an access token - uses config.JSON file for data by default
        get_token(client_ID, client_secret, username, password)
        """
        if client_id is None:
            client_id = self.CLIENT
        if client_secret is None:
            client_secret = self.SECRET
        if username is None:
            username = self.ACCOUNT
        if password is None:
            password = self.PASSWORD

        payload = {'grant_type': 'password',
                   'client_id': client_id,
                   'client_secret': client_secret,
                   'username': username,
                   'password': password}
        r = requests.post(self.url + '/oauth2/token', payload)

        return r.json()

    def refresh_token(self, client_id=None, client_secret=None,
                      refresh_token=None):
        """
        Refresh a previously acquired token
        use config.json data by default
        refresh_token(client_id, client_secret, refresh_token)
        """

        if client_id is None:
            client_id = self.CLIENT
        if client_secret is None:
            client_secret = self.SECRET
        if refresh_token is None:
            refresh_token = self.refresh_token

        payload = {'grant_type': 'refresh_token',
                   'client_id': client_id,
                   'client_secret': client_secret,
                   'refresh_token': refresh_token}
        r = requests.post(self.url + '/oauth2/token', payload)

        return r.json()

    def transaction(self, account_id, access_token=None, merchant=True):
        """
        Get details about a transaction
        Uses config.json secrets by default
        transaction(id, access_token, merchant)
        """

        if access_token is None:
            access_token = self.token

        headers = {'Authorization': 'Bearer ' + access_token}
        params = {}

        if merchant:
            params['expand[]'] = 'merchant'

        r = requests.get(self.url + '/transactions/' + account_id,
                         params=params, headers=headers)

        return r.json()

    def transactions(self, account_id, limit=100, since=None,
                     before=None, access_token=None):
        """
        List transactions
        transactions(account_id,[limit],[since],[before],[token])
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

        return r.json()

    def authenticate(self, access_token=None, client_id=None, user_id=None):
        """
        authenticate user
        """

        if access_token is None:
            access_token = self.token
        if client_id is None:
            client_id = self.CLIENT
        if user_id is None:
            user_id = self.ACCOUNT

        headers = {'Authorization': 'Bearer ' + str(access_token)}

        r = requests.get(self.url + '/ping/whoami', headers=headers)

        return r.json()

    def accounts(self, access_token=None):
        """
        detailed information about customer's accounts
        uses config.json data by default
        accounts(access_token)
        """
        if access_token is None:
            access_token = self.token

        headers = {'Authorization': 'Bearer ' + access_token}

        r = requests.get(self.url + '/accounts', headers=headers)

        return r.json()

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

        return r

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

        return r

