#To check if any pokemon's number is a palindrome AND their base stat total is a palindrome. Thanks to hoopsandhiphop on youtube for the idea

import requests
import progressbar

def palindrome(x):
	return str(x) == str(x)[::-1]

def numformat(num):
	if 0 < num < 10:
		return '00{0}'.format(num)
	elif 9 < num < 100:
		return '0{0}'.format(num)
	else:
		return str(num)

baseurl = 'https://www.serebii.net/pokedex-sm/'

outlines = []
for pokenum in progressbar.progressbar(range(810)):
	if palindrome(pokenum):
		url = baseurl + '{0}.shtml'.format(numformat(pokenum))
		page = requests.get(url)
		linestocheck = []
		for line in page.text.split('\n'):
			if 'Base Stats - Total:' in line:
				if line not in linestocheck:				
					linestocheck.append(line)
			if '<title>' in line:
				name = line.split()[0][7:]
		usedbsts = []
		for line in linestocheck:
			parsed = line.split()
			bst = parsed[-1][0:3]
			if bst not in usedbsts: 
				usedbsts.append(bst)
				if palindrome(bst):
					
					outlines.append('{0} checks! Stats = {1}, number = {2}'.format(name, bst, pokenum))
for line in outlines:
	print line
					
