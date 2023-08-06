
import time
import datetime


def unixToDatetime(epochTime):
	epochTime = int(epochTime)
	localTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epochTime))
	return localTime


def datetimeToUnix(ogDatetime):
	ogDatetime=datetime.datetime.strptime(ogDatetime, "%Y-%m-%d %H:%M:%S")
	unixTime = ogDatetime.strftime('%s')
	return unixTime


def strToDT(ogDTstr):
	format = "%Y-%m-%d %H:%M:%S"
	dt_object = datetime.datetime.strptime(ogDTstr, format)
	return dt_object


def addDays(ogDatetime, nDays):
	ogDtTypeStr = str(type(ogDatetime))
	if 'str' in ogDtTypeStr:	
		ogDatetime = strToDT(ogDatetime)
	newDate = ogDatetime + datetime.timedelta(days=nDays)
	return newDate


def subtractDays(ogDatetime, nDays):
	ogDtTypeStr = str(type(ogDatetime))
	if 'str' in ogDtTypeStr:
		ogDatetime = strToDT(ogDatetime)
	newDate = ogDatetime - datetime.timedelta(days=nDays)
	return newDate


def today():
	todayFull = datetime.datetime.now()
	todaySplit = str(todayFull).split(".")
	today = todaySplit[0]
	return today



