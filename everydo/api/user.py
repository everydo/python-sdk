# -*- coding: utf-8 -*-
from .base import BaseApi

class UserApi(BaseApi):
   
    def user_info(self, user_id):
        return self._get('/getPrincipalInfo', user_id=user_id)

    def has_user(self, username):
        return self._get('/hasUser', username=username)

    def list_user_groups(self, key):
        return self._get('/listUserGroups', key=key)


    def get_online_users_list(self, account):
        return self._get('/get_online_users_list', account=account)



