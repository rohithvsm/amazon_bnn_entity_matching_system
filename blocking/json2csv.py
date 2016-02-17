#!/usr/bin/python2.7

import sys
import blocking

def json2csv(json_dict):
    """

    Args:
        json_dict: dictionary containing the data of table 1

    """

    header = get_csv_header(table_1, prepend_1)

    for book_tuple in table_1['table']['tuples']:
                        if (    isinstance(t1_tup[attr], str)
                            and '"' in t1_tup[attr]):
                            t1_tup[attr] = t1_tup[attr].replace('"', '""')
                        matched_tuple = '%s,"%s"' % (matched_tuple
                                                    ,t1_tup[attr])

def main():

    json_fpath = sys.argv[1]
    csv_fpath  = sys.argv[2]

    table_1 = blocking.load_json(json_fpath)

    json2csv(table1)

if __name__ == '__main__':
    main()
