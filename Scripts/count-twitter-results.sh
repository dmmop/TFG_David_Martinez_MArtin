#!/bin/bash
#Devuelve el numero de filas que hay en los ficheros
filas_nongeo="hdfs dfs -cat twitter/single/nongeo.tweets.csv | wc -l"
filas_geo="hdfs dfs -cat twitter/single/geo.tweets.csv | wc -l"

echo "Evaluando tweets totales..."
tweets_geo=$(eval $filas_geo)
#tweets_geo=$(($tweets_geo - 1))
tweets_nongeo=$(eval $filas_nongeo)
#tweets_nongeo=$(($tweets_geo -1))
echo "Tweets con geolocalizados: $tweets_geo"
echo "Tweets sin localizar: $tweets_nongeo"