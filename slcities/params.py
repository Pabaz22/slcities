## City center coordinates (not actual center but center of the area where we'll do the API call)
DUBLIN_CENTER_COORDS=(53.350140, -6.266155)
NICE_CENTER_COORDS = (43.70809, 7.27372)


## Places types
# https://developers.google.com/maps/documentation/places/web-service/supported_types

PLACES_TYPES_DISCRIMINANT_SET = [
    'art_gallery', 'atm', 'bakery', 'bank', 'bar', 'beauty_salon', 'cafe',
    'car_dealer', 'car_rental', 'car_repair', 'car_wash', 'clothing_store',
    'convenience_store', 'department_store', 'doctor', 'drugstore',
    'electrician', 'electronics_store', 'furniture_store', 'gas_station',
    'gym', 'hair_care', 'hardware_store', 'hospital', 'jewelry_store',
    'laundry', 'liquor_store', 'lodging', 'movie_theater', 'museum',
    'night_club', 'park', 'parking', 'pharmacy', 'plumber', 'police',
    'post_office', 'primary_school', 'real_estate_agency', 'restaurant',
    'rv_park', 'school', 'shopping_mall', 'spa', 'stadium', 'bus_station',
    'subway_station', 'supermarket'
    ]

## Columns to retain for exportation
API_CALL_COLUMNS_OF_INTEREST = [
    'place_id', 'geometry.location.lat', 'geometry.location.lng', 'name',
    'types', 'price_level', 'opening_hours.open_now', 'formatted_address'
]

# lights_data = '../raw_data/dcc-pl-assert-list_open-data_260321.csv'
# footfall_data = '../raw_data/name_file_footfall.csv'
# areas_data = '../raw_data/Population_by_Sex_and_Marital_Status,_Electoral_Division,_Census_2016,_Theme_1.2,_Ireland,_2016,_CSO_&_OSi.geojson'




# PLACES_TYPES_BIG_DISCRIMINANT_SET = [
#     'accounting', 'amusement_park', 'art_gallery', 'atm', 'bakery', 'bank',
#     'bar', 'beauty_salon', 'bicycle_store', 'bowling_alley', 'cafe',
#     'car_dealer', 'car_rental', 'car_repair', 'car_wash', 'casino',
#     'clothing_store', 'convenience_store', 'dentist', 'department_store',
#     'doctor', 'drugstore', 'electrician', 'electronics_store', 'florist',
#     'furniture_store', 'gas_station', 'gym', 'hair_care', 'hardware_store',
#     'home_goods_store', 'hospital', 'insurance_agency', 'jewelry_store',
#     'laundry', 'lawyer', 'liquor_store', 'jewelry_store', 'laundry', 'lawyer',
#     'liquor_store', 'locksmith', 'lodging', 'meal_delivery', 'meal_takeaway',
#     'movie_rental', 'movie_theater', 'moving_company', 'museum', 'night_club',
#     'painter', 'park', 'parking', 'pet_store', 'pharmacy', 'physiotherapist',
#     'plumber', 'police', 'post_office', 'primary_school', 'real_estate_agency',
#     'restaurant', 'roofing_contractor', 'rv_park', 'school',
#     'secondary_school', 'shoe_store', 'shopping_mall', 'spa', 'stadium',
#     'storage', 'store', 'bus_station', 'subway_station', 'supermarket',
#     'tourist_attraction', 'travel_agency', 'university', 'veterinary_care'
# ]

# PLACES_TYPES_SINGLE_TO_FEW_PLACE = [
#     'airport',
#     'aquarium',
#     'cemetery',
#     'city_hall',
#     'courthouse',
#     'embassy',
#     'fire_station',
#     'funeral_home',
#     'library',
#     'light_rail_station',
#     'local_government_office',
#     'train_station',
#     'transit_station',
#     'zoo',
#     'casino',
# ]

# PLACES_TYPES_CULTURE_DEPENDENT = ['church', 'mosque', 'synagogue',
#                                   'hindu_temple']

# PLACES_TYPES_WHOLE_SET = [
#     'accounting', 'amusement_park', 'art_gallery', 'atm', 'bakery', 'bank',
#     'bar', 'beauty_salon', 'bicycle_store', 'bowling_alley', 'cafe',
#     'car_dealer', 'car_rental', 'car_repair', 'car_wash', 'casino',
#     'clothing_store', 'convenience_store', 'dentist', 'department_store',
#     'doctor', 'drugstore', 'electrician', 'electronics_store', 'florist',
#     'furniture_store', 'gas_station', 'gym', 'hair_care', 'hardware_store',
#     'home_goods_store', 'hospital', 'insurance_agency', 'jewelry_store',
#     'laundry', 'lawyer', 'liquor_store', 'jewelry_store', 'laundry', 'lawyer',
#     'liquor_store', 'locksmith', 'lodging', 'meal_delivery', 'meal_takeaway',
#     'movie_rental', 'movie_theater', 'moving_company', 'museum', 'night_club',
#     'painter', 'park', 'parking', 'pet_store', 'pharmacy', 'physiotherapist',
#     'plumber', 'police', 'post_office', 'primary_school', 'real_estate_agency',
#     'restaurant', 'roofing_contractor', 'rv_park', 'school',
#     'secondary_school', 'shoe_store', 'shopping_mall', 'spa', 'stadium',
#     'storage', 'store', 'bus_station', 'subway_station', 'supermarket',
#     'tourist_attraction', 'travel_agency', 'university', 'veterinary_care',
#     'airport', 'aquarium', 'cemetery', 'city_hall', 'courthouse', 'embassy',
#     'fire_station', 'funeral_home', 'library', 'light_rail_station',
#     'local_government_office', 'train_station', 'transit_station', 'zoo',
#     'casino', 'church', 'mosque', 'synagogue', 'hindu_temple'
# ]
