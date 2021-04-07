# installer for OWFS
# Copyright 2014-2020 Matthew Wall
# Copyright 2020-2021 Glenn McKechnie
# Distributed under the terms of the GNU Public License (GPLv3)

from weecfg.extension import ExtensionInstaller

def loader():
    return OWFSInstaller()

class OWFSInstaller(ExtensionInstaller):
    def __init__(self):
        super(OWFSInstaller, self).__init__(
            version="0.23.8",
            name='owfs',
            description='driver for one-wire devices connected via owfs',
            author="Matthew Wall, Glenn McKechnie",
            author_email="glenn.mckechnie@gmail.com",
            config={
                'OWFS': {
                    'driver': 'user.owfs',
                    'sensor_map': {},
                    'sensor_type': {}}},
            files=[('bin/user', ['bin/user/owfs.py'])]
            )
