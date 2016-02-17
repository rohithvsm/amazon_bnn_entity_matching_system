#!/usr/bin/python2.7

import sys
import csv

def main():

    csv_fpath = sys.argv[1]

    with open(csv_fpath) as fo:
        csv_reader = csv.reader(fo)
        for line in csv_reader:
            if line[-1] == '1':
                if line[8] != line[15]:
                    print line

if __name__ == '__main__':
    main()
