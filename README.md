# price-paid-data

This repository is for the analysis of UK housing price data.

Data transformations are conducted using Apache Beam.

In the local environment, Docker is used to build Apache Beam pipelines for the
transformation of data. Within the cloud environment GCP Dataflow is used as the
orchestratory and data is moved into BigQuery for analysis purposes.

## Setup Instructions

NOTE: For this to work locally, you will require Python and Docker on your
machine. This was built using:
- Docker 19.03.12

Run in the main folder directory:

1. `sh setup.sh`
2. `docker-compose build`
3. `docker-compose up -d`

The folder environemnt should be complete, and the docker container should be
running! In order to process a file with the module:

1. Add a file into the `data` folder. If you ran the `setup.sh` script, a
`monthly.csv` file should be in there as a test
2. Run the command: `docker-compose exec python_beam sh -c "python -m app.app --input data/ --output result/test"`

Your results will be stored in the `results` folder, or whichever folder you
specified in the command above. The file is stored as JSONLines grouped by
address.

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

- Move system into GCP
- Add pipeline using Dataflow as the runner
- Make the data available in BigQuery
- Ensure that the data structure aligns with the use cases or stakeholder
expectations
- Set up infrastructure using Terraform
- Download the source file from the URL
- Set up schedule to download latest month of data each month
- Automate build using CI/CD tool
