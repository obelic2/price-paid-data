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
from apache_beam.io import ReadFromText, WriteToText
from apache_beam.options.pipeline_options import PipelineOptions

KEYS = [
    "transaction_id",
    "price",
    "transfer_date",
    "postcode",
    "property_type",
    "old_new",
    "duration",
    "paon",
    "saon",
    "street",
    "locality",
    "town_city",
    "district",
    "county",
    "ppd_category_type",
    "record_status",
]


class CreateAddressObject(beam.DoFn):
    """Create Address object using address as key"""

    def process(self, element):
        """Unpacks the CSV and add key names and creates address object"""

        # Create the address key name
        address = " ".join(
            [
                element[key]
                for key in [
                    "paon",
                    "saon",
                    "street",
                    "locality",
                    "town_city",
                    "district",
                    "county",
                    "postcode",
                ]
                if element[key]
            ]
        )
        address_data = (address, element)
        yield address_data


class AddAddressKeys(beam.DoFn):
    """Add Address keys into the csv input"""

    def process(self, element):
        """Add keys afer reading"""

        line = csv.DictReader(
            [element], fieldnames=KEYS, delimiter=",", quotechar='"'
        )
        data = dict(next(line))

        yield data


class FormJson(beam.DoFn):
    """Pack up objects as JSON for export"""

    def process(self, element):
        """Likely a better way to accomplish this"""

        dict_object = {element[0]: element[1]}
        yield dict_object


def load_counties():
    # Load a list of counties for beam pipeline division
    with open("/app/counties.csv") as file:
        counties_file = csv.reader(file)
        counties = list(counties_file)

    return counties


def county_filter(element, county):
    # Filter the current county only
    return element[1]["county"] == county


def run(argv=None):
    """Main entry point; defines and runs the transform pipeline."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", dest="input", required=True, help="Input file to process."
    )
    parser.add_argument(
        "--output",
        dest="output",
        required=True,
        help="Output file to write results to.",
    )
    # parser.add_argument(
    #     '--monthly',
    #     dest='monthly',
    #     action='store_true',
    #     help='If data source is monthly, else assumed as yearly'
    # )
    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options = PipelineOptions(pipeline_args)

    # if not known_args.monthly:
    #     KEYS.pop(-1)

    with beam.Pipeline(options=pipeline_options) as p:
        lines = p | "read_data" >> ReadFromText(known_args.input)

        data = lines | "add_keys" >> beam.ParDo(AddAddressKeys())

        addresses = (
            data
            | "create_address_object" >> beam.ParDo(CreateAddressObject())
            # | "group_by_address" >> beam.GroupByKey()
            # | "create_json_string" >> beam.Map(json.dumps)
        )

        # address_object = addresses | "create_dict" >> beam.ParDo(FormJson())

        counties = load_counties()

        count = 0
        for county in counties:
            county = county[0]
            (
                addresses
                | f"filter_county_{count}"
                >> beam.Filter(county_filter, county)
                | f"create_dict_{count}" >> beam.ParDo(FormJson())
                | f"create_json_string_{count}" >> beam.Map(json.dumps)
                | f"write_local_{count}"
                >> WriteToText(
                    f"result/{county}/test", file_name_suffix=".json"
                )
            )
            count += 1

        # address_object | "write_local" >> WriteToText(
        #     known_args.output, file_name_suffix=".json"
        # )
        # address_object | "write_cloud" >> WriteToText(
        #     f"gs://uk-housing-prices/{known_args.output[6:]}",
        #     file_name_suffix=".json",
        # )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
