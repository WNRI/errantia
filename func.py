# AGPL 3.0+
# Odin Hørthe Omdal <odin.omdal@gmail.com>
# vim: encoding=utf8 ts=4 sws=4 expandtab

def mkslug(name):
    return name                   \
      .lower()                    \
      .replace(" ", "-")          \
      .encode("ascii", 'ignore')

