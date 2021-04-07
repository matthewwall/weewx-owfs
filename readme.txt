This driver is kept updated and is a drop in replacement for mwalls
original owfs.py.

It fixes some python3 / weewx4 bugs. It also has some additions.
It has been fairly well tested on python2 / python3 installations both as
a driver and as a service.
If there are any issues with it then contact me via github, or through
the weewx-users group and I'll endeavour to fix them.

This fork contains a driver named owfs-dallas.py that is based on mwalls
original owfs.py. It was created to develop a new function that provides
windDir values for the original dallas weather station that used DS2406
and DS2401 sensors.

It also contains a separate function called rain_withpath that is
derived from rainwise_bucket. This deliberately removes the hardcoded
secondary path to the counter and is intended for use with other rain
gauges.
That secondary path is expected to be supplied via the [[sensor_map]]
stanza.

The script can be run manually and will now return values when using the
pyownet module.

sudo PYTHONPATH=/home/weewx/bin python /home/weewx/bin/user/owfs.py --help

It functions in a compatible manner to the original python-ow method
with the addition of --pyownet_readings that offers a subset of the
--readings entries. It returns the values most likely to be required.

Also, the interface configuration has been tweaked to allow its omission
from weewx.conf when either ow or pyownet is used. The default is still
the USB for python-ow and localhost:4304 for pyownet (as hardcoded in
owfs.py. The option can still be used in weewx.conf if those defaults are
not suitable.

As of June 2020, owfs-dallas has been merged into owfs.py so the above
changes will be available when a "wee_extension" install is performed.

===========
PREREQUISITES

The latest linux distributions appear to have dropped the python3-ow
package. pyownet is a drop in replacement for that module.
This driver, and the original owfs.py will adjust themselves accordingly and
use whichever module is installed.

With the change to pyownet, the owserver package becomes a new requirement

sudo apt install owserver

then configure the owserver by moving aside the contents of
/etc/owfs.conf and creating a new file with the contents as
follows, but uncommenting one of the first 3 device entries as suits
your installation...

/etc/owfs.conf

#server: usb = all # for a DS9490
#server: device = /dev/ttyS1 # for a serial port
#server: device /dev/i2c-1 # for a pi using i2c-1
server: port = 4304

restart owserver...

sudo /etc/init.d/owserver stop
sudo /etc/init.d/owserver start

There are further notes, extracted from owfs.py, that are worth reading
if you require more information about this driver and its methods.
These are at bin/user/pydoc_owfs.txt

======
INSTALLATION & USAGE

owfs - weewx driver for one-wire devices via one-wire file system (OWFS)
Copyright 2014-2020 Matthew Wall, 2020-2021 Glenn McKechnie

Installation instructions:

0) install the python bindings for owfs:

sudo apt-get install python-ow (for python 2.x versions)

or if using weewx 4 with python 3.x then:

sudo apt-get install pyownet

if that is not available via apt-get then uses pip3 (apt-get install
pip3-python to install pip3 ):

sudo pip3 install pyownet

you will also require owserver (see above) to be running.

1) fetch the package:

wget -O https://github.com/glennmckechnie/weewx-owfs/archive/refs/heads/master.zip

2) run the installer:

sudo wee_extension --install weewx-owfs-master.zip

3) scan for one-wire sensors and readings/names. The examples assume a setup.py
installation so the paths may need changing:

sudo PYTHONPATH=/home/weewx/bin python /home/weewx/bin/user/owfs.py --help

sudo PYTHONPATH=/home/weewx/bin python /home/weewx/bin/user/owfs.py --sensors
sudo PYTHONPATH=/home/weewx/bin python /home/weewx/bin/user/owfs.py --readings

Note, it is assumed that 'python' points to the same version as weewx4 is
running.

4) modify weewx.conf, mapping database fields to devices, for example:

[OWFS]
    [[sensor_map]]
        outTemp = /uncached/28.8A071E050000/temperature
        UV = /uncached/EE.1F20CB020800/UVI/UVI
        luminosity = /26.FB67E1000000/S3-R1-A/luminosity
        lightning = /1D.1AD00F000000/counters.A
    [[sensor_type]]
        lightning = counter

If using owfs as a driver:

add the following line to the existing [OWFS] section (mentioned above)
     driver = user.owfs

Under python2.x using the original python-ow module.
The interface was specified under the [OWFS] Section.

With python3.x versions that use pyownet.
No interface is specified. It defaults to using owserver
(localhost:4304)

then specify OWFS as the station_type:
[Station]
    station_type = OWFS

If using owfs as a service, add OWFSService to the list of services:

[Engine]
    [[Services]]
        data_services = user.owfs.OWFSService

5) restart weewx

sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx start


===========

TROUBLESHOOTING

1)
Running owserver under systemd. This applies to the majority of recent
(2019) linux distributions. It only needs to be followed if owserver
won't start..

A problem that has been occurring with owserver on Debian Buster installs
is a refusal to start and run. There's no rhyme or reason to it, and it
magically fixes itself.

The following post describes a possible fix for that problem.

https://sourceforge.net/p/owfs/mailman/message/36765345/
part of...
https://sourceforge.net/p/owfs/mailman/owfs-developers/?viewmonth=201909

In summary, and quoting an extract from the above post ...

"/etc/systemd/system/owserver.service.d/override.conf is an override
file, that you create with"
sudo systemctl edit owserver.service

then add the following content...

# /etc/systemd/system/owserver.service.d/override.conf
[Service]
User=Debian-ow
Group=Debian-ow
ExecStart=
ExecStart=/usr/bin/owserver -c /etc/owfs.conf --foreground

[Install]
Also=


This disables the use of sockets for owserver, and brings the daemon to
the foreground.

This has also been raised as an issue on github. It points to the same solution but adds some more context around the problem..

https://github.com/owfs/owfs/issues/46

