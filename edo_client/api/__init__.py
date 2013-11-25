# -*- coding: utf-8 -*-
from .file import FileApi
from .user import UserApi
from .account import AccountApi
from .groups import GroupsAPI
class OCEverydoApi(object):
    @property
    def users(self):
        return UserApi(self, self.access_token, self.refresh_hook)

    @property
    def account(self):
        return AccountApi(self, self.access_token, self.refresh_hook)

    @property
    def groups(self):
        return GroupsAPI(self, self.access_token, self.refresh_hook)

class WOEverydoApi(object):

    @property
    def files(self):
        return FileApi(self, self.access_token, self.refresh_hook)
        

