def parts_to_curl(method, endpoint, headers, data=None):
    ignored_headers = (
        'Accept', 'Accept-Encoding', 'Connection', 'Content-Type', 'Content-Length', 'User-Agent')
    headers = ["'{0}:{1}'".format(k, v) for k, v in headers.items() if
               k not in ignored_headers]
    headers = " -H ".join(sorted(headers))

    curl_parameters = ['curl']
    for prefix, values in (('-X', method.upper()),
                           ('-H', headers),
                           ('-d', "'%s'" % data if data else None),
                           ):
        if values:
            curl_parameters.append('%s %s' % (prefix, values))
    curl_parameters.append("'%s'" % endpoint)
    command = " ".join(curl_parameters)
    return command


def to_curl(request):
    if not request:
        return 'No request'
    return parts_to_curl(request.method,
                         request.url,
                         request.headers,
                         request.body if getattr(request, 'body') else None)
