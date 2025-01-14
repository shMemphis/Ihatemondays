items = [
    {'name': 'apples', 'price': 10},
    {'name': 'oranges', 'price':10},
    {'name': 'durian','price' :50}
]

total = 0

for product in items:
    price = product['price']
    total = total+price


count = len(items)


average = total/count