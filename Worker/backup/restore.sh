#!/bin/bash
if [ "$#" -ne 1 ]; then
	echo "Provide a backup as first argument"
	exit(1)
fi
mongorestore --gzip --archive="$1"
