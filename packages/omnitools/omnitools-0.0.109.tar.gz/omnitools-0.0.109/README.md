# Omnitools

<badges>[![version](https://img.shields.io/pypi/v/omnitools.svg)](https://pypi.org/project/omnitools/)
[![license](https://img.shields.io/pypi/l/omnitools.svg)](https://pypi.org/project/omnitools/)
[![pyversions](https://img.shields.io/pypi/pyversions/omnitools.svg)](https://pypi.org/project/omnitools/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Miscellaneous functions written in short forms.</i>

# Hierarchy
```
omnitools
|---- encoding
|   |---- b64
|   |   |---- b64d()
|   |   |---- b64e()
|   |   |---- try_b64d()
|   |   '---- b64d_or_utf8e()
|   |---- file
|   |   '---- charenc()
|   '---- utf8
|       |---- utf8d()
|       |---- utf8e()
|       |---- try_utf8d()
|       '---- try_utf8e()
|---- hashing
|   |---- mac()
|   '---- sha512()
|---- rng
|   |---- randb()
|   |---- randi()
|   '---- randstr()
|---- stdout
|   '---- p()
'---- type
    |---- str_or_bytes
    |---- list_or_dict
    |---- key_pair_format
    |---- encryptedsocket_function
    '---- Obj()
```

# Example

## python
See `test`.