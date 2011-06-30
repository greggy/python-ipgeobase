# -*- coding: utf-8 -*-
import struct
import socket
import cPickle as pickle

from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings

from server.regions import REGIONS
import pygeoip


DB_TUPLE = pickle.load(open(settings.IPGEOBASE_DB, 'r')) # (x, y) x - диапозон ip, y - названия
SEEK_INFO = {}


def ipgeobase_info(ip):
    # читаем из ipgeobase
    if ip in SEEK_INFO:
        return SEEK_INFO[ip]
    else:
        number = struct.unpack('!L', socket.inet_aton(ip))[0]
        for i in DB_TUPLE[0]:
            if i[0] <= number <= i[1]:
                 item_id = DB_TUPLE[0].index(i)
                 break
            else:
                item_id = None
        if item_id:
            item = DB_TUPLE[0][item_id]
            region, city = '', ''
            if item[3]:
                info2 = DB_TUPLE[1][item[3]]
                region, city = info2[1], info2[0]
                SEEK_INFO[ip] = (item[2], region, city)
            return (item[2], region, city)
        else:
            return (None, None, None)


def get_geoip_info(ip, geo_db):
    u'''
        Собираем окончательную geoip информацию.
        geo_db передаём параметром чтоб не загружать базу на каждую итерацию.
    '''
    country, region, city = ipgeobase_info(ip)

    # читаем geoip
    if not region:
        info = geo_db.lookup(ip)
        country = info.country
        region = REGIONS.get('%s%s' % (info.country, info.region))
        city = info.city

    return (country, region, city)


class Command(BaseCommand):
    args = ''
    help = 'Write from cache to database.'

    def handle(self, *args, **options):
        geo_db = pygeoip.Database(settings.GEOIPDB_PATH)
        shown_ads = cache.get('focusme_ads')
        if shown_ads:
            # Сама запись в базу.
            count = 0
            for entry in shown_ads:
                country, region, city = get_geoip_info(entry[4], geo_db)
                try:
                    stat = Statistic.objects.create(
                            date_add = entry[0],
                            upload_id = entry[1],
                            url = entry[2],
                            user_uid = entry[3],
                            ip_addr = entry[4],
                            place_id = entry[5],
                            
                            geoip_country = country,
                            geoip_region = region,
                            geoip_city = city
                        )
                except:
                    print 'error:', entry
                count += 1
            print "Was written %d raws." % count

