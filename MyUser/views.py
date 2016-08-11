from Company.models import Location


def availableLocation(request):
    all_locations = None
    if request.user.is_superuser == False:
        # limit choices of location with location can user access
        all_locations = request.user.fk_locations.all()
    else:
        all_locations = Location.objects.all()
    return all_locations