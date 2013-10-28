# -*- coding: utf-8 -*-
from .base import BaseApi

class GroupsAPI(BaseApi):
    
    def has_ou(self, ou_id):
        return self._get('/hasOU', ou_id=ou_id)

    def list_group_members(self, key):
        return self._get('/listGroupMembers', key=key)

    def list_org_structure(self):
        return self._get('/listOrgStructure')

    def list_companies(self):
        return self._get('/listCompanies')

    def remove_groups(self, key):
        return self._get('/removeGroups', key=key)

    def list_instances(self, vendor_name, account_name, rpc):

        return self._get('/listInstances', vendor_name=str(vendor_name), 
                                    account_name=str(account_name), 
                                    rpc=rpc)


    def ou_info(self, ou_id, include_disabled, skip_cache):

        return self._get('/getOUDetail', ou_id=ou_id, include_disabled=include_disabled, skip_cache=skip_cache)

    def add_group_users(self, group_id, user_ids):

        return self._get('/add_group_users',group_id=group_id, user_ids=user_ids)

    def remove_group_users(self, group_id, user_ids):

        return self._get('/remove_group_users',group_id=group_id, user_ids=user_ids)












