# Mosaic Shapes


![Alt text](/examples/cranston.JPEG "Bryan Cranston")
![Alt text](/examples/trooper.JPEG "Storm Trooper")

Note: I am planning on converting this to Go in the near future, thus this repo will be largely unmaintained.

```python run.py ~/Desktop/og/bo.jpg -e 2000 -d -c 1; open /tmp/out.JPEG```

```
(shapes4) guppy:shapes dean$ python run.py -h
usage: run.py [-h] [-d] [-c {0,1,2}] [-a] [-r WORKING_RES] [-e ENLARGE]
              [-m MULTI] [-p POOL] [-o OUT]
              N [N ...]

Mosaic photos

positional arguments:
  N                     Photo path
optional arguments:
  -h, --help            show this help message and exit
  -d, --diamond         Use diamond grid instead of squares
  -c {0,1,2}, --color {0,1,2}
                        Specify color values
  -a, --analogous       Use analogous color
  -r WORKING_RES, --working_res WORKING_RES
                        Resolution to sample from
  -e ENLARGE, --enlarge ENLARGE
                        Resolution to draw
  -m MULTI, --multi MULTI
  -p POOL, --pool POOL
  -o OUT, --out OUT
  ```
