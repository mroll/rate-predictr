import base64
import json
from datetime import datetime

import requests

from cost import Cost


def fread(fname):
    with open(fname, 'r') as fp:
        return fp.read()


class LyftClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authfile = 'token.txt'
        self.access_token = None

    def _get_token(self):
        data = {"grant_type": "client_credentials", "scope": "public"}
        authstring = base64.b64encode("{}:{}".format(
            self.client_id, self.client_secret).encode())
        headers = {"Authorization": "Basic {}".format(authstring.decode())}

        token_value = requests.post(
            'https://api.lyft.com/oauth/token',
            data=data,
            headers=headers).json()['access_token']

        return {
            'value': token_value,
            'expiry': int(datetime.now().strftime('%s'))
        }

    def _token_from_authfile(self):
        try:
            filecontents = fread(self.authfile)
            if filecontents == '':
                filecontents = '{}'
            return json.loads(filecontents)
        except FileNotFoundError:
            return {}

    def _authfile_token_value(self):
        return self._token_from_authfile().get('value', None)

    def _authfile_token_expiry(self):
        return self._token_from_authfile().get('expiry', 0)

    def _authfile_is_valid(self):
        if datetime.now() < datetime.fromtimestamp(self._authfile_token_expiry()):
            return True
        return False

    def _renew_auth(self):
        self.access_token = self._get_token()
        with open(self.authfile, 'w') as fp:
            fp.write(json.dumps(self.access_token))

    def _authenticate(self):
        if datetime.now() < datetime.fromtimestamp(self._authfile_token_expiry()):
            return

        if self._authfile_is_valid():
            self.access_token = self._token_from_authfile()
        else:
            self._renew_auth()

    def _make_get_request(self, url, *args, **kwargs):
        self._authenticate()
        return requests.get(
            url,
            params=kwargs,
            headers={'Authorization': 'bearer {}'.format(self._authfile_token_value())}
        )

    def _make_post_request(self, url, *args, **kwargs):
        self._authenticate()
        return requests.post(
            url,
            data=kwargs,
            headers={'Authorization': 'bearer {}'.format(self.access_token)}
        )

    def get_cost(self, *args, **kwargs):
        return Cost(
            **self._make_get_request(
                'https://api.lyft.com/v1/cost',
                *args,
                **kwargs
            ).json()['cost_estimates'][0]
        )
