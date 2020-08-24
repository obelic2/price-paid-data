# price-paid-data

This repository is for the analysis of UK housing price data.

Data transformations are conducted using Apache Beam.

## Design Overview

The aim of this pipeline design is to maximize portability between different
systems, including local machines and the cloud. To this end, Docker containers
were used to standardise the processing environment and maintain replicability
across systems.

Python 3.7.9 Slim Buster edition was used as the base image, as this is the
highest supported Python version for Apache Beam. To this only Apache Beam is
required to be installed.

Within the pipeline itself, the CSV is transformed into an address object,
with the key being the long-form address of the property. This was used to
minimise incorrect property matches from neighbouring properties. I also don't
entirely know the pertinent parts of an address in the UK, so this could likely
be shortened and have the same accuracy.

Migrating the solution to the cloud would be straightforward. As this already
uses Apache Beam, using Dataflow as the runner should be no issue. This should
also reduce (or eliminate) the requirement of using Docker. The data can then
be added to BigQuery for any analysis.

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
