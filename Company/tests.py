from django.test import TestCase
from models import *
from views import getAllLocations


class GetLocationTestCase(TestCase):
    def setUp(self):
        company = Company.objects.create(name='stocky',slogan='MySlogan',short_description='Stocky is an stock management system',long_description='Stocky is an stock management system, can Monitor Data, Measure sales performance and generate invoices',phone='0xxxxxxxxxx',address='3x street, City, Country ',email='name@domain.com')
        location_type = LocationType.objects.create(type="Store")
        Location.objects.create(fk_locationType=location_type,name="Store1",phone='0xxxxxxxxx',address='street, City, Country',email='store1@domain.com')

    def test_get_all_locations(self):
        locations = getAllLocations()
        self.assertEqual(locations[0]['type'], 'Store')
        self.assertEqual(locations[0]['name'][0]['name'], 'Store1')
        print locations
