def test_create_location_and_return_latitude(fixture_location_create):
    latitude = 1
    assert fixture_location_create.latitude == latitude


def test_create_location_and_return_longitude(fixture_location_create):
    longitude = 1
    assert fixture_location_create.longitude == longitude
