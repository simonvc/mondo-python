import requests

class MondoClient():
    url = 'https://production-api.gmon.io/'

    def __init__(self, url = None):
        if url != None:
            self.url = url

    def token(self, client_id, client_secret, username, password):
        """
        Acquiring an access token
        """
        payload = {'grant_type': 'password', 'client_id': client_id, 'client_secret': client_secret, 'username': username, 'password': password }
        r = requests.post(self.url + '/oauth2/token', payload)

        return r.json()

    def refresh_token(self, client_id, client_secret, refresh_token):
        """
        Refreshing a proviously acquired token
        """
        payload = {'grant_type': 'refresh_token', 'client_id': client_id, 'client_secret': client_secret, 'refresh_token': refresh_token }
        r = requests.post(self.url + '/oauth2/token', payload)

        return r.json()

    def transaction(self, id, access_token, merchant = True):
        """
        Getting details about a transaction
        """
        headers = {'Authorization': 'Bearer ' + access_token}
        params = {}

        if merchant:
            params['expand[]'] = 'merchant'

        r = requests.get(self.url + '/transactions/' + id, params=params, headers=headers)

        return r.json()

    def transactions(self, access_token, account_id, limit = 100, since = None, before = None):
        """
        List transactions
        """
        headers = {'Authorization': 'Bearer ' + access_token}
        params = {'limit': limit, "account_id": account_id}

        if since != None:
            params['since'] = since

        if before != None:
            params['before'] = before

        r = requests.get(self.url + '/transactions', params=params, headers=headers)

        return r.json()

    def authenticate(self, access_token, client_id, user_id):
        """
        authenticate user
        """
        headers = {'Authorization': 'Bearer ' + str(access_token)}

        r = requests.get(self.url + '/ping/whoami', headers=headers)

        return r.json()

    def accounts(self, access_token):
        """
        detailed information about customer's accounts
        """
        headers = {'Authorization': 'Bearer ' + access_token}

        r = requests.get(self.url + '/accounts', headers=headers)

        return r.json()

    def create_feed_item(self, access_token, account_id, title, image_url, background_color = '#FCF1EE', body_color = '#FCF1EE', title_color = '#333', body = ''):
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

    def register_webhook(self, access_token, account_id, url):
        """
        registering a webhook
        """
        headers = {'Authorization': 'Bearer ' + access_token}
        payload = {"account_id": account_id, "url": url}

        r = requests.post(self.url + '/feed', data=payload, headers=headers)

        return r
