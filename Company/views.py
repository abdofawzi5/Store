from Company.models import Location


def getAllLocations():
    allLocations = Location.objects.all().values('fk_locationType__type','name')
    locationsList = []
    for location in allLocations:
        found = next((item for item in locationsList if item["type"] == location['fk_locationType__type']),False)
        if found == False:
            dict = {}
            dict['type'] = location['fk_locationType__type']
            dict['name'] = [location['name']]
            locationsList.append(dict)
        else:
            dict['name'].append(location['name'])
    return locationsList        


