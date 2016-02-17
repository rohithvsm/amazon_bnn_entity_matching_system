#!/usr/bin/python2.7
"""
Read book data from a json & format the Publication_date as MM/DD/YYYY.

"""

import sys
sys.path.append('../')
import time
import blocking
import tableA_amazon

def format_date(table_1):
    """Iterate through the json dictionary and format the Publication
    date field of the json.

    Args:
        table_1: python dictionary containing the json data

    """

    for index, t1_tup in enumerate(table_1['table']['tuples']):
        t1_pub_yr_str = t1_tup['Publication_date']
        try:
            t1_pub_date = time.strptime(t1_pub_yr_str, '%m/%d/%y')
            t1_tup['Publication_date'] = time.strftime('%m/%d/%Y', t1_pub_date)
            table_1['table']['tuples'][index]['Publication_date'] = (
                        time.strftime('%m/%d/%Y', t1_pub_date))
        except ValueError:
            try:
                t1_pub_date = time.strptime(t1_pub_yr_str, '%m/%d/%Y')
                t1_tup['Publication_date'] = time.strftime('%m/%d/%Y', t1_pub_date)
                table_1['table']['tuples'][index]['Publication_date'] = (
                        time.strftime('%m/%d/%Y', t1_pub_date))
            except ValueError:
                try:
                    t1_pub_date = time.strptime(t1_pub_yr_str, '%B %Y')
                    t1_tup['Publication_date'] = time.strftime('%m/%Y', t1_pub_date)
                    table_1['table']['tuples'][index]['Publication_date'] = (
                            time.strftime('%m/%Y', t1_pub_date))
                except ValueError:  # contains only YYYY
                    pass

    return table_1

def main():
    """Load the input json, format it and dump it in the output json."""

    if len(sys.argv) < 3:  # check command-line arguments
        print >> sys.stderr, ('Usage: %s input_json_path output_json_path'
                               % __file__)
        sys.exit(1)

    json_ipath = sys.argv[1]
    json_opath = sys.argv[2]

    table_1 = blocking.load_json(json_ipath)
    table_1_formatted = format_date(table_1)
    tableA_amazon.dump_json(table_1_formatted, json_opath)

if __name__ == '__main__':
    main()
