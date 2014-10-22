# The main scraper, to be run on a daemon every hour.

# If there are new spills it writes them to an sqlite db
# and sends out a tweet.

import os
import sqlite3
from bs4 import BeautifulSoup as bs
import requests
from urllib2 import urlopen
from time import sleep

dir = os.path.dirname(__file__)
databasePath = os.path.join(dir, 'data/SpillLog.db')

db = sqlite3.connect(databasePath)

def getRecord(ID):
	# Returns a complete DB row
	cursor = db.cursor()
	query = "SELECT * FROM spills WHERE ID=?"
	cursor.execute(query, (ID,))
	return cursor.fetchone()

def writeRecord(spill):
	cursor = db.cursor()
	query = "INSERT INTO spills VALUES (?,?,?,?,?,?,?,?)"
	cursor.execute(query, (
		spill['ID'],
		spill['FACID'],
		spill['COMPANY_NAME'],
		spill['OPERATOR_NUMBER'],
		spill['DATE'],
		spill['LAT'],
		spill['LONG'],
		spill['COUNTY']
	))
	db.commit()

# def checkRecordExists(ID):
# 	# Returns true/false if id exists in DB
# 	cursor = db.cursor()
# 	query = "SELECT EXISTS(SELECT 1 FROM myTbl WHERE u_tag="tag" LIMIT 1);"

def runScrape():
	data = { 'itype':'spill', 'maxrec':25 }
	page = 'http://cogcc.state.co.us/cogis/IncidentSearch2.asp'
	r = requests.post(page, data=data)

	soup = bs(r.text)
	rows = soup.find_all('tr')[3:]

	baseURL = "https://cogcc.state.co.us/cogis/"

	for row in rows:
		facID = row.find('a')['href'].replace('FacilityDetail.asp?facid=','').replace('&type=SPILL OR RELEASE', '')
		docNum = row.find('a').get_text().strip()
		
		if getRecord(docNum) is None:
			try:
				spill = {}
				
				spill['ID'] = docNum
				spill['FACID'] = facID
				spill['DATE'] = row.find_all('td')[0].find('font').get_text().strip()
				spill['COMPANY_NAME'] = row.find_all('td')[4].find('font').get_text().strip()
				spill['OPERATOR_NUMBER'] = row.find_all('td')[3].find('font').get_text().strip()
				
				detailURL = baseURL+row.find('a')['href'].replace('&type=SPILL OR RELEASE', '&type=SPILL%20OR%20RELEASE')
				print detailURL
				detailPage = urlopen(detailURL).read()
				detailSoup = bs(detailPage)

				rows = detailSoup.find_all('tr')

				county = rows[5].find_all('td')[1].find('font').get_text().split('-')[0].strip().title()
				spill['COUNTY'] = county

				print county

				latlong = rows[6].find_all('td')[3].find_all('font')[0].text.strip()
				print latlong

				spill['LAT'] = latlong.split('/')[0]
				spill['LONG'] = latlong.split('/')[1]

				writeRecord(spill)
				
				##
				## Put any code you want to perform on newly reported
				## spills here!
				##
			
			except:
				pass

		else:
			print "Looks like there aren't any new spills to report. Hooray!"

while True:
	runScrape()
	sleep(600)


