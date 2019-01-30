def readFile():
	outFile = open('modified_crime_data.csv', 'w+')

	with open('crime_by_county.csv') as fp:
		header = fp.readline()
		headerTokens = header.strip().split(', ')
		# 0 has County, 1 has State_Code, 2 has Violent_Crime_total, 3 has Murder, 4 has Rape, 5: Robbery, 
		# 6: Assault, 9: Burglary, 10: Larcery-Theft, 11: Vehicle_Theft

		newHeader = headerTokens[0] + ',' + headerTokens[1] + ',' + headerTokens[2] + ',' + headerTokens[3] + ',' + headerTokens[4] + ',' + headerTokens[5] + ',' + headerTokens[6] + ',' + headerTokens[9] + ',' + headerTokens[10] + ',' + headerTokens[11] + '\n'
		print newHeader
		outFile.write(newHeader)
		# outFile.close() #TODO: remove this from here
		for line in fp:

			# strip, then split
			tokens = line.strip().split(',')
			State_Code_tokens = tokens[1].split(' ') # 1 should have the code
			tokens[1] = State_Code_tokens[1]

			# print tokens[1]
			# print tokens

			for x in xrange(0, len(tokens)):
				if tokens[x] == '-' or tokens[x] == '(NA)' or tokens[x] == '(X)':
					# print tokens
					tokens[x] = ''
			# print tokens
			# return
			
			newLine = tokens[0] + ',' + tokens[1] + ',' + tokens[2] + ',' + tokens[3] + ',' + tokens[4] + ',' + tokens[5] + ',' + tokens[6] + ',' + tokens[9] + ',' + tokens[10] + ',' + tokens[11] + '\n'
			# print newLine
			# return

			# return

			# print len(tokens)
			# cleaned_last = tokens[2][:-1]
			# newLine = tokens[0].replace('"',"") + "," + tokens[1] + "," + cleaned_last + '\n'
			outFile.write(newLine)
		outFile.close()


readFile()