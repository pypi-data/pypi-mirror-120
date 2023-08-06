# Mojang

[![PyPI version](https://badge.fury.io/py/mojang.svg)](https://badge.fury.io/py/mojang)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mojang?style=flat-square)

[![Read the Docs](https://img.shields.io/readthedocs/mojang?style=flat-square)](https://mojang.readthedocs.io/en/latest/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/summer/mojang/blob/master/LICENSE/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mojang?style=flat-square)](https://pypistats.org/packages/mojang)

[**Documentation**](https://mojang.readthedocs.io/en/latest/)

`Mojang` is a Python package for accessing Mojang's services. It serves as a simple wrapper around Mojang's [API](https://wiki.vg/Mojang_API)
and can be used to convert UUIDs, get profile information, and much more. 

The library does not currently support authentication or login features.

## **Installation**

**Python 3.6 or higher is required.**

To install the library, you can just run the following console command:

```
python -m pip install mojang
```

## **Quickstart**

```py
from mojang import MojangAPI

uuid = MojangAPI.get_uuid("Notch")

if not uuid:
    print("Notch is not a taken username.")
else:
    print(f"Notch's UUID is {uuid}")

    profile = MojangAPI.get_profile(uuid)
    print(f"Notch's skin URL is {profile.skin_url}")
    print(f"Notch's skin model is {profile.skin_model}")
    print(f"Notch's cape URL is {profile.cape_url}")
```

To see a complete list of methods, read the [**documentation**](https://mojang.readthedocs.io/en/latest/).
