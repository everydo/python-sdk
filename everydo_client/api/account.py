# -*- coding: utf-8 -*-
from .base import BaseApi

class AccountApi(BaseApi):
    def get_token_info(self, access_token):
        return self._get('/api_get_token_info', access_token=access_token)

    def list_instances(self, rpc, account_name):
        return self._get('/api_list_instances', account_name=account_name, rpc=rpc)

    def remove_user(self, key):
        return self._get('/api_remove_user', key=key)

    def set_allowed_services(self, username, instance_name, services, app_name):
        return self._get('/api_set_allowed_services', username=username, instance_name=instance_name, services=services, app_name=app_name)

    def get_allowed_services(self, username, instance_name, app_name):
        return self._get('/api_get_allowed_services', username=username, instance_name=instance_name, app_name=app_name)

    def remove_ous(self, key):
        return self._get('/api_remove_ous', key=key)

    def set_ldap_config(self, server_address, enable):
        return self._get('/api_set_ldap_config', server_address=server_address, enable=enable)

    def get_ldap_config(self):
        return self._get('/api_get_ldap_config')

    def has_secret_key(self, key):
        return self._get('/api_has_secret_key', key=key)

    
    def password_check(self, key, password):
        return self._get('/api_password_check', key=key, password=password)

    def enable_dynamic_auth(self, uid, key, code):
        return self._get('/api_enable_dynamic_auth', uid=uid, key=key, code=code)

    def disable_dynamic_auth(self, key, code):
        return self._get('/api_disable_dynamic_auth', key=key, code=code)
