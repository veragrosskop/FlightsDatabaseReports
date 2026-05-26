from sqlalchemy import create_engine, text

QUERY_FLIGHT_BY_ID = "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.ID = :id"
QUERY_FLIGHT_BY_DATE = "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.DAY = :day AND flights.MONTH = :month AND flights.YEAR = :year"
QUERY_DELAYED_FLIGHTS_BY_AIRLINE = "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY FROM flights JOIN airlines ON flights.airline = airlines.id WHERE DELAY >= 20 AND airlines.airline = :airline"
QUERY_DELAYED_FLIGHTS_BY_IATA = "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY FROM flights JOIN airlines ON flights.airline = airlines.id WHERE DELAY >= 20 AND flights.ORIGIN_AIRPORT = :iata"


# Define the database URL
DATABASE_URL = "sqlite:///data/flights.sqlite3"

# Create the engine
engine = create_engine(DATABASE_URL)


def execute_query(query, params):
    """
    Execute an SQL query with the params provided in a dictionary,
    and returns a list of records (dictionary-like objects).
    If an exception was raised, print the error, and return an empty list.
    """
    try:
        with engine.connect() as conn:
            results = conn.execute(text(query), params)
            return results.fetchall()
    except Exception as e:
        print("Query error:", e)
        return []


def get_flight_by_id(flight_id):
    """
    Searches for flight details using flight ID.
    If the flight was found, returns a list with a single record.
    """
    params = {"id": flight_id}
    return execute_query(QUERY_FLIGHT_BY_ID, params)


def get_flights_by_date(day, month, year):
    """
    Searches for flights details using the date.
    If the flights were found, returns a list with records.
    """
    params = {"day": day, "month": month, "year": year}
    return execute_query(QUERY_FLIGHT_BY_DATE, params)


def get_delayed_flights_by_airline(airline):
    """
    Searches for flights details using the date.
    If the flights were found, returns a list with records.
    """

    params = {"airline": airline}
    return execute_query(QUERY_DELAYED_FLIGHTS_BY_AIRLINE, params)


def get_delayed_flights_by_airport(airport):
    """
    Searches for delayed flights details using the airport IATA code.
    If the flights were found, returns a list with records.
    """

    params = {"iata": airport}
    return execute_query(QUERY_DELAYED_FLIGHTS_BY_IATA, params)
