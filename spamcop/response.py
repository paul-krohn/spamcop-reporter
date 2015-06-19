from html.parser import HTMLParser
from bs4 import BeautifulSoup
import sys
import json


class SpamCopMetaFinder(HTMLParser):

    def __init__(self, verbose=0):
        self.metas = list()
        HTMLParser.__init__(self, verbose)

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag == "meta":
            self.metas.append(attrs)

    def detect_meta_refresh(self):
        for meta_tag in self.metas:
            if meta_tag[0][0] == "http-equiv":  # should always be the case:
                return meta_tag[1][1]
            else:
                pass  # ignoring badly-formatted meta tags
        return False

    def handle_endtag(self, tag):
        pass
        # print("Encountered an end tag :", tag)

    def handle_data(self, data):
        pass
        # print("Encountered some data  :", data)


class SpamCopHtmlPFinder(HTMLParser):

    def __init__(self, verbose=0):
        self.paragraphs = list()
        HTMLParser.__init__(self, verbose)

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        if tag == "p":
            print("and it is a paragraph")
            self.paragraphs.append(tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

class SpamCopFormFinder(HTMLParser):

    def __init__(self, verbose=0):
        self.forms = list()
        HTMLParser.__init__(self, verbose)

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag == "form":
            self.forms.append(attrs)
            for attr in attrs:
                print("     attr:", attr)

    # def detect_meta_refresh(self):
    #     for meta_tag in self.metas:
    #         if meta_tag[0][0] == "http-equiv":  # should always be the case:
    #             return meta_tag[1][1]
    #         else:
    #             pass  # ignoring badly-formatted meta tags
    #     return False

    def handle_endtag(self, tag):
        pass
        # print("Encountered an end tag :", tag)

    def handle_data(self, data):
        pass
        # print("Encountered some data  :", data)


class SpamCopFinder:

    def __init__(self):
        pass

    @staticmethod
    def confirm_form(html):
        # parse the passed-in html
        soup = BeautifulSoup(html)
        # find all the forms with enctype set to multipart/form-data
        right_form = soup.find_all(enctype="multipart/form-data")
        payload = dict()
        for child in right_form[0].descendants:
            if child.name == "input":
                # you can't detect if 'type' is set, so wrap it in a try/except block?
                try:
                    if child['type'] not in ['submit']:
                        # print("%s/%s/%s" % (child['name'], child['type'], child['value']))
                        payload[child['name']] = child['value']
                except KeyError:
                    pass
        # some error cases would be good!
        return payload
