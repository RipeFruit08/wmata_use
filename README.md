# wmata_use

script to parse csv use history of WMATA SMARTRIP Card.

# Monthly Unlimited Pass value assessment
Determines whether or not your Monthly Unlimited Pass is saving or costing you
money. This leverages the WMATA API. It requires supplying your own API key.

WMATA monthly passes are determined by trip fare which range from $2 to $6 with
0.25 increments in between. As of Dec 2021, the cost calculation for these fares
is 36 trips (or 18 round trips). For example, a pass with unlimited $2 fare
trips would cost $72 `($2 fare x 36 trips = 72)`. 

Given that a typical month has 4 weeks/20 working days even commuters taking the
train to work every day barely find value out of their monthly pass. If more
than two working days are taken off, then they are not even breaking even. This
is further complicated by things like ride time (peak vs off peak fares) as well
as fares that don't line up with the monthly pass. For example, it is possible
that a person's daily commute is $3.65 in each direction. However, for that
person they would need to purchase a $3.75 price point monthly pass which
further reduces the value of their monthly pass.

Of course this assumes that these riders are not using their pass during the
weekends. (note: As of Sep 2021, weekend fares were brought to a flat $2). It
would seem that the monthly fares are only worthwhile to the heaviest of users
who commute to work every day and use the metro on weekends.  WMATA should
consider restructuring the pricing of their monthly pass offerings to accomodate
more commuters especially since hybrid workers are becoming more common.

# What the script does
This script is fairly straightforward. It simply goes through a SMARTRIP User
History csv file and tallies up the fares on all trips on Metrorail. It will
then report back the total cost of that given period without a monthly pass.

## Setup
  1. Log in to your SMARTRIP account and view the Use History for a given month. 
  2. Select "Export To Excel" to download Use History in .csv format 
  3. Log in to your WMATA API account and retrieve your `Primary Key`. This will
  be used to the set `API_KEY` environment variable in the `env_vars`
  environment variable file
  4. `source env_vars` to set the environment variables
  5. run the script `python parse_csv.py`