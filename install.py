# installer for OWFS
# Copyright 2014-2020 Matthew Wall

from weecfg.extension import ExtensionInstaller

def loader():
    return OWFSInstaller()

class OWFSInstaller(ExtensionInstaller):
    def __init__(self):
        super(OWFSInstaller, self).__init__(
            version="0.22",
            name='owfs',
            description='driver for one-wire devices connected via owfs',
            author="Matthew Wall",
            author_email="mwall@users.sourceforge.net",
            config={
                'OWFS': {
                    'driver': 'user.owfs',
                    'interface': 'u',
                    'sensor_map': {},
                    'sensor_type': {}}},
            files=[('bin/user', ['bin/user/owfs.py'])]
            )
