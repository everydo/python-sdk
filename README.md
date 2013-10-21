易度开放API的python版本SDK开发包
===================================


这个版本根据新浪微博的python版SDK开发包 [Sinaweibopy](http://michaelliao.github.io/sinaweibopy "Sinaweibopy") 改写，在这里表示由衷的感谢！

安装：

    pip install everydo


使用示范：

    from everydo import APIClient

    domain = input('input you domain')
    # 生成授权地址
    api_client = APIClient(client_id='4343433', client_secret='12345', redirect_uri='http://127.0.0.1/access', domain=domain)
    url = api_client.request_authorize_url()
    print url
       
    # access_token 获取
    code = input('input you code')
    access_token = api_client.request_access_token(grant_type='authorization_code', code=code)
    api_client.set_access_token(access_token=access_token.access_token, refresh_token=access_token.refresh_token, expires=acce    ss_token.expires)
 
    # api调用
    user_info = api_client.get.user_info(pid='users.admin')
    file_info = api_client.get.file_info(site='defaults', uid='223232323')
