# {un}swamp
## Description
{un}swamp is a python library to create Data Quality Checks that can be run against a pandas dataframe.
## Quick Examples
In the following quick example we show the basic concept of:
- defining a Check Suite (that holds all the checks to run against a dataset)
- defining a Check and add it to a Check Suite
- run the Check Suite against a dataset
- evaluate the Check Result
### Dataset
For this Quick Example we use an open dataset from the City of New York that contains the NYS Math Test Results by Grade - Citywide by Race-Ethnicity for the years 2006 - 2011. Further details about the dataset can be found here: https://data.cityofnewyork.us/api/views/825b-niea/. In the following section we'll see a code example that does the following steps:
- collect the data as pandas dataframe
- create a Check Suite
- add two different Checks to that suite (1 shall pass / 1 shall fail)
- run the Check Suite against the collected dataset
- evaluate the Check Result to hopefully see a pass rate of 50%
### Code
```python
import pandas as pd
from unswamp.objects.checks import CheckColumnsExists, CheckColumnValuesInSet
from unswamp.objects.core import CheckRun, CheckSuite

# We load the dataset into a pandas dataframe
data_file = "https://data.cityofnewyork.us/api/views/825b-niea/rows.csv?accessType=DOWNLOAD"
dataset = pd.read_csv(data_file)

# We generate a CheckSuite to add our checks to
meta_data={"owner": "me"}
suite = CheckSuite("NY-Math-Grades-CheckSuite", "NY-Math-Grades", meta_data)

# We generate a test that checks for columns in the dataset
# The columns are available so the check will be successful
columns = ["Grade", "Year", "Category"]
check = CheckColumnsExists("CHK-001-ColsExists", columns, active=True, meta_data=meta_data)
suite.add_check(check)

# We generate a test that checks if all distinct values in column Year are in the provided values
# The year 2011 is missing so the check will fail
column = "Year"
values = [2006, 2007, 2008, 2009, 2010]
check = CheckColumnValuesInSet("CHK-002-ColsValuesInSet", column, values, active=True, meta_data=meta_data)
suite.add_check(check)

# We run the suite against the dataset and print the pass rate
# The pass rate is expected to be 50% since 1 test is successful and one fails
check_run = suite.run(dataset, "manual-test-run")
print(f"passed - {check_run.pass_rate*100}%")
```
## Credits
[![security: bandit](https://img.shields.io/badge/module-python-blue.svg)](https://www.python.org/) [![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit) [![security: bandit](https://img.shields.io/badge/front_end-Bootstrap-purple.svg)](https://getbootstrap.com/) [![security: bandit](https://img.shields.io/badge/icon-Ary_Prasetyo-black.svg)](https://thenounproject.com/search/?q=swamp&i=1592639)

