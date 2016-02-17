#!/usr/bin/python2.7
import sys
import random

def pick_random_sample(file_path, sample_size):
    with open(file_path) as in_fo:
        num_lines = 0
        for line in in_fo:
            num_lines += 1

        sample_line_nos = random.sample(xrange(1, num_lines), 301)
        #sample_line_nos.sort()

        with open('tableG.csv', 'w') as out_fo:
            in_fo.seek(0, 0)
            print >> out_fo, in_fo.readline().strip()
            for line_no, line in enumerate(in_fo):
                if line_no in sample_line_nos:
                    print >> out_fo, line.strip()

def main():
    blocked_csv = sys.argv[1]
    sample_size = sys.argv[2]

    pick_random_sample(blocked_csv, sample_size)

if __name__ == '__main__':
    main()
