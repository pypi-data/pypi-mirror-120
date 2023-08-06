# arequest

![PyPI](https://img.shields.io/pypi/v/arequest) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/arequest) ![Downloads](https://pepy.tech/badge/arequest) ![PyPI - License](https://img.shields.io/pypi/l/arequest)

_arequest is an async HTTP client for Python, with more customization._


## Warnning

**The arequest is experimental for now, please do not use for production environment.**


## Installation

`pip install arequest`  

> *python3.8 or higher version is required.*  


## Quickstart

``` python
import asyncio
import arequest

async def main():
    r = await arequest.get("https://httpbin.org/get")
    print(r.headers)
    print(r.status_code)
    print(r.encoding)
    print(r.text)
    print(r.json())

asyncio.run(main())
```

### Passing Parameters In URLs

``` python
await arequest.get("https://httpbin.org/get", params={"test": "123"})
```

### POST

``` python
await arequest.post("https://httpbin.org/post", data={"key": "value"})
```

- POST a JSON

``` python
await arequest.post("https://httpbin.org/post", json={"key": "value"})
```

### Binary Response Content

``` python
r.content
```

### Custom Headers

``` python
headers = {
    "user-agent": "test"
}
await arequest.get("https://httpbin.org/get", headers=headers)
```

> *`headers` could override any original request header, including `Host`*


### Cookies

``` python
await arequest.get("https://httpbin.org/cookies", cookies={"test": "test"})
```

### Unverified SSL Cert

``` python
await arequest.get("https://httpbin.org/get", verify=False)
```


## TODO
- [ ] Timeouts
- [ ] aiodns
- [ ] file upload
- [ ] socks5
- [ ] Keep-alive session
- [ ] http2
- [ ] redirect
- [ ] raw request

