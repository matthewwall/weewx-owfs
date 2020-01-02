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

4) start weewx

sudo /etc/init.d/weewx start
