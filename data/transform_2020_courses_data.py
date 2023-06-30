import pandas as pd
import numpy as np
import json

file_name = 'data\\2020-courses.json'

# Sample data in json file
"""{
  "ACCT 2301": {
    "id": 0,
    "name": "Introductory Financial Accounting",
    "hours": "3",
    "description": "An introduction to financial reporting designed to create an awareness of the accounting concepts and principles for preparing the three basic financial statements: the income statement, balance sheet, and statement of cash flows. The course is designed to benefit all students who will be future users of accounting information. Students must earn a grade of C or better to progress to ACCT 2302. ",
    "inclass": "3",
    "outclass": "0",
    "period": "S",
    "prerequisites": []
  }, ...
}"""

# After fixing the data
"""{
  {
    "id": 0,
    "classes": "ACCT 2301",
    "name": "Introductory Financial Accounting",
    "hours": "3",
    "description": "An introduction to financial reporting designed to create an awareness of the accounting concepts and principles for preparing the three basic financial statements: the income statement, balance sheet, and statement of cash flows. The course is designed to benefit all students who will be future users of accounting information. Students must earn a grade of C or better to progress to ACCT 2302. ",
    "inclass": "3",
    "outclass": "0",
    "period": "S",
    "prerequisites": []
  }, ...
}"""

 # Fix the JSON data
fixed_data = []

# Load the JSON data
json_data = json.load(open(file_name))

for key, value in json_data.items():
    value["code"] = key
    fixed_data.append(value)




# Convert the fixed data back to JSON
fixed_json = json.dumps(fixed_data)

# Make a dataframe from the JSON data
df = pd.read_json(fixed_json)

#Remove all columns except for classes, and name
df = df[['code', 'name']]

# Make the column "classes" the second column
cols = df.columns.tolist

# Reorder the rows so that course code in order with prefix CS, EE, ME, CE, SE, FIN, BIO, MATH, ACCT, PSY
sorting_order = {
    'ECS': 1,
    'ENGR': 1,
    'CS': 2,
    'EE': 3,
    'MECH': 4,
    'CE': 5,
    'SE': 6,
    'ITSS': 7,
    'STAT': 7,
    'FIN': 7,
    'MATH': 8,
    'PHYS': 9,
    'BIO': 10,
    'ACCT': 10,
    'FIN': 11,
    'PSY': 12,
    'CHEM': 13,
    
}

#Extract the prefix from the course code
df['prefix'] = df['code'].str.extract(r'([A-Z]+)')

#Sort the datafram by prefix from sorting_order
df = df.sort_values(by='prefix', key=lambda x: x.map(sorting_order))


# Save the dataframe to a CSV file
df.to_csv('data\\courses.csv', index=False)
