import requests

def get_toptier_code_from_name(name):
    url = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    # Debugging: Print the API response to verify structure
    print("API Response:", data)

    # Loop through agencies and match by 'agency_name'
    for agency in data.get('results', []):  # Use `.get` for safety
        if agency.get('agency_name') == name:  # Match by 'agency_name'
            return agency.get('toptier_code')  # Retrieve 'toptier_code'

    raise ValueError(f"No agency found for name: {name}")

def get_budgetary_resources(toptier_agency_code, fiscal_year):
    url = f"https://api.usaspending.gov/api/v2/agency/{toptier_agency_code}/budgetary_resources/"
    params = {'fiscal_year': fiscal_year}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get('current_total_budget_authority_amount', 0)  # Update key

def get_new_awards_count(toptier_agency_code, fiscal_year):
    url = f"https://api.usaspending.gov/api/v2/agency/{toptier_agency_code}/awards/new/count/"
    params = {'fiscal_year': fiscal_year}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get('new_awards_count', 0)  # Update key if necessary

# Main NASA-specific calculations
try:
    nasa_code = get_toptier_code_from_name("Access Board")  # Match agency by 'agency_name'
    budgetary_resources = get_budgetary_resources(nasa_code, fiscal_year=2024)
    new_awards_count = get_new_awards_count(nasa_code, fiscal_year=2024)

    # Avoid division by zero
    if budgetary_resources > 0:
        ratio = new_awards_count / budgetary_resources
        print(f"NASA's budgetary resources to new awards ratio in FY 2024: {ratio:.5f}")
    else:
        print("Budgetary resources are zero or unavailable.")

except ValueError as ve:
    print(ve)
except requests.exceptions.RequestException as re:
    print(f"Request failed: {re}")
