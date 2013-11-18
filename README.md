=======
python-sdk
==========

python SDK for everydo.com

安装：

    pip install everydo


使用示范：
 
    from everydo_client import EverydoClient

    def refresh_hook(new_ticket):
        # TODO: save the new ticket
        pass

    client = EverydoClient(API_KEY, API_SECRET, server_uri, refresh_hook)

    # 基于username/password登录（获取ticket）
    client.login(username=‘zope.system’, passowrd="")
    client.org_info.get_pricipal_info(pid)
    client.org_info.list_member_groups(pid)

    # 基于code方式登录，
    client.get_authorize_url(your_redirect_uri, SCOPE)
    # TODO: 服务器得到传入的code
    client.login_by_code(code)
    
    
    
    # ===========================================================================================
    # 新用户授权
    # ===========================================================================================
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
    save(edo_api.token_code, edo_api.refresh_token_code)

    # 调用特定的API
    status = auto_check(edo_api, edo_api.account.password_check, username='admin', password='')


    # ===========================================================================================
    # 从数据库中初始化用户授权
    # ===========================================================================================
    args = {'key': '',
            'secret': '',
            'api_host' : '',
            'redirect' : ''}
    # 初始化输入参数
    edo_api = EverydoApiClient(**args)

    # 从数据库中得到token，初始化
    token, refresh_token = token_from_sql_server()
    edo_api.auth_with_token(token, refresh_token)

    # 调用接口
    user_info = auto_check(edo_api, edo_api.users.get_user_info, pid='users.admin')


    def auto_check(api_obj, api_func, **kwargs):
        result = api_func(**kwargs)
        # 调用出错自动刷新Token，并将Token保存到数据库
        if 'api_error' in result:
            api_obj.refresh_token(api_obj.refresh_token_code)
            save(api_obj.token_code, api_obj.refresh_token_code)
            result = api_func(**kwargs)

        return result
