# Test suite for price paid data

from app.app import CreateAddressObject, AddAddressKeys


def test_csv_to_json():
    input_line = (
        '"{A96E4ACB-D1DA-9205-E053-6C04A8C0DA09}","240000","2004-06-22 00:00",'
        '"BS40 5JL","S","N","F","3","","CAMBRIDGE COURT","WRINGTON","BRISTOL",'
        '"NORTH SOMERSET","NORTH SOMERSET","A","A"'
    )

    expected = (
        (
            "3 CAMBRIDGE COURT WRINGTON BRISTOL "
            "NORTH SOMERSET NORTH SOMERSET BS40 5JL"
        ),
        {
            "transaction_id": "{A96E4ACB-D1DA-9205-E053-6C04A8C0DA09}",
            "price": "240000",
            "transfer_date": "2004-06-22 00:00",
            "postcode": "BS40 5JL",
            "property_type": "S",
            "old_new": "N",
            "duration": "F",
            "paon": "3",
            "saon": "",
            "street": "CAMBRIDGE COURT",
            "locality": "WRINGTON",
            "town_city": "BRISTOL",
            "district": "NORTH SOMERSET",
            "county": "NORTH SOMERSET",
            "ppd_category_type": "A",
            "record_status": "A",
        },
    )

    addkeys = AddAddressKeys()
    data = addkeys.process(input_line)
    pipe = CreateAddressObject()
    result = pipe.process(next(data))

    assert next(result) == expected
