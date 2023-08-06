#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import csv
from itertools import islice
from prettytable import PrettyTable

__author__ = 'franklinsijo'

class CSVViewer(object):
    def __init__(self, args):
        try:
            self.csvfile = args.CSVFILE[0]
            if not os.path.isfile(self.csvfile):
                raise IOError(self.csvfile + ' is not a valid file')
        except Exception as e:
            raise e
        self.delimiter = args.DELIMITER
        self.max_lines = args.LINES
        self.has_header = args.HAS_HEADER

    def view(self):
        with open(self.csvfile, 'r', encoding="utf8", errors='ignore') as fp:
            fr =csv.reader(fp, delimiter=self.delimiter)     
            tbl = PrettyTable()   
            if self.has_header:
                header = next(fr)                                                                  
                tbl.field_names = header
            records = []
            if self.max_lines < 0:
                for row in fr:
                    records.append(row)
            else:
                for row in islice(fr, 0, self.max_lines):
                    records.append(row)
            tbl.add_rows(records)
            print(tbl.get_string())


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument("CSVFILE", nargs=1, type=str, help="path of the csv file to view")
    argparser.add_argument("-l", "--lines", dest="LINES", type=int, default=-1, help="number of lines to view (default: no limit)")
    argparser.add_argument("-d", "--delimiter", dest="DELIMITER", type=str, default=",", help="character to use as field delimiter (default: COMMA [,])")
    argparser.add_argument("--has-header", dest="HAS_HEADER", action="store_true", help="the first row of the file is considered as the header")
    args = argparser.parse_args()
    viewer = CSVViewer(args)
    viewer.view()
   