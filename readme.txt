
This fork contains a driver named owfs-dallas.py that is based on the
original owfs.py. Once finished it's intended that it will be merged
into this fork as owfs.py

Its main difference with mwalls original owfs.py is that it includes a
new function that provides windDir values for an original dallas weather
station that used DS2406 and DS2401 sensors.

There is also a separate function called rain_withpath and that is
derived from rainwise_bucket. This deliberately removes the secondary
path to the counter. That secondary path is expected to be supplied by
the [[sensor_map]].

The _main_ function that allows the script to be run directly from a
terminal is incomplete. It needs more work for the pyownet side to work
as expected (for =readings).

N.B.

The latest distributions appear to have dropped the python-ow package.
pyownet is a drop in replacement for that module and this driver, and
the original owfs.py will adjust themselves accordingly.

With the change to pyownet, the owserver package becomes a new requirement

sudo apt install owserver

then configure the owserver by moving aside the contents of
/etc/owfs.conf and creating a new file with the contents as
follows, and uncommenting one of the first 3 device entries...

/etc/owfs.conf

#server: usb = all # for a DS9490
#server: device = /dev/ttyS1 # for a serial port
#server: device /dev/i2c-1 # for a pi using i2c-1
server: port = 4304

restart owserver...

sudo /etc/init.d/owserver stop
sudo /etc/init.d/owserver start


======

owfs - weewx driver for one-wire devices via one-wire file system (OWFS)
Copyright 2014-2020 Matthew Wall

Installation instructions:

0) install the python bindings for owfs:

sudo apt-get install python-ow

1) run the installer:

wee_extension --install weewx-owfs.tgz

2) scan for one-wire sensors and readings/names:

sudo PYTHONPATH=/home/weewx/bin python /home/weewx/bin/user/owfs.py --sensors
sudo PYTHONPATH=/home/weewx/bin python /home/weewx/bin/user/owfs.py --readings

3) modify weewx.conf, mapping database fields to devices, for example:

[OWFS]
    [[sensor_map]]
        outTemp = /uncached/28.8A071E050000/temperature
        UV = /uncached/EE.1F20CB020800/UVI/UVI
        luminosity = /26.FB67E1000000/S3-R1-A/luminosity
        lightning = /1D.1AD00F000000/counters.A
    [[sensor_type]]
        lightning = counter

If using owfs as a driver, specify OWFS as the station_type:

[Station]
    station_type = OWFS

If using owfs as a service, add OWFSService to the list of services:

[Engine]
    [[Services]]
        data_services = user.owfs.OWFSService

4) restart weewx

sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx start
