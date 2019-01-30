def readFile():
	outFile = open('modified_house_data.csv', 'w+')

	with open('house_data.csv') as fp:
		header = fp.readline()
		headerTokens = header.strip().split(', ')
		newHeader = headerTokens[0] + ',' + headerTokens[1] + ',' + headerTokens[2]
		print newHeader
		outFile.write(header)
		for line in fp:
			# strip, then split
			tokens = line.strip().split(', ')
			# print len(tokens)
			cleaned_last = tokens[2][:-1]
			newLine = tokens[0].replace('"',"") + "," + tokens[1] + "," + cleaned_last + '\n'
			outFile.write(newLine)
		outFile.close()


readFile()