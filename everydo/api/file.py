# -*- coding: utf-8 -*-
from .base import BaseApi

class FileApi(BaseApi):
    
    def get(self, file_id):
        return self._get('/++initd++%s/@@file_info' % file_id)



