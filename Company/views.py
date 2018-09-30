from Company.models import Location


def getAllLocations():
    allLocations = Location.objects.all().values('fk_locationType__type','name','id')
    locationsList = []
    for location in allLocations:
        found = next((item for item in locationsList if item["type"] == location['fk_locationType__type']),False)
        if found == False:
            dic = {}
            dic['type'] = location['fk_locationType__type']
            dic['name'] = [{'name':location['name'],'id':location['id']}]
            locationsList.append(dic)
        else:
            found['name'].append({'name':location['name'],'id':location['id']})
    return locationsList

def getLocation(ID):
    try:
        return Location.objects.filter(id = ID)[0]
    except:
        return Location.objects.all()[0]
        