# -*- coding: utf-8 -*-
from .file import FileApi
from .user import UserApi
from .account import AccountApi
from .groups import GroupsAPI
class OCEverydoApi(object):
    @property
    def users(self):
        return UserApi(self.access_token)

    @property
    def account(self):
        return AccountApi(self.access_token)

    @property
    def groups(self):
        return GroupsAPI(self.access_token)
    
class WOEverydoApi(object):

    @property
    def files(self):
        return FileApi(self.access_token)

