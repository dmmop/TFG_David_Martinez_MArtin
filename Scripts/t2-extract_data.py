#!/usr/bin/env python
# IMPORTS
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, SparkSession

from time import time
from datetime import datetime
import subprocess

# Constants
APP_NAME = "Clean tweets"
HDFS = 'hdfs://david-hdp:9000/'
LOG_FILE = '/home/david/logs/spark-twitter.log'
NON_PROCESS_TWEETS='flume/tweets/*'
TIME_NOW = "{:%Y-%m-%d__%H-%M-%S}".format(datetime.now())
GEO_TWEETS = "twitter/geo/tweets-{1}-{0}.csv"
NONGEO_TWEETS = "twitter/nongeo/tweets-{1}-{0}.csv"

SQL_GEO="SELECT * FROM (SELECT place.country_code AS country, lang, IF(LOCATE(' javascript ', text)>0, 1, 0) AS javascript, IF(LOCATE(' c# ', text)>0, 1, 0) AS cSharp, IF(LOCATE(' java ', text)>0, 1, 0) AS java, IF(LOCATE(' android ', text)>0, 1, 0) AS android, IF(LOCATE(' python ', text)>0, 1, 0) AS python, IF(LOCATE(' c++ ', text)>0, 1, 0) AS cplus, IF(LOCATE(' php ', text)>0, 1, 0) AS php, IF(LOCATE(' ios ', text)>0, 1, 0) AS ios, IF(LOCATE(' c ', text)>0, 1, 0) AS c, IF(LOCATE(' html ', text)>0, 1, 0) AS html FROM tweets WHERE text NOT LIKE 'RT @%' AND place.country != 'None' ) AS filter WHERE javascript > 0 OR cSharp > 0 OR java > 0 OR android > 0 OR python > 0 OR cplus > 0 OR php > 0 OR c > 0 OR html > 0"
SQL_NONGEO="SELECT * FROM (SELECT lang, IF(LOCATE(' javascript ', text)>0, 1, 0) AS javascript, IF(LOCATE(' c# ', text)>0, 1, 0) AS cSharp, IF(LOCATE(' java ', text)>0, 1, 0) AS java, IF(LOCATE(' android ', text)>0, 1, 0) AS android, IF(LOCATE(' python ', text)>0, 1, 0) AS python, IF(LOCATE(' c++ ', text)>0, 1, 0) AS cplus, IF(LOCATE(' php ', text)>0, 1, 0) AS php, IF(LOCATE(' ios ', text)>0, 1, 0) AS ios, IF(LOCATE(' c ', text)>0, 1, 0) AS c, IF(LOCATE(' html ', text)>0, 1, 0) AS html FROM tweets WHERE text NOT LIKE 'RT @%') AS filter WHERE javascript > 0 OR cSharp > 0 OR java > 0 OR android > 0 OR python > 0 OR cplus > 0 OR php > 0 OR c > 0 OR html > 0"

# Vars
start = time()
#end = 0
count = 0
count_GEO = 0
count_NONGEO = 0

def delete_file(path):
	subprocess.call(['hdfs', 'dfs', '-rm', '-f', '-R', path])


def save_csv(result, name, count):
	name = name.format(TIME_NOW, count)
	result.write.csv(name, mode='overwrite')

def process_tweets(sqlQuery):
	sc.setJobGroup('SQL', 'Filtering using sql')
	_result = spark.sql(sqlQuery)
	sc.setJobGroup('SQL', 'Counting SQL results')
	_count = _result.count()
	return _result, _count

def save_log():
	sc.setJobGroup('Save csv', 'Saving results on csv')
	m, s = divmod((end - start), 60)
	with open(LOG_FILE, 'w') as f:
		f.write("Log from clean-twitter at {:%Y-%m-%d %H-%M-%S}:\n".format(datetime.now()))
		f.write("\tTotal time: {:.2f}M {:.2f}s\n".format(m,s))
		f.write("\tTweets processed:{}\n".format(count))
		f.write("\tTweets with country:{}\n".format(count_GEO))
		f.write("\tTweets without country:{}\n".format(count_NONGEO))

def main(spark):
	global count, count_GEO, count_NONGEO
	sc.setJobGroup('Reading', 'Reading flume/tweets/*')
	df = spark.read.json(NON_PROCESS_TWEETS)
	sc.setJobGroup('Count', 'Counting brute tweets')
	count=df.count()
	sc.setJobGroup('SQL', 'Registering temporal table (tweets)')
	df.registerTempTable("tweets")
	sc.setJobGroup('Geo', 'Processing geo tweets')
	result_GEO, count_GEO = process_tweets(SQL_GEO)
	result_NONGEO, count_NONGEO = process_tweets(SQL_NONGEO)

	save_csv(result_GEO, GEO_TWEETS, count_GEO)
	save_csv(result_NONGEO, NONGEO_TWEETS, count_NONGEO)
	delete_file(NON_PROCESS_TWEETS)


if __name__ == "__main__":
	# Configure OPTIONS
	conf = SparkConf().setAppName(APP_NAME)
	conf = conf.setMaster("spark://david-hdp:7077")
	sc = SparkContext(conf=conf)
	spark = SparkSession(sc)
	
	# Execute main function
	main(spark)
	global end
	end = time()
	save_log()

	m, s = divmod((end - start), 60)

	print("\n\n\n\n\n\n \
		Total time: {:.2f}M {:.2f}s\n \
		Tweets processed:{}\n\
		Tweets with country:{}\n \
		Tweets without country:{}\n \
		\n\n\n\n\n".format(m, s, count, count_GEO, count_NONGEO))
