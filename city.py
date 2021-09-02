good_symbols_list = ['<', 'p', 'a', 'n', 'c', 'l', '=', "'", 'h', 'i', 'g', 'l', 't', 'e', 'd', '/', 's', '>']


def result_cleaner(caption):
    clean_caption = ''
    for letters in caption:
        if letters not in good_symbols_list:
            clean_caption += letters
    return clean_caption


class City:

    def __init__(self, some_dict):
        self.geoId = some_dict['geoId']
        self.destinationId = some_dict['destinationId']
        self.landmarkCityDestinationId = some_dict['landmarkCityDestinationId']
        self.type = some_dict['type']
        self.redirectPage = some_dict['redirectPage']
        self.latitude = some_dict['latitude']
        self.longitude = some_dict['longitude']
        self.searchDetail = some_dict['searchDetail']
        self.caption = result_cleaner(some_dict['caption'])
        self.name = some_dict['name']
