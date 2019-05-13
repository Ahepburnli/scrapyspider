

class VideoInfoTextPipeline(object):
    '''
        对数据进行处理
    '''
    def process_item(self, item, spider):
        if 'views' not in dict(item).keys():
            return item
        views = item.get('views','0')
        if ',' in views:
            item['views'] = int(''.join(views.split(',')))
        else:
            item['views'] = int(views)
        likes = item.get('likes','0')
        if ',' in likes:
            item['likes'] = int(''.join(likes.split(',')))
        else:
            item['likes'] = int(likes)
        comments = item.get('comments','0')
        if ',' in comments:
            item['comments'] = int(''.join(comments.split(',')))
        else:
            item['comments'] = int(comments)
        shares = item.get('shares','0')
        if ',' in shares:
            item['shares'] = int(''.join(shares.split(',')))
        else:
            item['shares'] = int(shares)
        return item