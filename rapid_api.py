import requests

import config


def get_destination_id(sity):
    kal_list = ['<', 's', 'p', 'n', 'c', 'a', '=', 'i', 'g', 'h', 'l', 't', 'e', 'd', "'", '>', '/']
    sity_list = []
    url = "https://hotels-com-provider.p.rapidapi.com/v1/destinations/search"

    querystring = {"query":f"{sity}","currency":"UAH","locale":"ru_RU"}

    headers = {
        'x-rapidapi-host': "hotels-com-provider.p.rapidapi.com",
        'x-rapidapi-key': "70d6c25f42msh251ac7432fef32bp1f4502jsn416b189200bc"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        result = response.json()
        for results in result['suggestions']:
            if results['group'] == 'CITY_GROUP':
                for city in results['entities']:
                    try:
                        clear_name = ''
                        for sym in city['caption']:
                            if not sym in kal_list:
                                clear_name += sym
                        sity_list.append(f"{clear_name}:{city['destinationId']}")
                    except KeyError:
                        pass
    return sity_list


def get_hotels(destination_id, option):
    results_dict = dict()
    options_dict = {
        "1": "PRICE_HIGHEST_FIRST",
        "2": "PRICE",
        "3": "DISTANCE_FROM_LANDMARK",
        "4": ""
    }

    url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/search"

    querystring = {"checkin_date":"2022-03-26","checkout_date":"2022-03-27","sort_order":f"{options_dict[option]}","destination_id":f"{destination_id}","adults_number":"1","locale":"ru_RU","currency":"UAH"}

    headers = {
        'x-rapidapi-host': "hotels-com-provider.p.rapidapi.com",
        'x-rapidapi-key': "70d6c25f42msh251ac7432fef32bp1f4502jsn416b189200bc"
        }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    for results in response['searchResults']['results']:
        if len(results_dict) <= 5:
            try:
                results_dict[results['id']] = dict()
                results_dict[results['id']]['photo'] = results['optimizedThumbUrls']['srpDesktop']
                results_dict[results['id']]['name'] = results['name']
                results_dict[results['id']]['address'] = results['address']['streetAddress']
                results_dict[results['id']]['price'] = f"{results['ratePlan']['price']['current']} - {results['ratePlan']['price']['info']}"
                landmarks_list = ''
                for landmarks in results['landmarks']:
                    landmarks_list += f"{landmarks['label']} - {landmarks['distance']}\n"
                results_dict[results['id']]['landmarks'] = landmarks_list
                results_dict[results['id']]['guestReviews'] = f"{results['guestReviews']['rating']} - {results['guestReviews']['badgeText']}"
            except KeyError:
                pass
        else:
            break

    return results_dict

