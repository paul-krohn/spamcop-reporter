#!/usr/bin/env python3
import sys
import json

from spamcop.response import SpamCopHtmlPFinder, SpamCopMetaFinder

# p_finder = SpamCopHtmlPFinder(verbose=1)
# p_finder.feed(open(sys.argv[1]).read())
# print(json.dumps(p_finder.paragraphs, indent=4))
meta_finder = SpamCopMetaFinder()
meta_finder.feed(open(sys.argv[1]).read())
# print(json.dumps(meta_finder.metas, indent=4))
refresh = meta_finder.detect_meta_refresh()

print("the refresh is: %s" % refresh)
