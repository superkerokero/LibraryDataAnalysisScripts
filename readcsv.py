#!/usr/bin/env python3
# coding: utf-8

"The scipt that handles csv input."
import csv
import sys


def readData(file):
    "Read data from given csv file and store it in a list."
    try:
    	# Open csv file with shift-jis encoding for Japanese support.
        with open(file, encoding='shift-jis') as csvfile:
            csvdata = csv.reader(csvfile, dialect='excel')
            rawdata = dict()
            for row in csvdata:
            	for rank, data in enumerate(row):
            		try:
            			rawdata[rank].append(data)
            		except:
            		    rawdata[rank] = list()
            		    rawdata[rank].append(data)
            return rawdata
    except IOError:
        sys.exit("File \'{0}\' open failed!".format(file))


if __name__ == "__main__":
    rawdata = readData("libsample.csv")
    print(rawdata[2][100])
