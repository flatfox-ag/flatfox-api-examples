import json


def print_response(response, show_headers=False):
    """
    Helper to print a response nicely.
    """
    res = response
    req = res.request

    print '=' * 80
    print 'Request: {} {}'.format(req.method, req.url)

    if show_headers:
        print '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items())

    print u'Body: {}'.format(req.body)

    print '-' * 80
    print 'Response Status Code: {}'.format(res.status_code)

    if show_headers:
        print '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items())

    try:
        body = json.dumps(res.json(), indent=2)
    except ValueError:
        body = res.text
    finally:
        print u'Body: {}'.format(body)

    print '=' * 80
    print '\n'
