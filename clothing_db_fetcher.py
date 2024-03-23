def fetch_clothing(min_price=None, max_price=None, gender=None, clothing_types=[]):
    query = {}
    if min_price:
        query['price'] = {'$gte': min_price}
    if max_price:
        if 'price' in query:
            query['price'].update({'$lte': max_price})
        else:
            query['price'] = {'$lte': max_price}
    if gender:
        query['gender'] = gender
    
    for clothing_type in clothing_types:

