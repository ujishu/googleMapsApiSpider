import googlemaps
import json
from key import KEY
from datetime import datetime as dt

# TODO
# save whole data in one json file

# This script collect next data:
# Place name
# address
# phone number
# web site
# reviews 
# google place url 

#Example of api call url:
#https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=50.4399900,30.5714000&radius=45000&type=establishment&keyword=Cafe&key=[KEY]
# location=50.4399900,30.5714000 was found manualy

#location="50.4399900,30.5714000"
radius = 50000
keyword = "Cafe"
place_type_list = ['food', 'bar', 'cafe', 'restaurant', 'establishment', 'point_of_interest']
place_id_list = []

def parse_place_page(place_id):
    
    """
    Func that parse sing place page.
    """
    
    place_info_response = gmaps.place(place_id)["result"]
    
    place_name = place_info_response["name"].encode('utf8').decode('utf8')
    place_address = place_info_response["formatted_address"].encode('utf8').decode('utf8')
    
    try:
        place_phone_number = place_info_response["international_phone_number"]
    except:
        place_phone_number = "-"
    
    try:
        place_website = place_info_response["website"]
    except:
        place_website = "-"
    
    try:    
        place_rating = place_info_response["rating"]
    except:
        place_rating = "-"
    
    place_google_url = place_info_response["url"]
    
    place_info = dict({"place_name": place_name,
                        "place_address": place_address,
                        "place_phone_number": place_phone_number,
                        "place_website": place_website,
                        "place_rating": place_rating,
                        "place_google_url": place_google_url,
                        "place_id": place_id})

    print("parse_place_page()")
    return place_info

def write_to_file(data, file_name):
    
    #string = str(data)
    data_for_write = data
    file = file_name
    
    with open(file, 'a') as f:
        json.dump(data_for_write, f, ensure_ascii=False)
        f.write('\n')
    print("write_to_file()")

def get_place_id_and_save(response, file_name):
    
    """
    This func collect place_ids from singl api response, call func parse_place_page
    and save data using write_to_file() function. 
    """
    
    print(place_id_list)

    if response["status"] != "OK":
        return "\nResponse status is %s \n" % response["status"]
    else:
        for item in response["results"]:
            #print(item)
            place_id = item["place_id"]
            if place_id not in place_id_list:
                place_id_list.append(place_id)
                place_info = parse_place_page(place_id)
                write_to_file(place_info, file_name)
            else:
                pass
        
        next_page_token = response["next_page_token"]
        
        get_new_response = gmaps.places_nearby(page_token=next_page_token, location=location, radius=radius, keyword=keyword, type=place_type)
        get_place_id_and_save(get_new_response, file_name)

if __name__ == "__main__":
    gmaps = googlemaps.Client(key=KEY)
    location =  '50.4501,30.5234' #gmaps.geocode(address='Kiev')[0]['address_components'][0]['location']
    print(location)
    file_name = "googlemaps_raw_data-" + dt.now().strftime('%d-%m-%y_%H%M%S') + '.output'
    
    # For place search will be used "Nearby Search" method.
    # Request first page
    
    for place_type in place_type_list:
        places_result_first_page = gmaps.places_nearby(location=location,
                                                    radius=radius,
                                                    keyword=keyword,
                                                    type=place_type)
        try:
            get_place_id_and_save(places_result_first_page, file_name)
        except googlemaps.exceptions.ApiError as e:
            print("\nException: %s\n" % e)
            pass
        except KeyError as err:
            print(err)
            if place_type_list.index(place_type)+1 == len(place_type_list):
                print("\nExit")
                break
            else:
                print("Switch to next place_type: %s" % place_type_list[place_type_list.index(place_type) + 1])
                pass