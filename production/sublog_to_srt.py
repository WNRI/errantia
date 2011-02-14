#!/usr/bin/env python
# vim: fileencoding=utf-8 ts=4 sw=4 sws=4 expandtab :

from __future__ import print_function
import sys
import csv
import codecs
from datetime import datetime, timedelta
from pysrt import SubRipFile, SubRipItem, SubRipTime

TIMEFORMAT = '%Y-%m-%d %H:%M:%S.%f'
START_TIME = None

try:
    sublog = open(sys.argv[1], 'rb')
except IndexError:
    print("Usage: {0} <sub.log> > file.srt".format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

srt = SubRipFile(eol='\n', encoding='utf-8')
i = 1

for line in sublog:
    line = line.split(",", 1)
    if (line[0] and line[0][0] == '-'):
        if (START_TIME == None and line[0][:8] == '- start '):
            START_TIME = datetime.strptime(line[0], '- start ' + TIMEFORMAT +
            '\n')
        continue

    no = datetime.strptime(line[0], TIMEFORMAT) - START_TIME
    if (abs(no) > timedelta(1)):
        print("\nCan't go over a day in a subtitle! Delete non-used lines in" + \
                " log.\nLet there only be one '- start' line at the top of" + \
                " the log-file.")
        sys.exit(1)

    time = SubRipTime.from_ordinal(no.seconds*1000 + no.microseconds*0.001)

    item = SubRipItem(i, start=time, end=time + 30*1000,
            text=unicode(line[1], 'utf-8'))
    srt.append(item)
    i += 1

srt.clean_indexes()
#srt.save(path=sys.stdout)

for line in srt:
    sys.stdout.write(unicode(line).encode('utf-8'))
