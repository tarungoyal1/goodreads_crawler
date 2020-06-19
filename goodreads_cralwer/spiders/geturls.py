from pymongo import MongoClient


def get_urls():
    client = MongoClient()
    db = client['books']
    col_bookurls = db['book_urls']
    url_list = []
    batch_size = 1000
    while 1:
        cursor = col_bookurls.find(filter={'status': 'pending'}).limit(batch_size)
        url_list.clear()
        for item in cursor:
            url_list.append(item['url'])
        yield url_list

if __name__ == '__main__':
    pass