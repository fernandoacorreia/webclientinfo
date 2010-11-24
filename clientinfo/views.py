import datetime
import uuid

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

import settings
from models import Url, UrlAccess, UrlAccessData

def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365*24*60*60  #one year
    else:
        max_age = days_expire*24*60*60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() +
                                         datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires)
    return response

def info(request, url_id):
    url = get_object_or_404(Url, pk=int(url_id))
    access_history = url.urlaccess_set.order_by('created_on').all()
    return render_to_response('info.html', {'url': url, 'access_history':
                                            access_history})

def save_access_data(access, key, value):
    if not value: return
    access_data = UrlAccessData()
    access_data.access = access
    access_data.key = key
    access_data.value = value
    access_data.save()

def save_meta_access_data(access, field, request):
    value = request.META.get(field, None)
    if value:
        save_access_data(access, field, value)

def go(request, url_id):
    url = get_object_or_404(Url, pk=int(url_id))

    access = UrlAccess()
    access.url = url
    access.save()

    meta_fields = ['HTTP_USER_AGENT', 'REMOTE_ADDR', 'REMOTE_HOST',
                   'HTTP_ACCEPT_ENCODING', 'HTTP_ACCEPT_LANGUAGE',
                   'HTTP_ACCEPT_CHARSET', 'HTTP_VIA', 'HTTP_COOKIE',
                   'HTTP_LOGNAME', 'HTTP_USER', 'HTTP_USERNAME']
    for field in meta_fields:
        save_meta_access_data(access, field, request)

    old_cookie = request.COOKIES.get('UUID', None)
    if old_cookie:
        save_access_data(access, 'UUID_COOKIE(old)', old_cookie)
    else:
        new_cookie = uuid.uuid4()
        save_access_data(access, 'UUID_COOKIE(new)', new_cookie)

    response = render_to_response('go.html', {'url': url})
    if not old_cookie:
        set_cookie(response, 'UUID', new_cookie)
    return response
