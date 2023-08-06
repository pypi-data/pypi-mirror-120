import delta.tables as dt

def _jdbc_createconnection(_user, _passw, _url, _driver):
  """
  Create a connection to a specified database (connected through JDBC) and return the connection as a result.
  Authentication is based on the user and password combination for the specified database.
  The database is identified through the URL.
  """
  # Create the connection to the database
  _conn = (spark.read.format('jdbc')
           .option('url', _url)
           .option('driver', _driver)
           .option('user', _user)
           .option('password', _passw)
          )
  return _conn

def oracle_executequery(_query, _user, _passw, _url):
  """
  Execute a SQL query on the specified Oracle database and return the result as a PySpark dataframe.
  Authentication is based on the user and password combination for the specified database.
  The database is identified through the URL.
  
  Additional keyword arguments are not yet supported
  
  Ensure that the Oracle JDBC driver is installed on your cluster (https://mvnrepository.com/artifact/com.oracle.jdbc)
  """
  # Create the connection to the database
  _conn = _jdbc_createconnection(_user, _passw, _url, _driver='oracle.jdbc.driver.OracleDriver')
  
  # Provide additional settings for an Oracle database
  _conn = _conn.option('oracle.jdbc.timezoneAsRegion', 'false')
    
  # Execute the query and return the result as a dataframe
  return _conn.option('query', _query).load()

def oracle_readtable(_table, _user, _passw, _url, **kwargs):
  """
  Read a SQL table from the specified Oracle database and return the result as a PySpark dataframe.
  Authentication is based on the user and password combination for the specified database.
  The database is identified through the URL.
  
  Additional keyword arguments for the JDBC connection (https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html) are supported
  
  Ensure that the Oracle JDBC driver is installed on your cluster (https://mvnrepository.com/artifact/com.oracle.jdbc)
  """
  # Create the connection to the database
  _conn = _jdbc_createconnection(_user, _passw, _url, _driver='oracle.jdbc.driver.OracleDriver')
  
  # Provide additional settings for an Oracle database
  _conn = _conn.option('oracle.jdbc.timezoneAsRegion', 'false')
    
  # Work with the additional keyword arguments
  for _key, _val in kwargs.items():
    _conn = _conn.option(_key, _val)  
    
  # Read the table and return the result as a dataframe
  return _conn.option('dbtable', _table).load()

def postgres_executequery(_query, _user, _passw, _url):
  """
  Execute a SQL query on the specified Postgres database and return the result as a PySpark dataframe.
  Authentication is based on the user and password combination for the specified database.
  The database is identified through the URL.
  
  Additional keyword arguments are not yet supported
  
  Ensure that the PostgreSQL JDBC driver is installed on your cluster (https://jdbc.postgresql.org/)
  """
  # Create the connection to the database
  _conn = _jdbc_createconnection(_user, _passw, _url, _driver='org.postgresql.Driver')
      
  # Execute the query and return the result as a dataframe
  return _conn.option('query', _query).load()

def postgres_readtable(_table, _user, _passw, _url, **kwargs):
  """
  Read a SQL table from the specified Postgres database and return the result as a PySpark dataframe.
  Authentication is based on the user and password combination for the specified database.
  The database is identified through the URL.
  
  Additional keyword arguments for the JDBC connection (https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html) are supported
  
  Ensure that the PostgreSQL JDBC driver is installed on your cluster (https://jdbc.postgresql.org/)
  """
  # Create the connection to the database
  _conn = _jdbc_createconnection(_user, _passw, _url, _driver='org.postgresql.Driver')
    
  # Work with the additional keyword arguments
  for _key, _val in kwargs.items():
    _conn = _conn.option(_key, _val)  
    
  # Read the table and return the result as a dataframe
  return _conn.option('dbtable', _table).load()

def bigquery_readtable(_project, _dataset, _table, **kwargs):
  """
  Read the BigQuery table from the specified dataset in the corresponding project (identified as {_project}.{_dataset}.{_table}).  Returns the data as a PySpark dataframe.
  
  Additional keyword arguments for the BigQuery connection (https://github.com/GoogleCloudDataproc/spark-bigquery-connector) are supported
  
  **Note**: Defaults to the project of the Service Account being used
  """
  
  # Create the connection to the BigQuery table
  _conn = spark.read.format('bigquery')
  
  # Work with the additional keyword arguments
  for _key, _val in kwargs.items():
    _conn = _conn.option(_key, _val)
    
  # Read the BiqQuery table and return the result as a dataframe
  return _conn.load('{}.{}.{}'.format(_project, _dataset, _table))

def bigquery_writetable(_df, _project, _dataset, _table, _writemode='append', **kwargs):
  """
  Write out the PySpark dataframe _df to the specified BigQuery table.  The BigQuery table is identified as {_project}.{_dataset}.{_table}.
  
  Different types of writing behaviour are supported:
  _writemode='overwrite':  overwrites existing BigQuery table with the dataframe
  _writemode='append':     appends the dataframe to the existing BigQuery table (default)
  
  Additional keyword arguments for the BigQuery connection (https://github.com/GoogleCloudDataproc/spark-bigquery-connector) are supported
  
  **Note**: A temporary GcsBucket is almost always required!
  """
  assert _writemode in ['overwrite', 'append'], 'Illegal _writemode specified'
  
  # Create the connection to the BigQuery table
  _conn = _df.write.format('bigquery')
  
  # Work with the additional keyword arguments
  for _key, _val in kwargs.items():
    _conn = _conn.option(_key, _val)
  
  # Set writemode
  _conn = _conn.mode(_writemode)
  
  # Write out the dataframe
  _conn.save('{}.{}.{}'.format(_project, _dataset, _table))
  return

def delta_readfile(_path):
  """
  Read the Delta Lake file stored at the specified path.
  
  Additional keyword arguments are not supported
  """
  return spark.read.format('delta').load(_path)

def delta_writefile(_df, _path, _writemode='append', _cond=None, _partition=False, _partcols=[]):
  """
  Write out the PySpark dataframe _df to the specified _path as a Databricks Delta Lake file.
  
  Different types of writing behaviour are supported:
  _writemode='overwrite':  overwrites existing Delta Lake files at the specified _path with the dataframe
  _writemode='append':     appends the dataframe to the existing Delta Lake files (default)
  _writemode='insert_all': appends the dataframe to the existing Delta Lake files and inserts complete rows for all matches rows according to the condition
  _writemode='insert_none':appends the dataframe to the existing Delta Lake files and inserts *no* rows for all matches rows according to the condition
  _writemode='insert_specific': not yet supported
  
  **Note**: the original table needs to be referred as "table" for the insert condition and the new table as "updates"
  
  Setting the _partitioning of the Delta Lake file during overwrite write mode is supported.  Any existing partitioning will be automatically followed during all other write modes.
  _partition: boolean to indicate whether partitioning is needed
  _partcols:  list of column names to be used for partitioning
  """
  assert _writemode in ['overwrite', 'append', 'insert_all', 'insert_none'], 'Illegal _writemode specified'
  
  # Overwrite behaviour
  if _writemode == 'overwrite':
    _conn = (_df.write
             .format('delta')
             .mode('overwrite')
             .option('overwriteSchema', 'true')
            )
    # Include partioning
    if _partition:
      _conn = _conn.partitionBy(_partcols)
    
    _conn.save(_path)
    return
  
  # Append behaviour
  elif _writemode == 'append':
    _conn = (_df.write
             .format('delta')
             .mode('append')
            )
    _conn.save(_path)
    return
  
  # WhenMatchedInsertAll behaviour
  elif _writemode == 'insert_all':
    # Connect to the existing table
    _table = dt.DeltaTable.forPath(spark, _path)
    
    # Create an execution plan
    _plan = (_table
             .alias('table')
             .merge(_df.alias('updates'), _cond)
             .whenMatchedUpdateAll()
             .whenNotMatchedInsertAll()
            )
    _plan.execute()
    return
  
  # WhenMatchedInsertNone behaviour  
  elif _writemode == 'insert_none':
    # Connect to the existing table
    _table = dt.DeltaTable.forPath(spark, _path)
    
    # Create an execution plan
    _plan = (_table
             .alias('table')
             .merge(_df.alias('updates'), _cond)
             .whenNotMatchedInsertAll()
            )
    _plan.execute()
    return
