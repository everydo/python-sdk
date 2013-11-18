# -*- coding: utf-8 -*-
from pyoauth2 import AccessToken
from .error import EverydoAPIError, EverydoOAuthError

DEFAULT_START = 0
DEFAULT_COUNT = 20

def check_execption(func):
    def _check(*arg, **kws):
        resp = func(*arg, **kws)
        if resp.status >= 400:
            raise EverydoAPIError(resp)
        try:
            result = eval(resp.parsed)
            # 无错误返回结果
            if not 'token_error' in result:
                return result
            
            self = arg[0]
            if not self.refresh_hook:
                return result

            self.client.refresh_token(self.access_token.refresh_token)
            print self.access_token.token, self.access_token.refresh_token
            if self.refresh_hook:
                self.refresh_hook(self.access_token.token, self.access_token.refresh_token)
            return _check(*arg, **kws)

        except:
            return None
    return _check


class BaseApi(object):
    def __init__(self, client, access_token, refresh_hook):
        self.client = client
        self.refresh_hook = refresh_hook
        self.access_token = access_token
        if not isinstance(self.access_token, AccessToken):
            raise EverydoOAuthError(401, 'UNAUTHORIZED')

    def __repr__(self):
        return '<EverydoAPI Base>'

    @check_execption
    def _get(self, url, **opts):
        return self.access_token.get(url, **opts)

    @check_execption
    def _post(self, url, **opts):
        return self.access_token.post(url, **opts)

    @check_execption
    def _put(self, url, **opts):
        return self.access_token.put(url, **opts)

    @check_execption
    def _patch(self, url, **opts):
        return self.access_token.patch(url, **opts)

    @check_execption
    def _delete(self, url, **opts):
        return self.access_token.delete(url, **opts)
 
