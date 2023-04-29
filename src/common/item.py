import csv


def get_return_obj(active, buy_price):
    return {
        'active': active,
        'buy_price': buy_price
    }


def get_item():
    with open('orders.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            return get_return_obj(row[0], row[1])

        return get_return_obj(0, 0)


def put_item(active, price):
    print('put_item', price)
    with open('orders.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([active, price])

