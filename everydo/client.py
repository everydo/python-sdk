# -*- coding: utf-8 -*-
from pyoauth2 import Client, AccessToken
from everydo.api import OCEverydoApi, WOEverydoApi
from everydo.api.base import check_execption 


class EverydoApiClient:

    def __init__(self, key, secret, api_host, redirect=''):
        self.key = key
        self.secret = secret
        self.api_host = api_host
        self.redirect_uri = redirect
        self.client = Client(key, secret,
                       site=self.api_host, 
                       authorize_url=self.api_host + '/@@authorize', 
                       token_url= self.api_host + '/@@access_token')

        self.access_token = None

    def __repr__(self):
        return '<EverydoClient OAuth2>'

    @property
    def authorize_url(self):
        return self.client.auth_code.authorize_url(redirect_uri=self.redirect_uri)

    def auth_with_code(self, code):
        self.access_token = self.client.auth_code.get_token(code, redirect_uri=self.redirect_uri, header_format="Oauth2 %s")

    def auth_with_token(self, token):
        self.access_token = AccessToken(self.client, token, header_format="Oauth2 %s")

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
        access_token = AccessToken(self.client, token='', refresh_token=refresh_token, header_format="Oauth2 %s")
        self.access_token = access_token.refresh()

    def get_account(self):
        client = OCApiClient(self.key, self.secret, self.api_host, self.redirect_uri)
        client.auth_with_token(self.token_code)
        return client

    @check_execption
    def _get(self, url, **opts):
        return self.access_token.get(url, **opts)

    @property
    def list_sites(self):
        return self._get('/list_sites')

    def get_site(self, site_name):
        site = self.list_sites.get(site_name, {})
       	if not site:
            return None

        client = WOApiClient(self.key, self.secret, site['site_url'], self.redirect_uri)
        client.auth_with_token(self.token_code)
        return client

class OCApiClient(OCEverydoApi):
    def __init__(self, key, secret, api_host, redirect=''):
        self.redirect_uri = redirect
        self.client = Client(key, secret,
                       site=api_host, authorize_url='', token_url='')
        self.access_token = None

    def __repr__(self):
        return '<OCClient OAuth2>'

    def auth_with_token(self, token):
        self.access_token = AccessToken(self.client, token, header_format="Oauth2 %s")

    @property
    def token_code(self):
        return self.access_token and self.access_token.token

class WOApiClient(WOEverydoApi):
    def __init__(self, key, secret, api_host, redirect=''):
        self.redirect_uri = redirect
        self.client = Client(key, secret,
                       site=api_host, authorize_url='', token_url='')
        self.access_token = None

    def __repr__(self):
        return '<WOClient OAuth2>'

    def auth_with_token(self, token):
        self.access_token = AccessToken(self.client, token, header_format="Oauth2 %s")

    @property
    def token_code(self):
        return self.access_token and self.access_token.token



if __name__ == '__main__':
    args = {'key': '',
            'secret': '',
            'api_host' : '',
            'redirect' : ''}
    # 初始化输入参数
    edo_api = EverydoApiClient(**args)
    print edo_api.authorize_url

    code = input('input the code')
    # 通过code获取access_token
    edo_api.auth_with_code(str(code))

    # 获取oc的API操作对象
    oc_api = edo_api.get_account()



    # 特定站点的API操作对象
    wo_api = edo_api.get_site('default')

    # 调用特定的API
    file_info = wo_api.files.file_info(file_id=9284298392)

