import pandas as pd
import re


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    # Remove rows where the passenger count is equal to 0 and the trip distance is equal to zero.
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0) ]

    # Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    # Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id.
    data.columns = data.columns.to_series().apply(lambda x: re.sub(r'((?<=[a-z])[A-Z])', r'_\1', x).lower())

    print(data['vendor_id'].unique())

    return data


@test
def test_output(output, *args) -> None:
    assert not output.columns.isin(['vendor_id']).all(), "There is no columns called 'vendor_id'"
    assert output['passenger_count'].isin([0]).sum() == 0, "There are rides with zero passenger"
    assert output['trip_distance'].isin([0]).sum() == 0, "There are rides with no distance"
