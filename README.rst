hoi4tools
=========

Few tools and library to parse content from Hearts of Iron 4.

License
=======

hoi4tools is released under MIT.

Install
=======

.. sourcode:: bash

  python setup.py install


Example
=======

Library
-------

Using the parser directly:

.. sourcecode:: python

  import hoi4tools.parser
  from pprint import pprint
  
  content = """ stuff = {
           foo = {
               biture = sanglier
               cost = 0.42
               power > 9000
               chance < 13.5
               modifier = -0.7
           }
           bar = {
               item1
               item2
               "item3 with quote"
           }
  
  }"""
  
  parser = hoi4tools.parser.Hoi4Yaccer()
  ret = parser.parse(content)
  pprint(ret)


Parsing a file:

.. sourcecode:: python

  import hoi4tools.parser
  import os
  from pprint import pprint
  
  # path to one of the file of HOI4
  file_hoi4 = os.path.join(
      os.environ.get("HOME","~/"),
      ".steam/steam/steamapps/common/Hearts of Iron IV/common/units/destroyer.txt"
  )
  
  ret = hoi4tools.parser.parse_file(file_hoi4)
  pprint(ret)
  

Parsing all .txt files in a directory:

.. sourcecode:: python

  import hoi4tools.parser
  import os
  from pprint import pprint
  
  # path to one of the file of HOI4
  dir_hoi4 = os.path.join(
      os.environ.get("HOME","~/"),
      ".steam/steam/steamapps/common/Hearts of Iron IV/common/units/"
  )
  
  ret = hoi4tools.parser.parse_dir(dir_hoi4)
  pprint(ret)


Parsing + filtering data relevant to production:

.. sourcecode:: python

  import hoi4tools.parser
  import hoi4tools.filters
  import os
  from pprint import pprint
  
  # path to one of the file of HOI4
  dir_hoi4 = os.path.join(
      os.environ.get("HOME","~/"),
      ".steam/steam/steamapps/common/Hearts of Iron IV/common/units/"
  )
  
  ret = hoi4tools.filters.filter_production(
      hoi4tools.parser.parse_dir(dir_hoi4)
  )
  pprint(ret)

Command line tool
-----------------

Extract raw content of hoi4 data as json:

.. sourcecode:: bash

  $ hoi4-extract-raw --help

  Usage: hoi4-extract-raw [options]
  
  Options:
    -h, --help            show this help message and exit
    -d DIR, --stats-directory=DIR
                          directory containing the stats files of hoi4
    -f DIR, --file=DIR    path to a data file of hoi4 (ex: infantry.txt)
    -o OUT, --out=OUT     path of outpout json file


Extract and filter content from hoi4 for production stat as json:

.. sourcecode:: bash

  $ hoi4-extract-prod --help

  Usage: hoi4-extract-raw [options]
  
  Options:
    -h, --help            show this help message and exit
    -d DIR, --stats-directory=DIR
                          directory containing the stats files of hoi4
    -f DIR, --file=DIR    path to a data file of hoi4 (ex: infantry.txt)
    -o OUT, --out=OUT     path of outpout json file



