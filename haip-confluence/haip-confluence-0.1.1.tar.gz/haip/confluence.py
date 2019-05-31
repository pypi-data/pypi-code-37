import logging
import aiohttp 
import haip.config as config

_logger = logging.getLogger(__name__)

def getSession():
    cfg = config.get('confluence', username=None, password=None, timeout=10)
    params = {'timeout': aiohttp.ClientTimeout(total=cfg.timeout)}
    if cfg.username is not None:
        params['auth'] = aiohttp.BasicAuth(cfg.username, cfg.password)
    return aiohttp.ClientSession(**params)

async def getBody(id, expand='version,body.storage'):
    cfg = config.get('confluence', url=config.MANDATORY)
    url = f'{cfg.url}content/{id}?expand={expand}'
    async with getSession() as session:
        async with session.get(url, headers={'Content-Type': 'application/json'}) as response:
            data = await response.json()
            return { 'version': data['version']['number'], 
                     'title': data['title'],
                     'body': data['body']['storage']['value'] }

async def setBody(id, body):
    current = await getBody(id)
    cfg = config.get('confluence', url=config.MANDATORY)
    url = f'{cfg.url}content/{id}?expand=version'
    payload = {
        'version': {
            'number': current['version'] + 1
        }, 
        'title': current['title'],
        'type': 'page',
        'body': {
            'storage': {
                'value': body,
                'representation': 'storage'
            }
        }
    }
    async with getSession() as session:
        async with session.put(url, json=payload) as response:
            data = await response.json()
            _logger.info("update confluence page %s (old_version=%s, new_version=%s)", 
                         id, current['version'], data['version']['number'])
            return data

async def createPage(space, parent_id, title, body):
    cfg = config.get('confluence', url=config.MANDATORY)
    url = f'{cfg.url}content'
    payload = {
        'title': title,
        'type': 'page',
        'space': {
            'key': space
        },
        'ancestors': [{ 'id': parent_id }],
        'body': {
            'storage': {
                'value': body,
                'representation': 'storage'
            }
        }
    }
    async with getSession() as session:
        async with session.post(url, json=payload) as response:
            data = await response.json()
            return data
        
async def getChildren(id, expand='version,body.storage'):
    cfg = config.get('confluence', url=config.MANDATORY)
    url = f'{cfg.url}content/{id}/child/page?limit=1000&expand={expand}'
    async with getSession() as session:
        async with session.get(url, headers={'Content-Type': 'application/json'}) as response:
            data = await response.json()
            children = []
            for item in data['results']:
                child = {
                    'id': item['id'],
                    'title': item['title'],
                    'version': item['version']['number'],
                    'body': item['body']['storage']['value']
                }
                children.append(child)
            return children

async def upload(id, name, file):
    cfg = config.get('confluence', url=config.MANDATORY)
    url = f'{cfg.url}content/{id}/child/attachment'
    async with getSession() as session:
        # first get attachment-id (if exists)
        attachment_id = None
        async with session.get(url) as response:
            data = await response.json()
            for attachment in data['results']:
                if attachment['title'] == name:
                    attachment_id = attachment['id']
                    break
        if attachment_id is not None:
            url = f'{url}/{attachment_id}/data'
        # create/update attachment
        data = aiohttp.FormData()
        data.add_field('file', open(file, 'rb'), filename=name)
        async with session.post(url, headers={ 'X-Atlassian-Token': 'nocheck' }, data=data) as response:
            data = await response.json()
            return data


