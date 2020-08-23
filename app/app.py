"""
Transform price paid data

This module transforms UK price paid data for housing into its desired state.
This module is currently for local runtime
"""

import argparse
import csv
import json
import logging

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions

KEYS = [
    'transaction_id',
    'price',
    "transfer_date",
    'postcode',
    'property_type',
    'old_new',
    'duration',
    'paon',
    'saon',
    'street',
    'locality',
    'town_city',
    'district',
    'county',
    'ppd_category_type',
    'record_status'
]

class CreateJSONObject(beam.DoFn):
    """Add keys to data fields"""

    def process(self, element):
        """To fill in"""
        line = csv.DictReader([element], fieldnames=KEYS,
                              delimiter=',', quotechar='"')
        data = dict(next(line))
        address = ' '.join([data[key] for key in 
            ['paon', 'saon', 'street', 'locality', 'town_city',
            'district', 'county', 'postcode'] if data[key]])
        address_data = {
            address: [data]
        }
        yield address_data


def run(argv=None):
    """Main entry point; defines and runs the transform pipeline."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        required=True,
        help='Input file to process.')
    parser.add_argument(
        '--output',
        dest='output',
        required=True,
        help='Output file to write results to.')
    parser.add_argument(
        '--monthly',
        dest='monthly',
        action='store_true',
        help='If data source is monthly, else assumed as yearly'
    )
    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options = PipelineOptions(pipeline_args)

    if not known_args.monthly:
        KEYS.pop(-1)

    with beam.Pipeline(options=pipeline_options) as p:
        lines = p | ReadFromText(known_args.input)

        data = (lines
                | beam.ParDo(CreateJSONObject())
                | beam.Map(json.dumps))

        data | WriteToText(known_args.output, file_name_suffix='.json')

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
