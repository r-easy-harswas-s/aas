import os

from pyspark.sql import SparkSession
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType
from pyspark.sql.types import DoubleType

PATH = '/Users/juliet/data/PAMAP2_Dataset/Protocol'

SENSOR_FIELDS = ['temp', 'acc-x-16', 'acc-y-16', 'acc-z-16',
          'acc-x-6', 'acc-y-6', 'acc-z-6'
          'gy-x', 'gy-y', 'gy-z',
          'mag-x', 'mag-y', 'mag-z',
          'orient-x', 'orient-y', 'orient-z']

SENSOR_LOCATIONS = ['hand', 'chest', 'ankle']

ALL_SENSOR_FIELDS = [StructField('-'.join([loc, name]), DoubleType(), True)
                     for loc in SENSOR_LOCATIONS
                     for name in SENSOR_FIELDS]

SCHEMA = StructType([StructField('subjectid', DoubleType(), True),
                     StructField('ts', DoubleType(), True),
		             StructField('activityID', DoubleType(), True),
                     StructField('hr', DoubleType(), True)] + ALL_SENSOR_FIELDS)


spark = SparkSession.builder \
    .appName('PAMAP2 Activity Recognition') \
    .getOrCreate()
sc = spark.sparkContext

# Get all file names in data dir
files = [os.path.split(file)[1] for file in os.listdir(PATH)]
print("XXX{}XXX".format(",".join(files)))

def process_text_line(line, subject_id):
    assert isinstance(line, basestring)
    elems = line.split(' ')
    return tuple(float(elem) for elem in elems)
    

def process_single_file(file_name):
    txt_lines = sc.textfile(os.path.join(PATH, file_name))
    observations = txt_lines.map
    subject_id = float(file_name[9:10])
    # map and create a bunch of tuples of observations
    observations = txt_lines.map(lambda line: process_text_line(line,
                                                              subject_id))
    

