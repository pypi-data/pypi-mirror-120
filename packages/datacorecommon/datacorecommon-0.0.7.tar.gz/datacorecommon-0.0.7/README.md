# datacore-common
The Datacore-common repository contains wrapper functions to work with various PySpark APIs and is maintained by the Data Core team.  These wrapper functions provide an easy method to interface or to interact with PySpark Dataframes.  They are built on top of the standard pyspark functionality and are extended with the Databricks Delta functionality.

__Note__: It is assumed that this package is installed on a Databricks cluster.  Support is also provided for a local installation. 

## Requirements
- Python version >= 3.6
- PySpark version >= 3.1
- Delta-Spark version >= 1.0.0
- Relevant JDBC drivers (Oracle, Postgres, ...)

__Note__: Databricks ensures that the correct version of Python, PySpark and Delta-Spark are included on their clusters by including these in their runtime environments.  The JDBC drivers need to be installed on the Databricks cluster but are not available out of the box.

__Note__: Links to the JDBC drivers are:
- [Postgres](https://jdbc.postgresql.org/)
- [Oracle](https://mvnrepository.com/artifact/com.oracle.jdbc)

## Installation
To install at Databricks simply run `pip install --upgrade datacorecommon`.  This can be done at a workspace level, a cluster level, and a notebook level ([see documentation page](https://docs.databricks.com/libraries/index.html#python-environment-management)).

To install locally run  `pip install --upgrade datacorecommon[local]`.  This ensures that PySpark and Delta-Spark are installed on your local machine.  __The JDBC drivers are not provided.__

## Known issues
__oracle_readtable__
- Partitioning the JDBC connection on a timestamp column: this requires you to provide the following kwarg `sessionInitStatement="ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'`.

__bigquery_writetable__
- A temporaryGcsBucket is needed for writing to a BigQuery table: while not mandatory for the function to operate, it is required in the backend and can be set by providing the following kwarg `temporaryGcsBucket='my-bucket-name'`.