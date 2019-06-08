from view import comment, get_cities, view, del_comment, stat, stat_city

patterns = [
    (r'^/comment/$', comment),
    (r'^/view/$', view),
    (r'^/stat/$', stat),
    (r'^/stat/(?P<id>[0-9]+)/$', stat_city),

    # API
    (r'^/api/get_cities/$', get_cities),
    (r'^/api/delete_comment/$', del_comment),
]