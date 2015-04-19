from __future__ import unicode_literals, division, absolute_import
import os
__author__  = 'be4i'
__version__ = '0.1'

import logging

from flexget import plugin, validator
from flexget.entry import Entry
from flexget.event import event
from flexget.config_schema import one_or_more
from flexget.utils import requests, json
from flexget.utils.search import torrent_availability
from flexget.utils.template import RenderError

phpFile = 'php/addtorrent.php?json=1'
log = logging.getLogger('rutorrent')

class rutorrent(object):
    schema = {
        'type': 'object',
        'properties': {
            'user': {'type': 'string'},
            'pass': {'type': 'string'},
            'url': {'type': 'string'},
            'path': {'type': 'string', 'format': 'path'},
            'autostart': {'type': 'boolean', 'default': True}
        },
        'required': ['url'],
    }
        
    def on_task_output(self, task, config):
        session = requests.Session()
        auth = (config.get('user'), config.get('pass'))
        url = config['url'] + '/' + phpFile

        for entry in task.accepted:
            path = entry.get('path', config.get('path', ''))
            
            try:
                path = os.path.normcase(os.path.expanduser(entry.render(path)))
            except RenderError as e:
                log.error('Could not render path for `%s` downloading to default directory.' % entry['title'])
                # Add to default folder
                path = ''

            payload = {'dir_edit': path, 'url': entry['url']}

            if(config['autostart'] == False):
                payload.update({'torrents_start_stopped': '1'})
            
            if task.options.test:
                log.info('Would add `%s` to rutorrent' % entry['title'])
                continue

            result = session.get(url, params=payload, auth=auth)

            if(result.json()['result'] == 'Success'):
                log.info('Added `%s` to rutorrent' % entry['title'])
                log.info('in folder %s ' % path)
            else:
                entry.fail('Fail to add `%s` to rutorrent' % entry['url'])
            
@event('plugin.register')
def register_plugin():
    plugin.register(rutorrent, 'rutorrent', api_ver=2)
 
