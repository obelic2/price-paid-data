"""
Transform price paid data

This module transforms UK price paid data for housing into its desired state.
This module is currently for local runtime
"""

import argparse
import csv
import json
import logging

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
