# For start this programm need install Java.
# Next command make this.
#
# sudo add-apt-repository ppa:webupd8team/java
# sudo apt-get update
# sudo apt install openjdk-11-jdk
# java -version
# you see ->
# openjdk version "11.0.7" 2020-04-14
# OpenJDK Runtime Environment (build 11.0.7+10-post-Ubuntu-3ubuntu1)
# OpenJDK 64-Bit Server VM (build 11.0.7+10-post-Ubuntu-3ubuntu1, mixed mode, sharing)



from pyspark import SparkConf, SparkContext
import collections

conf = SparkConf().setMaster("local").setAppName("RatingsHistogram")
sc = SparkContext(conf = conf)

lines = sc.textFile("/home/al/MyProjects/Pyspark_Hadoop/ml-100k/u.data")
ratings = lines.map(lambda x: x.split()[2])
result = ratings.countByValue()

sortedResults = collections.OrderedDict(sorted(result.items()))
for key, value in sortedResults.items():
    print("%s %i" % (key, value))
