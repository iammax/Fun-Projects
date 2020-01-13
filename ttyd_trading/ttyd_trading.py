#This script will tell you if there are any profitable buy low/sell high transactions you can make given a starting town and ending town in Paper Mario: The Thousand Year Door


def combine_strs(strs):
    temp = ''
    for word in strs:
        temp += '{0} '.format(word)
    return temp[:-1]

def get_buydata():

    buyprices = open('ttyd_buydata.txt', 'r')
    buyprices = buyprices.readlines()
    buydata = {}
    num_buylines = len(buyprices)
    buylines_counter = 0

    while buylines_counter < num_buylines:
        here = buyprices[buylines_counter]
        if len(here) == 1:
            current_shop = buyprices[buylines_counter + 1][:-1]
            buylines_counter += 2
            buydata[current_shop] = {}
        else:
            current_item = here.split()[:-2]
            current_item = combine_strs(current_item)
            price = int(here.split()[-2])
            buylines_counter += 1
            buydata[current_shop][current_item] = price
    return buydata


def get_selldata():
    sellprices = open('ttyd_selldata.txt', 'r')
    sellprices = sellprices.readlines()
    temp = []
    for line in sellprices:
        if line.split()[-1][-3:] != 'png':
            temp.append(line)
    sellprices = temp
    numlines = len(sellprices)
    counter = 0
    selldata = {}
    shop_order = {}
    shop_number = 0
    shops_done = 0
    while counter < numlines:
        here = sellprices[counter].split()
        if len(here) > 3:
            shops_done = 1
        if shops_done == 0:
            shop_name = combine_strs(here)
            shop_order[shop_number] = shop_name
            shop_number += 1
            selldata[shop_name] = {}
            counter += 1
        else:
            line_len = len(here)
            item_name = here[0:line_len-10]
            item_name = combine_strs(item_name)
            prices = here[line_len-10:]
            for shopnumber in shop_order:
                shop_name = shop_order[shopnumber]
                selldata[shop_name][item_name] = prices[shopnumber]
            counter += 1
    return selldata

buydata = get_buydata()
selldata = get_selldata()


for buy_shop in buydata:
    print 'Buying in shop: {0}'.format(buy_shop)
    for item in buydata[buy_shop]:
        buy_price = int(buydata[buy_shop][item])
        for sell_shop in selldata:
            sell_price = int(selldata[sell_shop][item])
            if sell_price > buy_price:
                print 'Sell {2} in shop: {0} for a profit of {1}'.format(sell_shop, sell_price-buy_price, item)
    print ''
