import requests

def get_state_data(fiscal_year):
    """
    Fetches state data for a given fiscal year from the API.
    """
    url = "https://api.usaspending.gov/api/v2/recipient/state/"
    params = {'fiscal_year': fiscal_year}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()  # Assumes response is JSON-encoded

def find_highest_grant_per_resident(fiscal_year):
    """
    Finds the state or territory with the highest grant per resident for a given fiscal year.
    """
    data = get_state_data(fiscal_year)
    
    # Validate that the data is a list
    if not isinstance(data, list):
        raise ValueError("Unexpected response format: data is not a list.")
    
    highest_state = None
    highest_grant_per_resident = 0

    for state in data:
        # Extract population and grant total, defaulting to 0 if not present
        population = state.get('count', 0)  # Assuming 'count' represents population
        grant_total = state.get('amount', 0)

        # Avoid division by zero
        if population > 0:
            grant_per_resident = grant_total / population
            if grant_per_resident > highest_grant_per_resident:
                highest_grant_per_resident = grant_per_resident
                highest_state = state.get('name', 'Unknown')

    # If no valid states found, raise an error
    if highest_state is None:
        raise ValueError("No state data with valid population and grant values.")

    return highest_state, highest_grant_per_resident

def main():
    try:
        fiscal_year = 2023
        state, grant_per_resident = find_highest_grant_per_resident(fiscal_year=fiscal_year)
        print(f"State with highest grant value per resident in {fiscal_year}: {state} (${grant_per_resident:.2f})")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the program
main()
