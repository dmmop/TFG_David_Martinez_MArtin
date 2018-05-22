#!/bin/bash

#Comrpueba si existe el fichero (0) o si no existe (1)
check_nongeo="hdfs dfs -test -e twitter/single/nongeo.tweets.csv"
#Crea un csv con todos los datos de la carpeta twitter/nongeo/*
create_nongeo="hdfs dfs -getmerge twitter/nongeo/* nongeo.csv"
#Añade cada linea del fichero nongeo.csv al fichero nongeo.tweets.csv
merge_nongeo_local="cat nongeo.csv >> nongeo.tweets.csv"
#Suma el fichero 'nongeo.csv' del local al 'twitter/single/nongeo.tweets.csv' del hdfs
merge_nongeo_dfs="hdfs dfs -appendToFile nongeo.csv twitter/single/nongeo.tweets.csv"
#Sube el fichero a hdfs
upload_nongeo="hdfs dfs -put nongeo.tweets.csv twitter/single/"

#Los mismos comandos anteriores con otro path
check_geo="hdfs dfs -test -e twitter/single/geo.tweets.csv"
create_geo="hdfs dfs -getmerge twitter/geo/* geo.csv"
merge_geo_local="cat geo.csv >> geo.tweets.csv"
merge_geo_dfs="hdfs dfs -appendToFile geo.csv twitter/single/geo.tweets.csv"
upload_geo="hdfs dfs -put geo.tweets.csv twitter/single/"

#Elimina todos los ficheros generados durante el proceso
remove_resources_geo="hdfs dfs -rm -r twitter/geo/*"
remove_resources_nongeo="hdfs dfs -rm -r twitter/nongeo/*"
remove_nongeo_local="rm nongeo.csv"
remove_nongeo_tweets="rm nongeo.tweets.csv"
remove_geo_local="rm geo.csv"
remove_geo_tweets="rm geo.tweets.csv"

#Devuelve el numero de filas que hay en los ficheros
filas_nongeo="hdfs dfs -cat twitter/single/nongeo.tweets.csv | wc -l"
filas_geo="hdfs dfs -cat twitter/single/geo.tweets.csv | wc -l"


# Evaluar si los ficheros existen
exist_nongeo=$(eval $check_nongeo)
exist_geo=$(eval $check_geo)

echo "Evaluando fichero nongeo"
#Si el fichero no existe
if [ '$exist_nongeo' == '1' ]; then
		echo "No existe fichero ../nongeo.tweets.csv"
		echo "Creando cabecera de csv"
		echo 'lang,javascript,cSharp,java,android,python,cplus,php,ios,c,html' > nongeo.tweets.csv
		echo "Exportando archivos del hdfs"
		eval $create_nongeo
		echo "Creando fichero local con cabecera"
		eval $merge_nongeo_local
		echo "Subiendo fichero ../nongeo.tweets.csv"
		eval $upload_nongeo
		echo "fichero nongeo subido"
		echo "Eliminando ficheros auxiliares nongeo..."
		eval $remove_nongeo_local
		eval $remove_nongeo_tweets
		eval $remove_resources_nongeo
		echo "Ficheros auxiliares nongeo borrados!"
# Si existe el fichero
else
		echo "Existe el fichero ../nongeo.tweets.csv"
		echo "Exportando datos del hdfs"
		eval $create_nongeo
		echo "Uniendo fichero local con hdfs"
		eval $merge_nongeo_dfs
		echo "Eliminando fichero auxiliar..."
		eval $remove_nongeo_local
		eval $remove_resources_nongeo
		echo "Fichero geo auxilair, eliminado!"
fi

echo "Evaluando fichero geo"
if [ '$exist_geo' == '1' ]; then
		echo "No existe fichero ../geo.tweets.csv"
		echo "Creando cabecera de csv"
		echo 'country, lang,javascript,cSharp,java,android,python,cplus,php,ios,c,html' > geo.tweets.csv
		echo "Exportando datos del hdfs"
		eval $create_geo
		echo "Creando fichero local con cabecera"
		eval $merge_geo_local
		echo "Subiendo fichero ../geo.tweets.csv"
		eval $upload_geo
		echo "fichero ../geo.tweets.csv subido"
		echo "Eliminando ficheros geo auxiliares..."
		eval $remove_geo_local
		eval $remove_geo_tweets
		eval $remove_resources_geo
		echo "Ficheros auxilaires geo, eliminados!"
else
		echo "Existe el fichero ../geo.tweets.csv"
		echo "Exportando datos del hdfs"
		eval $create_geo
		echo "Uniendo fichero local con hdfs"
		eval $merge_geo_dfs
		echo "Eliminando fichero geo auxiliar..."
		eval $remove_geo_local
		eval $remove_resources_geo
		echo "Fichero geo auxiliar, eliminado!"
fi

echo "Evaluando tweets totales:"
tweets_geo=$(eval $filas_geo)
#tweets_geo=$(($tweets_geo - 1))
tweets_nongeo=$(eval $filas_nongeo)
#tweets_nongeo=$(($tweets_geo -1))
echo "Tweets con geolocalizados: $tweets_geo"
echo "Tweets sin localizar: $tweets_nongeo"
echo "fin"
