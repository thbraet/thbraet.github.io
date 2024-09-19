# Databricks notebook source
# MAGIC %md
# MAGIC # Framework 

# COMMAND ----------

# MAGIC %md
# MAGIC # How To
# MAGIC * Clone this notebook
# MAGIC * Make sure to name the notebook exactly the same as the intended table name, following the naming conventions specified in https://fluviusso.atlassian.net/wiki/spaces/ATHENA/pages/57409573/Naming+Conventions
# MAGIC * Optionally, in Cmd 5 you can create a view containing the incremental changes from a specific table
# MAGIC * Insert your satellite or link query in Cmd 6. Make sure to also add an incremental load version if you specified a table changes view in Cmd 5.
# MAGIC * Different query options are available:
# MAGIC   * Satellite:
# MAGIC     * Write your satellite query
# MAGIC     * Make sure to add a business ID. The business ID has to align to the following naming convention : h_*EntityName*_BID.
# MAGIC     * In case of transactional data: include the BID & name the transaction identifier column 'TRANSACTION'  
# MAGIC     * Once your query is finished, the BDV framework will automatically add metadata to your table + create the accompanying hub
# MAGIC   * Link satellite:
# MAGIC     * Write your link satellite query
# MAGIC     * Make sure to add the business IDs of the 2 tables between there is a link. The business IDs have to align to the following naming convention : h_*EntityName*_BID
# MAGIC         * Exception in the above naming convention: when the same entity is referenced twice, you can apply the following: h_*EntityName*_*SubEntityName*_BID. 
# MAGIC     * In case of transactional data: include the BIDs & name the transaction identifier column 'TRANSACTION'  
# MAGIC     * Once your query is finished, the BDV framework will automatically add metadata to your table + create the accompanying link
# MAGIC   * Link:
# MAGIC     * Write your link query
# MAGIC     * Make sure to only add the business IDs of the 2 tables between there is a link. The business IDs have to align to the following naming convention : h_*EntityName*_BID.
# MAGIC         * Exception in the above naming convention: when the same entity is referenced twice, you can apply the following: h_*EntityName*_*SubEntityName*_BID. 
# MAGIC     * Any additional columns included in the query will be ignored.
# MAGIC     * Once your query is finished, the BDV framework will automatically add metadata to your table
# MAGIC * You need to include the catalog environment suffix as a spark variable. So e.g. dataplatform_a becomes dataplatform_${bdv.environment}
# MAGIC * Once your query is finished, or if you want to test the results, you can click the 'Run all'-button in the top right corner of the notebook

# COMMAND ----------

# MAGIC %md
# MAGIC ## Get environment

# COMMAND ----------

# DBTITLE 1,Initialize catalog
# Import packages
from datetime import datetime
import random
import string
import pyspark.sql.functions as F

# Widgets
dbutils.widgets.removeAll()

dbutils.widgets.text("Key vault", "dbss-001", "Key vault")
dbutils.widgets.dropdown("Is Loaded Incrementally", "FALSE", ["TRUE", "FALSE"])

# Initialize key vault
key_vault = dbutils.widgets.get("Key vault")
is_loaded_incrementally = dbutils.widgets.get("Is Loaded Incrementally")
databricks_environment = dbutils.secrets.get(scope = key_vault, key = 'databricks-environment')[1]
# Query read environment
bdv_environment = dbutils.secrets.get(scope = key_vault, key = 'databricks-bdv-environment')[1]
spark.conf.set("bdv.environment", bdv_environment)
spark.conf.set("loaded.incrementally", is_loaded_incrementally)

print(f"Your query will contain results of tables from environment " + bdv_environment)

# Functions
def get_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def get_table_changes(table: str):
    # Get table changes
    notebook_name = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get().split('/')[-1]
    view_name = table.split('.')[2] + '_tc_view'
    certificate_id = table.split('.')[2][0:8]
    runtime = str(spark.sql(f"""select max(LastRunTime) from dataplatform_{databricks_environment}.process.ods_load_journal where CertificateID = '{certificate_id}' and BDVNotebook = '{notebook_name}'""").head()[0])
    updateRuntime = str(spark.sql(f"""select max(timestamp) from (DESCRIBE HISTORY {table})""").head()[0])
    if runtime == 'None':
        df_changes = spark.table(table)
    else:
        df_changes = spark.read.format("delta").option("readChangeFeed", "true").option("startingTimestamp", runtime).table(table)
        df_changes = df_changes.filter(F.col("_commit_timestamp") > runtime)
        df_changes = df_changes.filter(F.col('_change_type').isin('insert', 'update_postimage'))
    print('Created incremental view: ' + view_name)
    # Update staging ods load journal, except for dev env -> this logic is only used during daily loads
    if databricks_environment != 'o':
        spark.sql(f"INSERT INTO dataplatform_{databricks_environment}.process.ods_load_journal VALUES('{certificate_id}', '{updateRuntime}', '{notebook_name}')")
    return df_changes.createOrReplaceTempView(view_name)

# COMMAND ----------

# DBTITLE 1,Get table changes
# In this command, you can create views containing only the incremental changes after the last run.
# The function get_table_changes('catalog.schema.table') will return the following view 'table_tc_view'
# Example: get_table_changes('dataplatform_' + bdv_environment + '.ods.003_0027_nemesis_nemcel') returns '003_0027_nemesis_nemcel_tc_view'
get_table_changes()

# COMMAND ----------

# MAGIC %md
# MAGIC # Business

# COMMAND ----------

# MAGIC %md
# MAGIC ## Intro
# MAGIC
# MAGIC | Item          | Value |
# MAGIC | ------------- | ---- |
# MAGIC | Stakeholders  |      |
# MAGIC | Categorie     | RDV / BDV / DWH - SCD1 / DWH - SCD2 (DWH gegenereerd) / DWH - SCD2 (CMS/ODS source historiek)     |
# MAGIC | Granulariteit |      |
# MAGIC | Jira item     |      |

# COMMAND ----------

# MAGIC %md
# MAGIC ## History
# MAGIC
# MAGIC |Actie|Omschrijving|User|DEV datum|Jira ticket|
# MAGIC |-----|------------|----|------------|-----------|
# MAGIC |     |            |    |            |           |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Logica

# COMMAND ----------

# MAGIC %md
# MAGIC ### Stap x - Finale query

# COMMAND ----------

# DBTITLE 0,Query
# MAGIC %sql
# MAGIC -- insert your business query here
# MAGIC -- Full load
# MAGIC -- SELECT
# MAGIC -- FROM
# MAGIC -- WHERE ${loaded.incrementally} = 'FALSE'
# MAGIC
# MAGIC -- UNION ALL
# MAGIC
# MAGIC -- Incremental load
# MAGIC -- SELECT
# MAGIC -- FROM
# MAGIC -- WHERE ${loaded.incrementally} = 'TRUE'

# COMMAND ----------

# MAGIC %md
# MAGIC # Framework

# COMMAND ----------

# MAGIC %md
# MAGIC ## Export result

# COMMAND ----------

alias = get_random_string(10) + datetime.utcnow().strftime('%f')[:-3]

_sqldf.alias(alias).createOrReplaceGlobalTempView(alias)
dbutils.notebook.exit(alias)
