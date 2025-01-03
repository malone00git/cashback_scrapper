# List of Automotive categories
automotive_categories = ["car_dealer", "car_rental", "car_repair", "car_wash", "electric_vehicle_charging_station",
                         "gas_station", "parking", "rest_stop"]

# List of Business categories
business_categories = [
    "corporate_office", "farm", "ranch"
]

# List of Culture categories
culture = [
    "art_gallery", "art_studio", "auditorium", "cultural_landmark", "historical_place", "monument", "museum",
    "performing_arts_theater", "sculpture"
]

# List of Education categories
education = [
    "library", "preschool", "primary_school", "school", "secondary_school", "university"
]

# List of Entertainment and Recreation categories
entertainment_recreation = [
    "adventure_sports_center", "amphitheatre", "amusement_center", "amusement_park", "aquarium", "banquet_hall",
    "barbecue_area", "botanical_garden", "bowling_alley", "casino", "childrens_camp", "comedy_club", "community_center",
    "concert_hall", "convention_center", "cultural_center", "cycling_park", "dance_hall", "dog_park", "event_venue",
    "ferris_wheel", "garden", "hiking_area", "historical_landmark", "internet_cafe", "karaoke", "marina",
    "movie_rental", "movie_theater", "national_park", "night_club", "observation_deck", "off_roading_area",
    "opera_house", "park", "philharmonic_hall", "picnic_ground", "planetarium", "plaza", "roller_coaster",
    "skateboard_park", "state_park", "tourist_attraction", "video_arcade", "visitor_center", "water_park",
    "wedding_venue", "wildlife_park", "wildlife_refuge", "zoo"
]

# List of Facilities categories
facilities = [
    "public_bath", "public_bathroom", "stable"
]

# List of Finance categories
finance = [
    "accounting", "atm", "bank"
]

# List of Food and Drink categories
food_and_drink = [
    "acai_shop", "afghani_restaurant", "african_restaurant", "american_restaurant", "asian_restaurant", "bagel_shop",
    "bakery", "bar", "bar_and_grill", "barbecue_restaurant", "brazilian_restaurant", "breakfast_restaurant",
    "brunch_restaurant", "buffet_restaurant", "cafe", "cafeteria", "candy_store", "cat_cafe", "chinese_restaurant",
    "chocolate_factory", "chocolate_shop", "coffee_shop", "confectionery", "deli", "dessert_restaurant", "dessert_shop",
    "diner", "dog_cafe", "donut_shop", "fast_food_restaurant", "fine_dining_restaurant", "food_court",
    "french_restaurant", "greek_restaurant", "hamburger_restaurant", "ice_cream_shop", "indian_restaurant",
    "indonesian_restaurant", "italian_restaurant", "japanese_restaurant", "juice_shop", "korean_restaurant",
    "lebanese_restaurant", "meal_delivery", "meal_takeaway", "mediterranean_restaurant", "mexican_restaurant",
    "middle_eastern_restaurant", "pizza_restaurant", "pub", "ramen_restaurant", "restaurant", "sandwich_shop",
    "seafood_restaurant", "spanish_restaurant", "steak_house", "sushi_restaurant", "tea_house", "thai_restaurant",
    "turkish_restaurant", "vegan_restaurant", "vegetarian_restaurant", "vietnamese_restaurant", "wine_bar"
]

# List of Geographical Areas categories
geographical_areas = [
    "administrative_area_level_1", "administrative_area_level_2", "country", "locality", "postal_code",
    "school_district"
]

# List of Government categories
government = [
    "city_hall", "courthouse", "embassy", "fire_station", "government_office", "local_government_office",
    "police", "post_office"
]

# List of Health and Wellness categories
health_and_wellness = [
    "chiropractor", "dental_clinic", "dentist", "doctor", "drugstore", "hospital", "massage", "medical_lab",
    "pharmacy", "physiotherapist", "sauna", "skin_care_clinic", "spa", "tanning_studio", "wellness_center",
    "yoga_studio"
]

# List of Housing categories
housing = [
    "apartment_building", "apartment_complex", "condominium_complex", "housing_complex"
]

# List of Lodging categories
lodging = [
    "bed_and_breakfast", "budget_japanese_inn", "campground", "camping_cabin", "cottage", "extended_stay_hotel",
    "farmstay", "guest_house", "hostel", "hotel", "inn", "japanese_inn", "lodging", "mobile_home_park", "motel",
    "private_guest_room", "resort_hotel", "rv_park"
]

# List of Natural Features categories
natural_features = [
    "beach"
]

# List of Places of Worship categories
places_of_worship = [
    "church", "hindu_temple", "mosque", "synagogue"
]

# List of Services categories
services = [
    "astrologer", "barber_shop", "beautician", "beauty_salon", "body_art_service", "catering_service",
    "cemetery", "child_care_agency", "consultant", "courier_service", "electrician", "florist", "food_delivery",
    "foot_care", "funeral_home", "hair_care", "hair_salon", "insurance_agency", "laundry", "lawyer", "locksmith",
    "makeup_artist", "moving_company", "nail_salon", "painter", "plumber", "psychic", "real_estate_agency",
    "roofing_contractor", "storage", "summer_camp_organizer", "tailor", "telecommunications_service_provider",
    "tour_agency", "tourist_information_center", "travel_agency", "veterinary_care"
]

# List of Shopping categories
shopping = [
    "asian_grocery_store", "auto_parts_store", "bicycle_store", "book_store", "butcher_shop", "cell_phone_store",
    "clothing_store", "convenience_store", "department_store", "discount_store", "electronics_store", "food_store",
    "furniture_store", "gift_shop", "grocery_store", "hardware_store", "home_goods_store", "home_improvement_store",
    "jewelry_store", "liquor_store", "market", "pet_store", "shoe_store", "shopping_mall", "sporting_goods_store",
    "store", "supermarket", "warehouse_store", "wholesaler"
]

# List of Sports categories
sports = [
    "arena", "athletic_field", "fishing_charter", "fishing_pond", "fitness_center", "golf_course", "gym",
    "ice_skating_rink", "playground", "ski_resort", "sports_activity_location", "sports_club",
    "sports_coaching", "sports_complex", "stadium", "swimming_pool"
]

# List of Transportation categories
transportation = [
    "airport", "airstrip", "bus_station", "bus_stop", "ferry_terminal", "heliport", "international_airport",
    "light_rail_station", "park_and_ride", "subway_station", "taxi_stand", "train_station", "transit_depot",
    "transit_station", "truck_stop"
]


def all_categories():
    list_stack = [automotive_categories, business_categories, culture, education,
                  entertainment_recreation, facilities, finance, food_and_drink, geographical_areas,
                  government, health_and_wellness, housing, lodging, natural_features, places_of_worship,
                  services, shopping, sports, transportation]
    return list_stack
