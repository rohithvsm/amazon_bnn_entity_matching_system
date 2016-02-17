#!/usr/bin/python2.7

import sys
import json
import collections
#import difflib
#import csv

def get_csv_header(table_1, prepend_1, table_2, prepend_2):
    """Writes the csv header looking at the table schema in table_1.

    Args:
        table_1  : dictionary containing the schema of the table 1
        prepend_1: prepend to all the attributes from table_1 in the
                   blocked table
        table_2  : dictionary containing the schema of the table 2
        prepend_1: prepend to all the attributes from table_2 in the
                   blocked table

    Returns:
        a list containing the csv header fields

    """

    ti_id_attr = table_1['table']['idAttrib']
    t2_id_attr = table_1['table']['idAttrib']

    header = '"pairId:INTEGER",'

    header = '%s"%s.%s:%s","%s.%s:%s",' % (header, prepend_1,
                     ti_id_attr['name'], ti_id_attr['type'], prepend_2,
                     t2_id_attr['name'], t2_id_attr['type'])
    #header = ['pairId:INTEGER']
    #header.append('%s.%s:%s' % (prepend_1, ti_id_attr['name']
    #                           ,ti_id_attr['type']))
    #header.append('%s.%s:%s' % (prepend_2, t2_id_attr['name']
    #                           ,t2_id_attr['type']))

    for attr in table_1['table']['attributes']:
        if attr['name'] == ti_id_attr['name']: continue
        header = '%s"%s.%s:%s",' % (header, prepend_1, attr['name']
                                   ,attr['type'].upper())
        #header.append('%s.%s:%s' % (prepend_1, attr['name']
        #                           ,attr['type'].upper()))

    for attr in table_2['table']['attributes']:
        if attr['name'] == t2_id_attr['name']: continue
        header = '%s"%s.%s:%s",' % (header, prepend_2, attr['name']
                                   ,attr['type'].upper())
        #header.append('%s.%s:%s' % (prepend_2, attr['name']
        #                           ,attr['type'].upper()))

    return header

def do_blocking(table_1, prepend_1, table_2, prepend_2, csv_file
               ,blocking_attr):
    """Given 2 dictionaries containing the data of 2 tables, does
    blocking to generate the candidate set and writes it into the
    csv_file.

    Args:
        table_1      : dictionary containing the data of table 1
        prepend_1    : prepend to all the attributes from table_1 in the
                       blocked table
        table_2      : dictionary containing the data of table 2
        prepend_1    : prepend to all the attributes from table_2 in the
                       blocked table
        csv_file     : file into which the blocked data is written in
                       csv format
        blocking_attr: the attribute in the table on which the blocking
                       is done

    """

    header = get_csv_header(table_1, prepend_1, table_2, prepend_2)

    t1_id = table_1['table']['idAttrib']['name']
    t2_id = table_1['table']['idAttrib']['name']

    # insert book tuples from table_2 into a dictionary indexed on the
    # matching attribute so that lookups of books from table_1 in
    # table_2 is efficient
    t2_idxd = collections.defaultdict(list)
    for book_tuple in table_2['table']['tuples']:
        t2_idxd[book_tuple[blocking_attr]].append(collections.OrderedDict(
                                                                   book_tuple))

    pair_id = 1
    with open(csv_file, 'wb') as csv_fo:
        #blk_csv = csv.writer(csv_fo)
        #blk_csv.writerow(header)
        print >> csv_fo, header

        # iterate through the tuples in table_1 and match it with
        # table_2 on the blocking_attr using the t2_idxd
        for t1_tup in table_1['table']['tuples']:
            blking_attr_val = t1_tup[blocking_attr]
            if blking_attr_val in t2_idxd:
                for t2_tup in t2_idxd[blking_attr_val]:
                    matched_tuple = '"%s","%s","%s"' % (pair_id, t1_tup[t1_id]
                                                       ,t2_tup[t2_id])
                    #matched_tuple = ['%s' % pair_id, '%s' % t1_tup[t1_id]
                    #                ,'%s' % t2_tup[t2_id]]

                    # append attributes from table 1
                    for attr in t1_tup:
                        if attr == t1_id: continue
                        if (    isinstance(t1_tup[attr], str)
                            and '"' in t1_tup[attr]):
                            t1_tup[attr] = t1_tup[attr].replace('"', '""')
                        matched_tuple = '%s,"%s"' % (matched_tuple
                                                    ,t1_tup[attr])
                        #if isinstance(t1_tup[attr], str):
                        #    t1_tup[attr] = t1_tup[attr].encode('utf8')
                        #    if '"' in t1_tup[attr]:
                        #        t1_tup[attr] = t1_tup[attr].replace('"', '""')
                        #matched_tuple.append('%s' %t1_tup[attr])

                    # append attributes from table 2
                    for attr in t2_tup:
                        if attr == t2_id: continue
                        if (    isinstance(t2_tup[attr], str)
                            and '"' in t2_tup[attr]):
                            t2_tup[attr] = t2_tup[attr].replace('"', '""')
                        matched_tuple = '%s,"%s"' % (matched_tuple
                                                    ,t2_tup[attr])
                        #if isinstance(t2_tup[attr], str):
                        #    t2_tup[attr] = t2_tup[attr].encode('utf8')
                        #    if '"' in t2_tup[attr]:
                        #        t2_tup[attr] = t2_tup[attr].replace('"', '""')
                        #matched_tuple.append('%s' %t2_tup[attr])

                    pair_id += 1
                    print >> csv_fo, matched_tuple.encode('utf8')
                    #blk_csv.writerow(matched_tuple.encode('utf8').split(','))

def load_json(json_file_path):
    """Loads the json data present in the file located at json_file_path
    to a python dictionary.

    Args:
        json_file_path: path of the file containing the json data

    Returns:
        python dictionary containing the json data

    """

    with open(json_file_path) as json_fo:
        return json.load(json_fo, object_pairs_hook=collections.OrderedDict)

def main():
    """Load data of the 2 tables from json files and perform the
    blocking."""

    json_fpath_1 = sys.argv[1]
    json_fpath_2 = sys.argv[2]

    table_1 = load_json(json_fpath_1)
    table_2 = load_json(json_fpath_2)

    csv_file      = 'blocked.csv'
    prepend_1     = 'amzn'
    prepend_2     = 'bnn'
    blocking_attr = 'Publisher'

    do_blocking(table_1, prepend_1, table_2, prepend_2, csv_file
               ,blocking_attr)

if __name__ == '__main__':
    main()
