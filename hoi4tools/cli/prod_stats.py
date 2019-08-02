#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from optparse import OptionParser
import os
import sys
import re
import json
import hoi4tools.parser
import hoi4tools.filters

def main():

    parser = OptionParser()
    parser.add_option("-d", "--stats-directory", dest="directory",
            help="directory containing the stats files of hoi4",
            default=os.path.join(
                os.environ.get("HOME","~/"), 
                ".steam/steam/steamapps/common/Hearts of Iron IV/common/units/"
            ),
            metavar="DIR")

    parser.add_option("-f", "--file", dest="file",
            help="path to a data file of hoi4 (ex: infantry.txt)",
            metavar="DIR")
    parser.add_option("-o", "--out", dest="out_file",
            help="path of outpout json file", default=None,
            metavar="OUT")

    (options, args) = parser.parse_args()

    if options.directory is None and options.file is None:
        print("missing --directory or --file option")
        sys.exit(1)


    if options.file is not None and options.directory is not None:
        print("option --directory and --file are exclusive, please pick one")
        sys.exit(1)

    data = {}

    if options.file:
        data = hoi4tools.parser.parse_file(options.file)

    elif options.directory:
        data = hoi4tools.parser.parse_dir(options.directory)

    data = hoi4tools.filters.filter_production(data)

    json_data = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))

    if options.out_file:
        with open(options.out_file, 'w') as o:
            o.write(json_data)
    else:
        print(json_data)

if __name__ == '__main__':
    main()
