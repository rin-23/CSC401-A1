#!/bin/bash
FILES=./tweets/*
for f in $FILES
do
	python twtt.py $f ./generated_twt/`basename $f`.twt
done