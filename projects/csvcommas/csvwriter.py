#!/usr/bin/env python3

import csv

# https://stackoverflow.com/questions/10373247/how-do-i-write-a-python-dictionary-to-a-csv-file
# my_dict0 = {"test": 1, "testing": 2}
# my_dict0 = {"test": 1, "testing": {'dependencies': None}}
# my_dict1 = {'aws': {'dependencies': None,
#                     'deployment': {'documentation': 'TBD', 'link': 'TBD'},
#                     'human_name': 'aws',
#                     'service_tier': 0,
#                     'slack': '#something'},
#            'core_api': {'dependencies': ['aws'],
#                     'deployment': {'documentation': 'TBD', 'link': 'TBD'},
#                     'human_name': 'core-api',
#                     'owner_handle': 'do_not_know',
#                     'service_tier': 1,
#                     'slack': '#api'}}

# with open('mycsvfile.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
#     w = csv.DictWriter(f, my_dict0.keys())
#     w.writeheader()
#     w.writerow(my_dict0)


my_dict = [{"col1": 1000, "col2": 2000}, {"col1": 3000, "col2": 4000}]
f = open('mycsvfile.csv','wb')
w = csv.DictWriter(f, my_dict.keys())
w.writerows(my_dict)
f.close()
