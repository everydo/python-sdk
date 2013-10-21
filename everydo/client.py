# -*- coding: utf-8 -*-
from pyoauth2 import Client, AccessToken
from api import OCEverydoApi, WOEverydoApi
from api.base import check_execption 


class AccountApiClient:

    def __init__(self, key, secret, api_host, redirect=''):
        self.key = key
        self.secret = secret
        self.api_host = api_host
        self.redirect_uri = redirect
        self.client = Client(key, secret,
                       site=self.api_host, authorize_url=self.api_host + '/authorite', token_url= self.api_host + '/access_token')
        self.access_token = None

    def __repr__(self):
        return '<EverydoClient OAuth2>'

    @property
    def authorize_url(self):
        return self.client.auth_code.authorize_url(redirect_uri=self.redirect_uri)

    def auth_with_code(self, code):
        self.access_token = self.client.auth_code.get_token(code, redirect_uri=self.redirect_uri)

    def auth_with_token(self, token):
        self.access_token = AccessToken(self.client, token)

    def auth_with_password(self, username, password, **opt):
        self.access_token = self.client.password.get_token(username=username,
                                 password=password, redirect_uri=self.redirect_uri, **opt)

    @property
    def token_code(self):
        return self.access_token and self.access_token.token

    @property
    def refresh_token_code(self):
        return getattr(self.access_token, 'refresh_token', None)

    def refresh_token(self, refresh_token):
        access_token = AccessToken(self.client, token='', refresh_token=refresh_token)
        self.access_token = access_token.refresh()

    def get_account(self):
        client = OCApiClient(self.key, self.secret, self.api_host, self.redirect)
        client.auth_with_token(self.token_code)
        return client

    @check_execption
    def _get(self, url, **opts):
        return self.access_token.get(url, **opts)


    def list_sites(self):
        return self._get('list_sites')

    def get_site(self, site_name):
        site = self.list_sites.get(site_name, {})
        if not site.get(site_name):
            return None
        
        return OCApiClient(self.key, self.secret, site.get(site_name)['api_url'], self.redirect)

class OCApiClient(OCEverydoApi):
    def __init__(self, key, secret, redirect=''):
        self.redirect_uri = redirect
        self.client = Client(key, secret,
                       site=self.API_HOST, authorize_url=self.AUTHORIZE_URL, token_url=self.TOKEN_URL)
        self.access_token = None

    def __repr__(self):
        return '<OCClient OAuth2>'

    def auth_with_token(self, token):
        self.access_token = AccessToken(self.client, token)

    @property
    def token_code(self):
        return self.access_token and self.access_token.token

class WOApiClient(WOEverydoApi):
    def __init__(self, key, secret, redirect=''):
        self.redirect_uri = redirect
        self.client = Client(key, secret,
                       site=self.API_HOST, authorize_url=self.AUTHORIZE_URL, token_url=self.TOKEN_URL)
        self.access_token = None

    def __repr__(self):
        return '<WOClient OAuth2>'

    def auth_with_token(self, token):
        self.access_token = AccessToken(self.client, token)

    @property
    def token_code(self):
        return self.access_token and self.access_token.token


