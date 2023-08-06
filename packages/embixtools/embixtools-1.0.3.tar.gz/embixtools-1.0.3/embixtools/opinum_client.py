import requests
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
from functools import wraps
from datetime import datetime as dt, timedelta as td

class Opinum(object):
    
    def __init__(self, usr, pwd, client_id, client_secret):
        self.username = usr
        self.password = pwd
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = ''
        self.token_expiration = dt(1000,1,1)
        self.sites = self.request('GET','sites').json()
        self.sources = self.request('GET','sources', params = {'sourcesFilter.displayLevel': 'Site'}).json()
        self.variables = self.request('GET','variables').json()
        self.timeseries = [
            {
                'id': variable['id'],
                'site': source['siteName'],
                'source': source['name'],
                'name': variable['name'],
            }
            for source in self.sources
            for variable in self.variables if variable['sourceId'] == source['id']
        ]

    def auth(self):
        oauth = OAuth2Session(
            client = LegacyApplicationClient(client_id=self.client_id)
        )
        token = oauth.fetch_token(
            token_url = 'https://identity.opinum.com/connect/token',
            scope = 'opisense-api push-data',
            username = self.username,
            password = self.password,
            client_id = self.client_id,
            client_secret = self.client_secret,
            auth = None
        )
        self.token =  'Bearer ' + token['access_token']
        self.token_expiration = dt.utcnow() + td(seconds=60)
        return self.token
    
    def var(self, site, source, name):
        return [
            ts['id'] for ts in self.timeseries 
            if all((
                ts['site'] == site,
                ts['source'] == source,
                ts['name'] == name,
            ))
        ][0]
    
    def token_required(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if dt.utcnow() > self.token_expiration:
                self.auth()
            return func(self, *args, **kwargs)
        return wrapper
    
    @token_required
    def request(self, method, url, data={}, params={}, headers={}):
        resp = requests.request(
            method = method,
            url = f'https://api.opinum.com/{url}',
            params = params,
            headers = {**headers, 'Authorization': self.token},
            json = data
        )
        if resp.status_code >= 400:
            raise Exception(f'{resp.status_code} || {resp.text}')
        return resp

    @token_required
    def push(self, dps):
        resp = requests.post(
            url = 'https://push.opinum.com/api/data',
            json = dps,
            headers = {
                'Authorization': self.token,
            },
        )
        if resp.status_code >= 400:
            raise Exception(f'{resp.status_code} || {resp.text}')
        return resp
    
    @token_required
    def get_ts(self, site, source, name, interval=None):
        params = {
            'filter.variableId': self.var(site, source, name),
            'filter.displayLevel': 'ValueVariableDate',
            'filter.includeToBoundary': True
        }
        if not interval is None:
            params['filter.from'] = interval[0].strftime('%Y-%m-%dT%H:%M:%S')
            params['filter.to'] = interval[1].strftime('%Y-%m-%dT%H:%M:%S')
        data = self.request(method='GET', url='data', params=params).json()
        return [{'date': x['date'], 'rawValue': x['rawValue']} for x in data]
    
    @token_required
    def push_ts(self, site, source, name, dps):
        return self.push([{
            'variableId': self.var(site, source, name), 
            'data': dps
        }])