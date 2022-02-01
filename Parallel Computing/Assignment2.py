# Databricks notebook source
## Dillon Dugan
# Loading and Cleaning Data
from pyspark.sql.types import StructType, StructField, FloatType, StringType
import pyspark.sql.functions as f

sensorSchema = StructType( 
                          [StructField('US1', FloatType(), True), 
                           StructField('US2', FloatType(), True),
                           StructField('US3', FloatType(), True),
                           StructField('US4', FloatType(), True),
                           StructField('US5', FloatType(), True),
                           StructField('US6', FloatType(), True),
                           StructField('US7', FloatType(), True),
                           StructField('US8', FloatType(), True),
                           StructField('US9', FloatType(), True),
                           StructField('US10', FloatType(), True),
                           StructField('US11', FloatType(), True),
                           StructField('US12', FloatType(), True),
                           StructField('US13', FloatType(), True),
                           StructField('US14', FloatType(), True),
                           StructField('US15', FloatType(), True),
                           StructField('US16', FloatType(), True),
                           StructField('US17', FloatType(), True),
                           StructField('US18', FloatType(), True),
                           StructField('US19', FloatType(), True),
                           StructField('US20', FloatType(), True),
                           StructField('US21', FloatType(), True),
                           StructField('US22', FloatType(), True),
                           StructField('US23', FloatType(), True),
                           StructField('US24', FloatType(), True),
                           StructField('Class', StringType(), True),
                        ])
sensor_reading = spark.read.format('csv').option('header',False).schema(sensorSchema).load('dbfs:///FileStore/tables/sensor_readings_24.data')
sensor_reading.select([f.count(f.when(f.isnan(col),col)).alias(col) for col in sensor_reading.columns]).show()

# COMMAND ----------

# Build a Pipeline for data transformation then split train and test data
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml import Pipeline

vecAssem = VectorAssembler(inputCols=['US1','US2','US3','US4','US5','US6','US7','US8','US9','US10','US11','US12','US13','US14','US15','US16','US17','US18','US19','US20','US21','US22','US23','US24'],outputCol='features')
predIndexer = StringIndexer(inputCol='Class',outputCol='label')
rf = RandomForestClassifier(numTrees=500,maxDepth=5,seed=42)
myStages = [vecAssem,predIndexer]

pipeline = Pipeline(stages=myStages)

sensor_pipe = pipeline.fit(sensor_reading)
sensor_data = sensor_pipe.transform(sensor_reading)
training, testing = sensor_data.randomSplit([0.7,0.3],seed=42)
print(training.groupBy('label').count().take(5))

# COMMAND ----------

# Apply random forest model to training data and evaluate the model
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

rf = RandomForestClassifier(numTrees=500,maxDepth=5,seed=42)
rf_model = rf.fit(training)
predTrain = rf_model.transform(training)

evaluator = MulticlassClassificationEvaluator(labelCol='label',predictionCol='prediction')
accuracy = evaluator.evaluate(predTrain)
print('Accuracy = ',accuracy)

predTest= rf_model.transform(testing)
evaluator = MulticlassClassificationEvaluator(labelCol='label',predictionCol='prediction')
accuracy = evaluator.evaluate(predTest)
print('Accuracy = ',accuracy)

# COMMAND ----------

# Streaming testing data on random forest model
testing.write.format('parquet').option('header',True).mode('overwrite').save('FileStore/tables/testing/')
testing.createOrReplaceTempView('testing')

# Source
sourceStream = spark.readStream.format('parquet').option('header',True).option('maxFilesPerTrigger',1).schema(sensorSchema).load('dbfs:///FileStore/tables/testing')

# Query
sensorPiping = sensor_pipe.transform(sourceStream)
predictions = rf_model.transform(sensorPiping)

# Sink
sinkStream = predictions.writeStream.format('memory').queryName('testResults').trigger(processingTime='10 seconds').start()


# COMMAND ----------

spark.sql('SELECT label,prediction FROM testResults').show()

# COMMAND ----------


