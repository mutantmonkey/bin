#!/usr/bin/python3

import os.path
import pyhugh
import subprocess
import yaml

try:
    import xdg.BaseDirectory
    configpath = xdg.BaseDirectory.load_first_config('mmhome', 'config.yml')
except:
    configpath = os.path.expanduser('~/.config/mmhome/config.yml')

config = yaml.safe_load(open(configpath))
h = pyhugh.PyHugh(config['hue_bridge'], config['hue_username'])

h.create_schedule({
    'name': "Off",
    'command': {
        'address': "/api/{0}/groups/0/action".format(h.username),
        'method': "PUT",
        'body': {
            'on': False,
        },
    },
    'time': "PT00:00:25",
    'autodelete': True,
})

subprocess.call(['/usr/bin/systemctl', 'poweroff'])
