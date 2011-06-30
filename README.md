# Python IPGeoBase

## Description:

This helper can generate pickle db from txt files, than you can use
this db to get ipgeobase (http://ipgeobase.ru) info by ip address.

## Usage:

1. Download latest archieve of txt files http://ipgeobase.ru/files/db/Main/geo_files.tar.gz
2. Put both txt files to geo_files dir
3. Run 'python cidr_create.py'
4. Look at example.py (in file was written django custom managemen command) how to use cidr_pickle.db

## Simple example

    >>> from example import ipgeobase_info
    >>> c, r, t = ipgeobase_info('46.20.191.2')
    >>> print c, r, t
    RU Владимирская область Владимир