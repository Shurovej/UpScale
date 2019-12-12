#! /bin/bash

# find many *.jpg files
#   then for each file name call `split2.py` with that file name in argumnent
#   then all output of each `split2.py` call send to `teech2.py`

find pic -name '*.jpg' 2>/dev/null \
  | xargs -L 1  ./split2.py \
  | ./teech2.py
