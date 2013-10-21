# -*- coding: utf-8 -*-
from .file import FileApi

class OCEverydoApi(object):
    pass

class WOEverydoApi(object):

    @property
    def files(self):
        return FileApi(self.access_token)

