#!/bin/bash

for filename in /home/david/git/*.gz; do
	printf "\nExtracting $filename..."
	gzip -d $filename
	printf "...SUCCESFULLY"
done