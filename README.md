# pynec-examples

This repository contains the following PyNEC models:

* Inverted-V antenna for 20 meters (invv-\*.py)
* ZS6BKW antenna for 40/20/17/12/10 meters (zs6bkw-\*.py)

Usage:

```
mkvirtualenv pynec-examples
pip3 install -r requirements.txt

# Inverted-V
./invv-azimuth.py && ./invv-elevation.py && ./invv-swr.py
open invv-*.png

# ZS6BKW
time ./zs6bkw-optimize.py | tee zs6bkw-result.txt
```
