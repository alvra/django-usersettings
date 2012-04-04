from math import log
from django.utils.timesince import timesince





def format_filesize(user, size, none_is_zero=True):
    if size is None:
        if none_is_zero:
            size = 0
        else:
            raise ValueError("Function format_filesize got None")
    elif not isinstance(size, (int,long)):
        size = int(unicode(size))   # because Django passes us special string types
    format = (u'%(size).1f %(unit)s', u'%(size)d %(unit)s')
    pfx_base = 1024   # = 2**10
    pfx = {
        1000 : (
            '',
            'k',
            'M',
            'G',
            'T',
            'P',
            'E',
            'Z',
            'Y',
        ),
        1024 : (
            '',
            'Ki',
            'Mi',
            'Gi',
            'Ti',
            'Pi',
            'Ei',
            'Zi',
            'Yi',
        ),
    }
    # specify the minimal factor of a prefix the size must have
    # in order to be used
    # EG: setting this to 0.9 will cause only values > 0.9 kB
    # to be considered for the 'kb' unit (but values > 0.9 MB will get the 'MB' unit)
    pfx_min = 1.0

    # start of calculation
    if size == 0:
        return format[1] % dict(size=0, unit='B')
    if size < 0.9 * pfx_base:
        return format[1] % dict(size=size, unit='B')
    # start expensive calculation
    n = 1
    while size > pfx_min*(pfx_base**(n+1)) and n < len(pfx[pfx_base])-1:
        n += 1
    # parse to return string
    prefixed_size = size/float(pfx_base**n)
    if prefixed_size.is_integer():
        return format[1] % dict(size=prefixed_size, unit=u'%sB'%pfx[pfx_base][n])
    else:
        return format[0] % dict(size=prefixed_size, unit=u'%sB'%pfx[pfx_base][n])


def round_float(value, places):
    value = round(value, places)
    if places <= 0:
        return int(value+0.5)
    s = str(value)
    if places > 0:
        try:
            e = s.index('.')+places+1
            if e < len(s):
                return s[:e]
            else:
                return s + '0'*(e-len(s))
        except ValueError:
            return s+'.'+'0'*places


def format_datetime(user, datetime):
    return '<span title="%s">%s</span>' % (datetime.strftime('%a %b %d, %Y %H:%M:%S %z'), timesince(datetime)) # TODO: create something better
    return datetime.strftime('%a %b %d, %Y %H:%M:%S %z')

def format_date(user, date):
    return date

def format_time(user, time):
    return time

def format_user(user, otheruser):
    "Formats otheruser into a string the ways user wants them."
    return otheruser.username
