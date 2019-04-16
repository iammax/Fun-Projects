num_of_states_to_count = int(input('Count the top X states: ')) # calculates the population density of the USA only including the top X states. Excluding D.C. since it's all heavily urban
if num_of_states_to_count > 50 or num_of_states_to_count < 1:
	print ("There aren't {0} states, pick between 1 and 50".format(num_of_states_to_count))
	quit()

import requests
import pandas as pd

link = 'https://simple.wikipedia.org/wiki/List_of_U.S._states_by_population_density'
page = requests.get(link).text
pan = pd.read_html(page)
table = pan[3]
states = {}
for index in range (1,len(table)):
	try:
		rank = int(table[0][index])
		name = table[1][index]
		pop = float(table[2][index])
		area = float(table[3][index])
		density = float(table[4][index])
		if rank not in states:
			states[rank] = [name, pop, area, density]
	except:
		pass
pop = 0
area = 0
for rank in range (1, num_of_states_to_count+1):
	pop += states[rank][1]
	area += states[rank][2]
print ('Final density, in people/sq mile: ', pop/area)
