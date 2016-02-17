#!/usr/bin/python2.7

import sys
import json
import collections
import difflib

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
        a string containing the csv header

    """

    ti_id_attr = table_1['table']['idAttrib']
    t2_id_attr = table_1['table']['idAttrib']

    header = '"pairId:INTEGER",'

    header = '%s"%s.%s:%s","%s.%s:%s",' % (header, prepend_1,
                     ti_id_attr['name'], ti_id_attr['type'], prepend_2,
                     t2_id_attr['name'], t2_id_attr['type'])

    for attr in table_1['table']['attributes']:
        if attr['name'] == ti_id_attr['name']: continue
        header = '%s"%s.%s:%s",' % (header, prepend_1, attr['name']
                                   ,attr['type'].upper())

    for attr in table_2['table']['attributes']:
        if attr['name'] == t2_id_attr['name']: continue
        header = '%s"%s.%s:%s",' % (header, prepend_2, attr['name']
                                   ,attr['type'].upper())

    return header

def do_blocking(table_1, prepend_1, table_2, prepend_2, csv_file
               ,matching_attrs):
    """Given 2 dictionaries containing the data of 2 tables, does
    blocking and writes it into the csv_file.

    Args:
        table_1  : dictionary containing the data of table 1
        prepend_1: prepend to all the attributes from table_1 in the
                   blocked table
        table_2  : dictionary containing the data of table 2
        prepend_1: prepend to all the attributes from table_2 in the
                   blocked table
        csv_file : file into which the blocked data is written in csv
                   format

    """

    header = get_csv_header(table_1, prepend_1, table_2, prepend_2)

    t1_id = table_1['table']['idAttrib']['name']
    t2_id = table_1['table']['idAttrib']['name']

    pair_id = 1

    # insert book tuples from table_2 into a dictionary per matching
    # attribute so that lookups of books from table_1 in table_2 is
    # efficient
    #table_2_tuples = []
    #for index, matching_attr in enumerate(matching_attrs):
    #    table_2_tuples.append({})
    #    for book_tuple in table_2['table']['tuples']:
    #        attr_val = book_tuple[matching_attr]
    #        table_2_tuples[index][attr_val] = collections.OrderedDict()
    #        for attr in book_tuple:
    #            table_2_tuples[index][attr_val][attr] = book_tuple[attr]

    with open(csv_file, 'w') as csv_fo:
        print >> csv_fo, header

    with open(csv_file, 'a') as csv_fo:
        for book_tuple_1 in table_1['table']['tuples']:
            for book_tuple_2 in table_2['table']['tuples']:
                #for index, matching_attr in enumerate(matching_attrs):
                ratio = difflib.SequenceMatcher(None, book_tuple_1['Publisher']
                                    ,book_tuple_2['Publisher']).ratio()
                if ratio >= 0.85:
                    #if (book_tuple_1['Publication_date'] !=
                    #    book_tuple_2['Publication_date']):
                    #    continue
                    # write the ids
                    matched_tuple = '"%s","%s","%s","%s"' % (ratio, pair_id,
                                            book_tuple_1[t1_id],
                                            book_tuple_2[t2_id])

                    # append attributes from table 1
                    for attr in book_tuple_1:
                        if attr == t1_id: continue
                        if (    isinstance(book_tuple_1[attr], str)
                            and '"' in book_tuple_1[attr]):
                            book_tuple_1[attr] = book_tuple_1[attr].replace('"', '""')
                        matched_tuple = '%s,"%s"' % (matched_tuple
                                                    ,book_tuple_1[attr])

                    # append attributes from table 2
                    for attr in book_tuple_2:
                        if attr == t2_id: continue
                        if (    isinstance(book_tuple_2[attr], str)
                            and '"' in book_tuple_2[attr]):
                            book_tuple_2[attr] = book_tuple_2[attr].replace('"', '""')
                        matched_tuple = '%s,"%s"' % (matched_tuple
                                                    ,book_tuple_2[attr])


                    pair_id += 1
                    print >> csv_fo, matched_tuple.encode('utf8')
            #num_matches = 0
            #for index, attr in enumerate(matching_attrs):
            #index = 0
            #attr_val = book_tuple[matching_attrs[index]]
            #if attr_val in table_2_tuples[index]:  # match
            #    num_matches += 1
            #    for attr in matching_attrs[index+1:]:
            #        print book_tuple[matching_attrs[num_matches]], table_2_tuples[index][attr_val][attr]
            #        if book_tuple[matching_attrs[num_matches]] == table_2_tuples[index][attr_val][attr]:
            #            num_matches += 1
            #        else:
            #            break

            #if num_matches == len(matching_attrs):
                #return

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
    """"""

    json_fpath_1 = sys.argv[1]
    json_fpath_2 = sys.argv[2]

    table_1 = load_json(json_fpath_1)
    table_2 = load_json(json_fpath_2)

    csv_file = 'blocked.csv'
    prepend_1 = 'amzn'
    prepend_2 = 'bnn'
    do_blocking(table_1, prepend_1, table_2, prepend_2, csv_file
                ,['Title'])
               #,['Publication_date', 'Pages'])

if __name__ == '__main__':
    main()
