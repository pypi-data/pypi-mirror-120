## **About**

[![PyPI version](https://badge.fury.io/py/mojang.svg)](https://badge.fury.io/py/mojang)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mojang?style=flat-square)

[![Read the Docs](https://img.shields.io/readthedocs/mojang?style=flat-square)](https://mojang.readthedocs.io/en/latest/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/summer/mojang/blob/master/LICENSE/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mojang?style=flat-square)

[**Documentation**](https://mojang.readthedocs.io/en/latest/)

`Mojang` is a Python package for accessing Mojang's services. It serves as a simple wrapper around Mojang's [API](https://wiki.vg/Mojang_API)
and can be used to get name drop dates, convert UUIDs, and much more. It does not, however, currently support authentication or login features.

## **Installation**

**Python 3.6 or higher is required.**

To install the library, you can just run the following console command:

```
python -m pip install mojang
```

## **Quickstart**

```py
import time
from mojang import MojangAPI

uuid = MojangAPI.get_uuid("Notch")

if not uuid:
    print("Notch does not exist.")
else:
    print("Notch's UUID is", uuid)
    profile = MojangAPI.get_profile(uuid)
    print("Notch's skin URL is", profile.skin_url)

servers = MojangAPI.get_blocked_servers()
print(f"There are {len(servers)} blocked servers on Minecraft.")

drop_timestamp = MojangAPI.get_drop_timestamp("Notch")

if not drop_timestamp:
    print("Notch is not dropping")
else:
    seconds = drop_timestamp - time.time()
    print(f"Notch drops in {seconds} seconds")
```
To see a complete list of methods, read the [**documentation**](https://mojang.readthedocs.io/en/latest/).

