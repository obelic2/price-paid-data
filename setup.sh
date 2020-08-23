# Setup environment prior to running
# Mainly for desired folders for the module to run

# Run on a MacOS machine
mkdir data
mkdir result

# If curl not available, try wget
curl -o data/monthly.csv -OL http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update-new-version.csv
