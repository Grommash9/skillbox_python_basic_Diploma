class Hotel:

    def __init__(self, hotel):
        self.id = hotel['id']
        self.name = hotel['name']
        self.streetAddress = hotel['address']['streetAddress']
        self.ratePlan = hotel['ratePlan']['price']['current']
        self.ratePlan_info = hotel['ratePlan']['price']['info']

    def get_photos(self, hotel_id):
        import requests

        url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/photos"

        querystring = {"hotel_id": hotel_id}

        headers = {
            'x-rapidapi-host': "hotels-com-provider.p.rapidapi.com",
            'x-rapidapi-key': "70d6c25f42msh251ac7432fef32bp1f4502jsn416b189200bc"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        json_shit = response.json()

        photo_links = []

        for line in json_shit:
            photo_links.append(line['mainUrl'])

        print(photo_links)






