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
    
    if len(clothing_types) > 0:
        query['clothing_type'] = {'$in': clothing_types}

    print(query)

fetch_clothing(max_price = 30.0, gender = 'men', clothing_types = ['pants', 'shirt', 'dresses'])
