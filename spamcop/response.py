from bs4 import BeautifulSoup


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
                    if child['type'] == 'checkbox':
                        # could not find what the spec says to send
                        # when there is no 'value' on a checkbox. but
                        # True works ...
                        payload[child['name']] = True
                    if child['type'] not in ['submit']:
                        payload[child['name']] = child['value']
                except KeyError:
                    pass
        # some error cases would be good!
        return payload

    @staticmethod
    def meta_refresh_seconds(html):
        soup = BeautifulSoup(html)
        meta_tags = soup.find_all("meta")
        for meta in meta_tags:
            if meta.get('http-equiv'):
                # time.sleep wants a float
                return float(meta.get("content"))
        return False
