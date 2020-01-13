import pandas as pd
import requests
import subprocess
import numpy as np
import matplotlib.pyplot as plt

def parse(thing, factor):
    try:
        return float(thing)*factor
    except:
        try:
            b = thing.replace(',', '')
            return float(b[0:-3])*factor
        except:
            print ("Can't make float: {0}".format(thing))
        print ("Can't make float: {0}".format(thing))
        return -1.2345

def get_data(url, name, tablenums, cols):
    page = requests.get(url)
    text = page.text
    tables = pd.read_html(text)
    table = np.vstack([tables[q].drop_duplicates() for q in tablenums])
    out_x = []
    out_y = []
    for row in table:
#        print row
#        print cols[0], cols[1]
        try:
            x = parse(row[cols[0]], 1)
            y = parse(row[cols[1]], 10**-3)
            if y != -1.2345 and x!= -1.2345:
                out_x.append(x)
                out_y.append(y)
        except:
            print ("Can't convert something in this row to float or int: ", row)
    return [out_x, out_y]
        
    
urls = {'Brooklyn':['https://en.wikipedia.org/wiki/Demographics_of_Brooklyn', [1, 2], [0, 1]], 'Manhattan':['https://en.wikipedia.org/wiki/Demographics_of_Manhattan', [1,2], [0,1]], 'Queens':['https://en.wikipedia.org/wiki/Demographics_of_Queens', [0], [0, 3]], 'The Bronx':['https://en.wikipedia.org/wiki/Demographics_of_the_Bronx', [0], [0, 1]], 'Staten Island':['https://en.wikipedia.org/wiki/Demographics_of_Staten_Island', [2], [0,1]]}

for url in urls:
    print ('Parsing location: {0} located at URL: {1}'.format(url, urls[url][0]))
    data = get_data(urls[url][0], url, urls[url][1], urls[url][2])
    print( data)
#    print len(data[0]), len(data[1])
    plt.plot(data[0], data[1], label = url)
    
plt.legend(loc=2)
plt.ylabel('Population (thousands)')
plt.xlabel('Year')
plt.ylim([0, None])
plt.show()
