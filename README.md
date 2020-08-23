# price-paid-data

This repository is for the analysis of UK housing price data.

Data transformations are conducted using Apache Beam.

In the local environment, Docker is used to build Apache Beam pipelines for the
transformation of data. Within the cloud environment GCP Dataflow is used as the
orchestratory and data is moved into BigQuery for analysis purposes.

## Known issues

- Running the pipeline for a monthly file without specifying the flag doesn't
error out. Instead the key is null in the end.
- Address key can be cleaned up to not be so unwieldly
- Integration test cases when pipeline is run is required
  - Group by function tested manually and groups addresses when required
  - However a test can be written to automate this
- Currently can't run the complete data file. Unexpectedly dies, possibly due
to memory limitations

## Next Steps
