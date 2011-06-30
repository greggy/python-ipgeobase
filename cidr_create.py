# -*- coding: utf-8 -*-
import cPickle as pickle

GEO_FILES = './geo_files'


def gen_db():
    u'''Функция для генерации pickle базы ipgeobase.ru
    '''
    res = []
    tmp_list = []
    cities_dict = {}
    
    # cidr_optim.txt
    for line in open('%s/cidr_optim.txt' % GEO_FILES, 'r'):
        a = line.split('\t')       
        a[4] = a[4].strip()
        if a[4] == '-':
            a[4] = None
        else:
            a[4] = int(a[4])
            
        tmp_list.append(a[0])
        res.append((int(a[0]), int(a[1]), a[3], a[4]))
    res = sorted(res, key=lambda i: i[0])
    
    # проверка на дубли
    c = 0
    for item in res:
        if c > 0:
            if item[0] == res[c-1][0]:
                res.remove(item)
        c += 1
    
    # cities.txt 
    cities_file = open('%s/cities.txt' % GEO_FILES, 'r').read()
    lines = cities_file.decode('CP1251').split('\n')
    
    for line in lines:
         a = line.split('\t')
         if len(a) > 3:
             cities_dict.update({int(a[0]): (a[1], a[2])})
            
    f = open('%s/cidr_pickle.db' % GEO_FILES, 'w')
    pickle.dump((res, cities_dict), f)
    f.close()


if __name__ == '__main__':
    gen_db()