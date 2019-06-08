from view import comment, get_cities, view, del_comment, stat, stat_city

patterns = [
    (r'^/comment/$', 'comment.html', comment),
    (r'^/view/$', 'view.html', view),
    (r'^/stat/$', 'stat.html', stat),
    (r'^/stat/(?P<region_id>[0-9]+)/$', 'stat_city.html', stat_city),

    # API
    (r'^/api/get_cities/$', None, get_cities),
    (r'^/api/delete_comment/$', None, del_comment),
]