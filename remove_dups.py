#!/usr/bin/python2.7
import json
import collections

with open('../barnesandnobles.json') as fo:
    table_2 = json.load(fo)
    table_new = {}
    table_new['table'] = collections.OrderedDict()
    table_new['table']['name'] = table_2['table']['name']
    table_new['table']['description'] = table_2['table']['description']
    table_new['table']['idAttrib'] = table_2['table']['idAttrib']
    table_new['table']['attributes'] = table_2['table']['attributes']
    table_new['table']['tuples'] = []
    dict_ = {}
    #count = 0
    for tup in table_2['table']['tuples']:
        val = collections.OrderedDict()
        val['id'] = int(tup['id'])
        val['ISBN_13'] = int(tup['ISBN_13'])
        val['Title'] = tup['Title']
        val['Author'] = tup['Author']
        val['Price'] = float(tup['Price'])
        val['Publisher'] = tup['Publisher']
        val['Publication_date'] = tup['Publication_date']
        val['Pages'] = int(tup['Pages'])
        dict_[tup['ISBN_13']] = val
        #count += 1
        #if count > 100:
        #    break

    i = 1
    for isbn in dict_:
        dict_[isbn]['id'] = i
        i += 1
        table_new['table']['tuples'].append(dict_[isbn])
with open('new.json', 'wb') as file_obj:
    print >> file_obj, json.dumps(table_new, indent=4
                                     ,separators=(',', ': '))
