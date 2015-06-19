#!/usr/bin/env python3
import sys

from spamcop.response import SpamCopFinder
finder = SpamCopFinder()

refresh = finder.meta_refresh_seconds(open(sys.argv[1]).read())
print("the refresh is: %s" % refresh)
