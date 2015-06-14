#!/usr/bin/env python3

import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--debug', dest="debug", action="store_true", default=False)
# in our infinite wisdom, this is how we handle the default use case of
# a list of positional arguments
parser.add_argument('spam_files', metavar='FILE', type=str, nargs='+',
                    help='a list of files')

args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)


from spamcop.client import SpamCopClient


client = SpamCopClient()
for spam_file in args.spam_files:
    client.report(path_to_spam_mail_file=spam_file)
