from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("ACE Python Spark SQL Connecter") \
    .config("spark.some.config.option", "ACE") \
    .getOrCreate()

## Parameters
# df: spark dataframe which cantains the data
# url: jdbc url - i.e: jdbc:sqlserver://url:portnumber
# database: Name of the database to write - i.e.: ace-db
# dbtable: schema and abd the name of the table - i.e.: dbo.dbs
# username: Username of the database
# password: Password of the user
def writeSQL(df, url, database, dbtable, username, password):
  r = df.write.mode("append") \
      .format("jdbc") \
      .option("url", url) \
      .option("database", database) \
      .option("dbtable", dbtable) \
      .option("user", username) \
      .option("password", password) \
      .save()
  return r

# url: jdbc url - i.e: jdbc:sqlserver://url:portnumber
# database: Name of the database to write - i.e.: ace-db
# dbtable: schema and abd the name of the table - i.e.: dbo.dbs
# username: Username of the database
# password: Password of the user
def readSQL(url, database, dbtable, username, password):
  r = spark.read \
    .format("jdbc") \
    .option("url", url) \
    .option("database", database) \
    .option("dbtable", dbtable) \
    .option("user", username) \
    .option("password", password) \
    .load()
  return r