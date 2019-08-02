import hoi4tools.parser
from pprint import pprint


print("####################")
# Basic direct parsing
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

print("####################")
# parsing of a file
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

print("####################")
# parsing of a whole directory
import hoi4tools.parser
import os
from pprint import pprint

# path to one of the directory of HOI4
dir_hoi4 = os.path.join(
    os.environ.get("HOME","~/"),
    ".steam/steam/steamapps/common/Hearts of Iron IV/common/units/"
)

ret = hoi4tools.parser.parse_dir(dir_hoi4)
pprint(ret)


print("####################")
# parsing of a whole directory + filtering data relevant to production
import hoi4tools.parser
import hoi4tools.filters
import os
from pprint import pprint

# path to one of the directory of HOI4
dir_hoi4 = os.path.join(
    os.environ.get("HOME","~/"),
    ".steam/steam/steamapps/common/Hearts of Iron IV/common/units/"
)

ret = hoi4tools.filters.filter_production(
    hoi4tools.parser.parse_dir(dir_hoi4)
)
pprint(ret)


