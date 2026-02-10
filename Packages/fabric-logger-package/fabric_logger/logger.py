import notebookutils
from datetime import datetime
from notebookutils import mssparkutils
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

class FabricLogger:
    def __init__(self, eventhouse_uri, database="Logging", table="NotebookLogging"):
        self.logs = []
        self.eventhouse_uri = eventhouse_uri
        self.database = database
        self.table = table
        self.notebook_name = notebookutils.runtime.context.get("currentNotebookName")
        self.workspace_name = notebookutils.runtime.context.get("currentWorkspaceName")

    # Add records to the message log
    def log(self, log_level, log_message, log_trace=None):
        self.logs.append({
            "log_datetime": datetime.now(), 
            "workspace_name": self.workspace_name,
            "notebook_name": self.notebook_name,
            "log_level": log_level,
            "log_message": log_message,
            "log_trace": log_trace
        })

    # Write the message log to Eventhouse
    def write_to_eventhouse(self):
        # Define schema
        schema = StructType([
            StructField("log_datetime", TimestampType(), nullable=False),
            StructField("workspace_name", StringType(), nullable=True),
            StructField("notebook_name", StringType(), nullable=True),
            StructField("log_level", StringType(), nullable=False),
            StructField("log_message", StringType(), nullable=False),
            StructField("log_trace", StringType(), nullable=True)
        ])
        
        # Column order (must match schema order)
        columns_in_order = [
            "log_datetime", 
            "workspace_name",
            "notebook_name", 
            "log_level", 
            "log_message", 
            "log_trace"
        ]

        try:
            # Create spark session
            spark = SparkSession.builder.getOrCreate()
            
            # Create dataframe with schema, then select to ensure order
            df = spark.createDataFrame(self.logs, schema=schema).select(columns_in_order)
            
            # Write to Eventhouse
            df.write.format("com.microsoft.kusto.spark.synapse.datasource").\
            option("kustoCluster", self.eventhouse_uri).\
            option("kustoDatabase", self.database).\
            option("kustoTable", self.table).\
            option("accessToken", mssparkutils.credentials.getToken(self.eventhouse_uri)).\
            option("tableCreateOptions", "CreateIfNotExist").mode("Append").save()
        except Exception as e:
            print(f"Error writing to Eventhouse: {e}")