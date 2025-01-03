# Dictionary of Live Entertainment venues
live_entertainment = {
    "live entertainment": [
        "amphitheatre", "comedy_club", "concert_hall", "dance_hall", "event_venue", "karaoke", "night_club",
        "opera_house", "philharmonic_hall"
    ]
}

ev_charging = {
    "ev charging": ["electric_vehicle_charging_"]
}

mcdonald = {
    "mcdonald's": ["fast_food_restaurant"]
}

vet = {
    "vet": ["veterinary_care"]
}

public_transit = {
    "public transit": ["bus_station", "train_station", "subway_station", "transit_station", "light_rail_station",
                       "tram_station", "monorail_station", "bus_station"]
}


def all_dictionaries():
    dictionary_stack = [live_entertainment, ev_charging, mcdonald, vet, public_transit]
    return dictionary_stack
