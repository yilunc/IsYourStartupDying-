import csv
import datetime
import mysql.connector
from Company import Company

#   TODO:
#   !Priority!
##
#
#   Find a way to use NoneTypes in the distance calculation. Ie). None Funding
#   should be 0. Everything but founding date, should be 0.
#   Use Key verification to login to DB User instead of password
##
#   Quality Of Life
##
#   Clean the data so assumptions can be made.
#   Look into using defualtdict to get rid of the dict initalization try/catch
#   Consolidate the For-loops in weight calc as they are the same logic
#   Rework checking for None dates, and defaulting. Feels like too many if's
##
#
#


# MAGIC NUMBERS MHMM... (~^-^)~
MONEYTHRESHOLD = 800000
# Last time the DB was updated
LAST_REFRESH = datetime.date(2014,10,1)
# Based on 2.4 million a year
AVG_DAILY_BURN = float(2400000/365.0)
# Start ups that last more than 2.5 years are successful
OPERATION_RATING_PER_DAY = float(0.4/365.0)
# Start ups that have more than 2 years of runway are successful
RUNWAY_RATING_PER_DAY = float(0.5/365.0)
# Gain some points for relationships with key people
RELATIONSHIP_RATING = 0.2
# Companies that aren't auto successes and have no entered funding value
# are evaluated by last inflow, 1 - (inflow * rating)
INFLOW_RATING_PER_DAY = float(0.5/365.0)


def parseData(dbName):
    ref_data = []
    test_data = []
    country_map = {}
    city_map = {}
    market_map = {}
    maps = (country_map,city_map,market_map)

    entry_num = 0

    try:
        db = mysql.connector.connect(user='', password='', database=dbName)
        cursor = db.cursor(dictionary = True)
    except Exception as e:
        print("Unable to connect to Database {}:\n {}".format(dbName,e))
        raise SystemExit()

    query = ("SELECT normalized_name, category_code, status, "
    "country_code, state_code, city, region, invested_companies, "
    "first_investment_at, last_investment_at, investment_rounds, "
    "first_funding_at, last_funding_at, funding_rounds, "
    "funding_total_usd, founded_at, relationships FROM object_analysis "
    "WHERE entity_type NOT IN ('Product', 'People')")

    cursor.execute(query)

    for result in cursor:

        # WIP data points:
        #
        #state_code = result['state_code']
        #region = result['region']
        #invested_companies = result['invested_companies']

        name = result['normalized_name']
        market = result['category_code']
        funding_total = result['funding_total_usd']
        status = result['status']
        country = result['country_code']
        city = result['city']
        founded = result['founded_at']
        relationships = result['relationships']

        invest_rounds = result['investment_rounds']
        first_invest = result['first_investment_at']
        last_invest = result['last_investment_at']

        funding_rounds = result['funding_rounds']
        first_funding = result['first_funding_at']
        last_funding = result['last_funding_at']

        current_company = Company(name, status, market, country, city, founded,\
        relationships, invest_rounds, first_invest, last_invest,\
        funding_rounds, funding_total, first_funding, last_funding)

        current_company.successful = _is_successful(current_company)

        if entry_num % 500 != 0:
            country_map, city_map, market_map = _update_maps(country_map, \
            city_map, market_map, current_company)

            ref_data.append(current_company)
        else:
            test_data.append(current_company)
        entry_num += 1


    cursor.close()
    db.close()

    # Create the weight or 'influence rating' for each key in every map
    #
    for current_map in maps:
        for key in current_map:
            try:
                if((current_map[key][0] - current_map[key][1]) < -2):
                    print("Fails for {0} : {1}".format(key,current_map[key][0] - current_map[key][1]))
            except Exception as e:
                pass
            key_total = current_map[key][0] + current_map[key][1]
            if (key_total < 5 or current_map[key][0] > 0):

                current_map[key] = \
                float(current_map[key][1])/float(key_total)
                current_map[key] = abs(current_map[key] - 0.5)
            else:
                current_map[key] = 0.5

    return ref_data, test_data, country_map, city_map, market_map


def _is_successful(current_company):
    # Company is automatically considered a success if IPO or Acquired
    #
    rating = 0

    if current_company.status in ('ipo', 'acquired'):
        rating = 1
    elif ((current_company.first_funding or current_company.first_invest or \
    current_company.founded) and (current_company.status != 'closed')):
        # Company is operating so handle categorizing

        # Calculate start date (All three could be null) I want the acquired
        # IPO, and closed ones to trickle through without a SQL or cleaning
        # So must still Check

        # Need a success_rating of 1+
        valid_dates = []
        runway = 0

        if current_company.first_funding:
            valid_dates.append(current_company.first_funding)
        if current_company.first_invest:
            valid_dates.append(current_company.first_invest)
        if current_company.founded:
            valid_dates.append(current_company.founded)

        start_date = min(valid_dates)

        days_operating = (LAST_REFRESH - start_date).days

        if(current_company.funding_total):
            days_funded = \
            float(current_company.funding_total)/AVG_DAILY_BURN

            runway = days_operating - days_funded

        elif (days_operating < 912.5) and \
        (current_company.last_funding or current_company.last_invest):
            # 912.5 = 2.5 years
            # For empty funding data calculate the time since their
            # last funding. The thought is that if you have just recieved
            # funding then you have some sort of success.

            # As there are cases where date of funding is before founding...
            valid_dates = []
            if current_company.last_funding:
                valid_dates.append(current_company.last_funding)
            if current_company.last_invest:
                valid_dates.append(current_company.last_invest)
            last_inflow_at = max(valid_dates)
            days_since_inflow = (LAST_REFRESH - last_inflow_at).days
            flow_rating = (1 - (days_since_inflow * INFLOW_RATING_PER_DAY) )
            if flow_rating > 0:
                rating += flow_rating

        rating += days_operating * (OPERATION_RATING_PER_DAY)
        rating += runway * (RUNWAY_RATING_PER_DAY)
        if current_company.relationships:
            rating += current_company.relationships * RELATIONSHIP_RATING

    return bool(rating >= 1)


def _update_maps(country_map, city_map, market_map, current_company):
    if current_company.successful:
        # Company is deemed successful
        try:
            country_map[current_company.country][0] += 1
        except KeyError:
            country_map[current_company.country] = [1,0]

        try:
            market_map[current_company.market][0] += 1
        except KeyError:
            market_map[current_company.market] = [1,0]

        try:
            city_map[current_company.city][0] += 1
        except KeyError:
            city_map[current_company.city] = [1,0]
    else:
        try:
            country_map[current_company.country][1] += 1
        except KeyError:
            country_map[current_company.country] = [0,1]

        try:
            market_map[current_company.market][1] += 1
        except KeyError:
            market_map[current_company.market] = [0,1]

        try:
            city_map[current_company.city][1] += 1
        except KeyError:
            city_map[current_company.city] = [0,1]

    return country_map, city_map, market_map;
