# -*- coding: utf-8 -*-
from .base import BaseApi

class GroupsAPI(BaseApi):
    
    def has_ou(self, ou_id):
        return self._get('/api_has_ou', ou_id=ou_id)

    def list_group_members(self, key):
        return self._get('/api_list_group_members', key=key)

    def list_org_structure(self):
        return self._get('/api_list_org_structure')

    def list_companies(self):
        return self._get('/api_list_companies')

    def remove_groups(self, key):
        return self._get('/api_remove_groups', key=key)

    def ou_detail(self, ou_id, include_disabled):
        return self._get('/api_get_ou_detail', ou_id=ou_id, include_disabled=include_disabled)

    def add_group_users(self, group_id, user_ids):
        return self._get('/api_add_group_users',group_id=group_id, user_ids=user_ids)

    def remove_group_users(self, group_id, user_ids):
        return self._get('/api_remove_group_users',group_id=group_id, user_ids=user_ids)
