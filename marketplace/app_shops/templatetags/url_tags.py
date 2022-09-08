from django import template

register = template.Library()


@register.simple_tag
def paginate(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)

    return url


@register.simple_tag
def ordering(value, field_name, direction, urlencode=None):
    url = '?sort={}&type={}'.format(value, direction)

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != 'sort' and p.split('=')[0] != 'type', querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '?{sorting}&{urlencode}'.format(
            sorting="sort={}&type={}".format(value, direction),
            urlencode=encoded_querystring,
        )

    return url
