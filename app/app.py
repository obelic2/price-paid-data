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


def run(argv=None):
    """Main entry point; defines and runs the wordcount pipeline."""

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
    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options = PipelineOptions(pipeline_args)

    with beam.Pipeline(options=pipeline_options) as p:
        lines = p | ReadFromText(known_args.input)

        data = lines | beam.Map(json.dumps)

        data | WriteToText(known_args.output, file_name_suffix='.json')

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
