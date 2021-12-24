# wmata_use

script to parse csv use history of WMATA SMARTRIP Card.

# Monthly Unlimited Pass value assessment
Determines whether or not your Monthly Unlimited Pass is actually saving or
costing you money. This leverages the WMATA API and requires you supplying your
own API key

## Setup
  1. Log in to your SMARTRIP account and view the Use History for a given month. 
  2. Select "Export To Excel" to download Use History in .csv format 
  3. Log in to your WMATA API account and retrieve your `Primary Key`. This will
  be used to the set `API_KEY` environment variable in the `env_vars`
  environment variable file
  4. `source env_vars` to set the environment variables
  5. run the script `python parse_csv.py`