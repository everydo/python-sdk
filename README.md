易度开放API的python版本SDK开发包
===================================

安装：

    pip install everydo


使用示范：
    from everydo import EverydoApiClient

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

    # 获取oc的API操作对象
    oc_api = edo_api.get_account()

    sites = edo_api.list_sites
    for site in sites.values():
        print "site_name: %s ,site_title: %s \nsite_url: %s\n" % (site['site_name'], sites['site_title'], sites['site_url'])

    # 特定站点的API操作对象
    wo_api = edo_api.get_site('default')

    # 调用特定的API
    file_info = wo_api.files.file_info(file_id=9284298392)

