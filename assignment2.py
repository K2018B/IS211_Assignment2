#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS 211 Assignment Week 2"""

import urllib2
import csv
import datetime
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help="Enter a URL linking to a .csv file")
args = parser.parse_args()

logging.basicConfig(filename='errors.log', level=logging.ERROR)
logger = logging.getLogger('assignment_week2')

def downloadData(url):
    """Opens a supplied URL link.
    Args:
        url(str): a website url string
    """
    datafile = urllib2.urlopen(url)
    return datafile

def processData(datafile):
    """import .csv datafile
    Args:
        datafile(file): A .csv file supplied by user or downloaded from a URL
    """
    readfile = csv.DictReader(datafile)
    newdict = {}

    for num, line in enumerate(readfile):
        try:
            born = datetime.datetime.strptime(line['birthday'], '%d/%m/%Y')
            newdict[line['id']] = (line['name'], born)
        except:
            logging.error('Error processing line #{} for ID# {}'.format(
                num, line['id']))
    return newdict

def displayPerson(id, personData):
    """Looks up the id number in a supplied dictionary, and returns the name and
       date of birth associated with the id number
        """
    idnum = str(id)
    if idnum in personData.keys():
        print 'Person #{} is {} with a birthday of {}'.format(
            id, personData[idnum][0],
            datetime.datetime.strftime(personData[idnum][1], '%Y-%m-%d'))
    else:
        print 'No user found with that ID.'

def main():
    """Combines downloadData, processData, and displayPerson into one program to
    be run from the command line.
    """
    if not args.url:
        raise SystemExit
    try:
        csvData = downloadData(args.url)
    except urllib2.URLError:
        print 'Please enter a valid URL.'
        raise
    else:
        personData = processData(csvData)
        chooseid = raw_input('Please enter an ID# for lookup:')
        print chooseid
        chooseid = int(chooseid)
        if chooseid <= 0:
            print 'Number equal to or less than zero entered. Exiting program.'
            raise SystemExit
        else:
            displayPerson(chooseid, personData)
            main()

if __name__ == '__main__':
    main()
