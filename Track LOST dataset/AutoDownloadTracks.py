import urllib.request as urlRequest
# Fixed Variables
counter = 0
dayArray = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17'
,'18','19','20','21','22','23','24','25','26','27','28','29','30','31']
monthArray = ['01','02','03','04','05','06','07','08','09','10','11','12',]
# Tunable Variables
currentDay = dayArray[0]
currentMonth = monthArray[0]
currentYear = 2012
pointerDay = 0
pointerMonth = 0

while counter < 365:
	#template url: http://lost.cse.wustl.edu/static/camera/001/001_2013-08-07_11-00-01/tracks.txt
	# getting the complete url ready
	diff = 365 - counter
	print("Days Left: " + str(diff))
	try:
		filename = '001_' + str(currentYear) + currentMonth + currentDay + '.txt'
		url = 'http://lost.cse.wustl.edu/static/camera/001/001_' + str(currentYear) + '-' + currentMonth + '-' + currentDay + '_11-00-01/tracks.txt'
		#Scrape it!
		print(url)
		content = urlRequest.urlretrieve(url, filename)
	except:
		pass
	counter += 1

	if (pointerMonth == 3) or (pointerMonth == 5) or (pointerMonth == 8) or (pointerMonth == 10):
		if currentDay == '30':
			currentDay = dayArray[0]
			pointerMonth += 1
			currentMonth = monthArray[pointerMonth]
			pointerDay = 0			
		else:
			pointerDay += 1
			currentDay = dayArray[pointerDay]
			
	elif pointerMonth == 1:
		if currentYear%4 == 0 and currentDay == '28':#leapyear
			pointerDay += 1
			currentDay = dayArray[pointerDay]
		elif currentYear%4 == 0 and currentDay == '29':#reset to 01 if day ends for the month
			currentDay = dayArray[0]
			pointerDay = 0
			pointerMonth += 1
			currentMonth = monthArray[pointerMonth]
		elif (currentYear%4 != 0) and (currentDay == '28'): #Non Leap year
			currentDay = dayArray[0]
			pointerDay = 0
			pointerMonth += 1
			currentMonth = monthArray[pointerMonth]
		else:
			pointerDay += 1
			currentDay = dayArray[pointerDay]
	else: #for 31 days month
		if currentDay == '30':
			pointerDay += 1
			currentDay = dayArray[pointerDay]
		elif currentDay == '31':
			currentDay = dayArray[0]
			pointerDay = 0
			pointerMonth += 1
			currentMonth = monthArray[pointerMonth]
		else:
			pointerDay += 1
			currentDay = dayArray[pointerDay]

	
	#if year ends?
	if (pointerMonth == 11) and (pointerDay == 30):
		currentYear -= 1
		pointerMonth = 0
		pointerDay = 0
		currentMonth = monthArray[pointerMonth]
		currentDay = dayArray[pointerDay]
