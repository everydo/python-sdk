# -*- coding: utf-8 -*-
from pyoauth2 import Client, AccessToken
from everydo_client.api import OCEverydoApi, WOEverydoApi

class EverydoClient(OCEverydoApi):

    def __init__(self, key, secret, api_host, redirect='', refresh_hook=None):
        self.key = key
        self.secret = secret
        self.api_host = api_host
        self.redirect_uri = redirect
        self.refresh_hook = refresh_hook
        self.client = Client(key, secret,
                       site=self.api_host, 
                       authorize_url=self.api_host + '/@@authorize', 
                       token_url= self.api_host + '/@@access_token')

        self.access_token = None
        self.sites = []
    def __repr__(self):
        return '<EverydoClient OAuth2>'

    @property
    def authorize_url(self):
        return self.client.auth_code.authorize_url(redirect_uri=self.redirect_uri)

    def auth_with_code(self, code):
        self.access_token = self.client.auth_code.get_token(code, redirect_uri=self.redirect_uri)

    def auth_with_token(self, token, refresh_token=''):
        self.access_token = AccessToken(self.client, token=token, refresh_token=refresh_token)

    def auth_with_password(self, username, password, **opt):
        self.access_token = self.client.password.get_token(username=username,
                                 password=password, redirect_uri=self.redirect_uri, **opt)
        print self.token_code

    def list_sites(self):
        instances = self.account.list_instances()
        sites = []
        for app in instances.values():
            for name, value in app.items():
                value['name'] = name
                sites.append(value)
        return sites

    @property
    def token_code(self):
        return getattr(self.access_token, 'token', None)

    @property
    def refresh_token_code(self):
        return getattr(self.access_token, 'refresh_token', None)

    def refresh_token(self, refresh_token):
        access_token = AccessToken(self.client, token='', refresh_token=refresh_token)
        self.access_token = access_token.refresh()

    def get_site(self, site_name):
        if not self.sites:
            self.sites = self.list_sites()

        for site in self.sites:
            if site['name'] == site_name:
                client = WOApiClient(self.key, self.secret, site['url'], authorize_url=self.api_host + '/@@authorize', 
                                     token_url= self.api_host + '/@@access_token', redirect=self.redirect_uri)
                client.auth_with_token(self.token_code)
                return client

class WOApiClient(WOEverydoApi):
    def __init__(self, key, secret, api_host, authorize_url, token_url, redirect=''):
        self.redirect_uri = redirect
        self.client = Client(key, secret,
                       site=api_host, authorize_url=authorize_url, token_url=token_url)
        self.access_token = None

    def __repr__(self):
        return '<WOClient OAuth2>'

    def auth_with_token(self, token):
        self.access_token = AccessToken(self.client, token)

    @property
    def token_code(self):
        return self.access_token and self.access_token.token



if __name__ == '__main__':

    # ===========================================================================================
    # 新用户授权
    # ===========================================================================================
    args = {'key': '',
            'secret': '',
            'api_host' : '',
            'redirect' : ''}
    # 初始化输入参数
    edo_api = EverydoClient(**args)
    print edo_api.authorize_url

    code = input('input the code')
    # 通过code获取access_token
    edo_api.auth_with_code(str(code))


def save(token, refresh_token):
    print token, refresh_token

