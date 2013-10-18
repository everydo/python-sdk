#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.0.1'
__author__ = 'Chen Weihong(whchen1080@gmail.com)'

'''
Python client SDK for everydo API using OAuth 2.
'''

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import gzip, time, json, urllib, urllib2, logging, mimetypes, collections

OC_API = ['user_info']
WO_API = ['file_info']


class APIError(StandardError):
    '''
    raise APIError if receiving json message indicating failure.
    '''
    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        StandardError.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.error, self.request)

def _parse_json(s):
    ' parse str into JsonDict '

    def _obj_hook(pairs):
        ' convert json object to python object '
        o = JsonDict()
        for k, v in pairs.iteritems():
            o[str(k)] = v
        return o
    return json.loads(s, object_hook=_obj_hook)

class JsonDict(dict):
    ' general json object that allows attributes to be bound to and also behaves like a dict '

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value

def _encode_params(**kw):
    '''
    do url-encode parameters

    >>> _encode_params(a=1, b='R&D')
    'a=1&b=R%26D'
    >>> _encode_params(a=u'\u4e2d\u6587', b=['A', 'B', 123])
    'a=%E4%B8%AD%E6%96%87&b=A&b=B&b=123'
    '''
    args = []
    for k, v in kw.iteritems():
        if isinstance(v, basestring):
            qv = v.encode('utf-8') if isinstance(v, unicode) else v
            args.append('%s=%s' % (k, urllib.quote(qv)))
        elif isinstance(v, collections.Iterable):
            for i in v:
                qv = i.encode('utf-8') if isinstance(i, unicode) else str(i)
                args.append('%s=%s' % (k, urllib.quote(qv)))
        else:
            qv = str(v)
            args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(args)

def _encode_multipart(**kw):
    ' build a multipart/form-data body with randomly generated boundary '
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in kw.iteritems():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            # file-like object:
            filename = getattr(v, 'name', '')
            content = v.read()
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Length: %d' % len(content))
            data.append('Content-Type: %s\r\n' % _guess_content_type(filename))
            data.append(content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v.encode('utf-8') if isinstance(v, unicode) else v)
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary

def _guess_content_type(url):
    n = url.rfind('.')
    if n==(-1):
        return 'application/octet-stream'
    ext = url[n:]
    return mimetypes.types_map.get(ext, 'application/octet-stream')

_HTTP_GET = 0
_HTTP_POST = 1
_HTTP_UPLOAD = 2

def _http_get(url, authorization=None, **kw):
    logging.info('GET %s' % url)
    return _http_call(url, _HTTP_GET, authorization, **kw)

def _http_post(url, authorization=None, **kw):
    return _http_call(url, _HTTP_POST, authorization, **kw)

def _http_upload(url, authorization=None, **kw):
    logging.info('MULTIPART POST %s' % url)
    return _http_call(url, _HTTP_UPLOAD, authorization, **kw)

def _read_body(obj):
    using_gzip = obj.headers.get('Content-Encoding', '')=='gzip'
    body = obj.read()
    if using_gzip:
        gzipper = gzip.GzipFile(fileobj=StringIO(body))
        fcontent = gzipper.read()
        gzipper.close()
        return fcontent
    return body

def _http_call(the_url, method, authorization, **kw):
    '''
    send an http request and return a json object if no error occurred.
    '''
    boundary = None
    params = _encode_params(**kw)
    http_url = '%s?%s' % (the_url, params) if method==_HTTP_GET else the_url
    http_body = None if method==_HTTP_GET else params
    req = urllib2.Request(http_url, data=http_body)
    req.add_header('Accept-Encoding', 'gzip')
    if authorization:
        req.add_header('Authorization', 'OAuth2 %s' % authorization)
    if boundary:
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    try:
        resp = urllib2.urlopen(req, timeout=5)
        body = _read_body(resp)
        r = _parse_json(body)
        if hasattr(r, 'error_code'):
            raise APIError(r.error_code, r.get('error', ''), r.get('request', ''))
        return r
    except urllib2.HTTPError, e:
        try:
            r = _parse_json(_read_body(e))
        except:
            r = None
        if hasattr(r, 'error_code'):
            raise APIError(r.error_code, r.get('error', ''), r.get('request', ''))
        raise e


class HttpObject(object):

    def __init__(self, client, method):
        self.client = client
        self.method = method

    def __getattr__(self, attr):
        def wrap(**kw):
            if self.client.is_expires():
                raise APIError('21327', 'expired_token', attr)
            import pdb;pdb.set_trace()  
            if attr in WO_API:
            	api_url = self.sites[kw['site']]['url']
            	return _http_call('/'.join([api_url, attr]), self.method, self.client.access_token, **kw)	
            return _http_call('/'.join([self.client.domain, attr]), self.method, self.client.access_token, **kw)
        return wrap



class APIClient(object):
    """docstring for APIClient"""
    def __init__(self, client_id, client_secret, redirect_uri, domain):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.domain = domain
        self.sites = self._list_all_sites(domain)
        self.access_token = None
        self.expires = 0.0
        self.get = HttpObject(self, _HTTP_GET)
        self.post = HttpObject(self, _HTTP_POST)
        self.upload = HttpObject(self, _HTTP_UPLOAD)

    def _list_all_sites(self, domain):
        return [{'name':'test', 'title':"title", 'url':'url'}]

    def request_authorize_url(self, redirect_uri=None, **kw):
        redirect = redirect_uri if redirect_uri else self.redirect_uri

        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
        return '%s%s?%s' % (self.domain, 'authorize', \
                _encode_params(client_id = self.client_id, \
                        redirect_uri = redirect, **kw))


    def _parse_access_token(self, r):
        '''
        new:return access token as a JsonDict: {"access_token":"your-access-token","expires_in":12345678,"uid":1234}, expires_in is represented using standard unix-epoch-time
        '''
        current = int(time.time())
        expires = 3600 + current
        return JsonDict(access_token=r.access_token, refresh_token=r.refresh_token, expires=expires, expires_in=expires, uid=r.get('uid', None))
        
    def request_access_token(self, grant_type, **kw):
        r = _http_post('%s%s' % (self.domain, 'access_token'), \
                client_id = self.client_id, \
                client_secret = self.client_secret, \
                grant_type = grant_type, **kw)
        return self._parse_access_token(r)

    def set_access_token(self, access_token, refresh_token, expires):
        self.access_token = access_token 
        self.expires = expires

    def load_token(self, access_token, refresh_token, expires):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires = expires

    def is_expires(self):
        return not self.access_token or time.time() > self.expires


if __name__ == '__main__':
    domain = input('input you domain')
    # 生成授权地址
    api_client = APIClient(client_id='4343433', client_secret='12345', redirect_uri='http://127.0.0.1/access', domain=domain)
    url = api_client.request_authorize_url()
    print url

    # access_token 获取
    code = input('input you code')
    access_token = api_client.request_access_token(grant_type='authorization_code', code=code)
    api_client.set_access_token(access_token=access_token.access_token, refresh_token=access_token.refresh_token, expires=access_token.expires)

    # api调用
    user_info = api_client.get.user_info(pid='users.admin')
    file_info = api_client.get.file_info(site='defaults', uid='223232323')
