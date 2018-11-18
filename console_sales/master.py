import subprocess
import pandas as pd
import re
import matplotlib.pyplot as plt


def parse(number):
	try:
		return float(number)
	except:
#		print 'Trying to parse: ', number
		orignumber = number
		number = number.split()
		if len(number) == 2 and (number[1] == 'million' or number[1] == 'millionGT' or number[1] == 'million(estimate)'):
			try: 
				out = float(number[0])*10**6
#				print 'Turning ', orignumber, 'into: {0}'.format(out)
				return out
			except:
				splitted = number[0].split(u'\u2013')
				if len(splitted) == 2:
					out =  (float(splitted[0])+float(splitted[1]))*.5*10**6
#					print number[0], 'looks like an average? returning {0}'.format(out)
					return out
				else:		
					if number[0][0] == '>':
						outval = float(number[0][1:])*10**6
#						print 'greater than... turning ', orignumber, ' into ', outval
						return outval
					else:
#						print 'no method for million thing', number
						return number
			else:
				print "Can't turn ", number[0], " into a float"
				return number
		else:
			if len(orignumber.split(',')) == 2:
#				print 'Looks like two numbers, probably a date, returning the first out of', orignumber
				return float(orignumber.split(',')[0])
			else:				
				print 'No parse method for: ', orignumber
				return number

def populate(names, makers, years, sales):
	outdict = {}
	dim = len(names)
	for q in range (1,dim):
		console = names[q]
		maker = makers[q]
		year = parse(years[q])
		sale = parse(sales[q])
		if maker not in outdict:
			outdict[maker] = []
		outdict[maker].append([console, sale, year])
	return outdict

print "Getting info from wikipedia..."
webpage = subprocess.check_output(['curl https://en.wikipedia.org/wiki/List_of_best-selling_game_consoles'], shell=True)
html = pd.read_html(webpage, encoding='utf-8')

consoles = html[1]
handhelds = html[2]

console_names = consoles[0]
console_makers = consoles[1]
console_years = consoles[2]
console_sales = consoles[3]

handheld_names = handhelds[0]
handheld_makers = handhelds[1]
handheld_years = handhelds[2]
handheld_sales = handhelds[3]

print "Parsing console data..."
console_dict = populate(console_names, console_makers, console_years, console_sales)
print 'Parsing handheld data...'
handheld_dict = populate(handheld_names, handheld_makers, handheld_years, handheld_sales)

print 'console dict: '
for q in console_dict:
	print q, console_dict[q]

print '\n\n\n'
print 'handheld dict: ', handheld_dict
for q in handheld_dict:
	print q, handheld_dict[q]

plt.subplot(2, 1, 1)
plt.ylim([0, None], auto=True)
plt.xlabel('Year of release')
plt.ylabel('Unit sales thus far (millions)')
colors = ['purple',  'yellow', 'orange', 'pink', 'brown', 'teal', 'maroon', 'peru', 'orchid']
colordict = {'Nintendo':'red', 'Sega': 'blue', 'Sony':'black', 'Microsoft':'green'}
for maker in console_dict.keys():
	num_consoles = len(console_dict[maker])
	console_dict[maker] = sorted(console_dict[maker], key = lambda x: x[2])
	if num_consoles > 0:
		try:
			color = colordict[maker]
		except:
			color = colors[0]
			colordict[maker] = color
			colors.remove(color)		
		dummy = 0	
		for console_entry in console_dict[maker]:
			console, sale, year = console_entry
			sale /=10**6
			if dummy == 0:
				plt.scatter(year, sale, color = color, label = '{0}'.format(maker))
			else:
				plt.plot([year, prev_point[0]], [sale, prev_point[1]], color = color)
			plt.text(year, sale, u'{0}'.format(console))
			prev_point = [year, sale]
			dummy = 1
		plt.legend(loc=2, fancybox=True, framealpha=0.5)
plt.subplot(2,1,2)
plt.ylim([0, None], auto=True)
plt.xlabel('Year of release')
plt.ylabel('Unit sales thus far (millions)')
for maker in handheld_dict.keys():
	num_consoles = len(handheld_dict[maker])
	handheld_dict[maker] = sorted(handheld_dict[maker], key = lambda x: x[2])
	if num_consoles > 0:
		try:
			color = colordict[maker]
		except:
			color = colors[0]
			colors.remove(color)	
		dummy = 0
		for console_entry in handheld_dict[maker]:
			console, sale, year = console_entry
			sale /=10**6
			if dummy == 0:
				plt.scatter(year, sale, color = color, label = '{0}'.format(maker))
			else:
				plt.plot([year, prev_point[0]], [sale, prev_point[1]], color = color)
			prev_point = [year, sale]
			dummy = 1
			plt.text(year, sale, u'{0}'.format(console))
		plt.legend(loc=2, fancybox=True, framealpha=0.5)
plt.savefig('video_game_graph.png', dpi=400)
plt.show()
