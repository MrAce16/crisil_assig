import requests

def get_average_loan_amount(state_fips, fiscal_year):
    # Base URL for state awards
    url = f"https://api.usaspending.gov/api/v2/recipient/state/awards/{state_fips}/"
    params = {'fiscal_year': fiscal_year, 'award_type_codes': ['07']}  # '07' is for loan awards
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Validate the data structure
    if not isinstance(data, list):
        raise ValueError("Unexpected API response format. Expected a list of award types.")

    # Extract loan data from the response
    loan_data = next((item for item in data if item['type'] == 'loans'), None)

    if not loan_data or loan_data['count'] == 0:
        return 0  # No loans available for this state and fiscal year

    # Calculate the average loan amount
    total_loans = loan_data['amount']
    count_loans = loan_data['count']

    return total_loans / count_loans

# FIPS code for Texas
texas_fips = '48'
try:
    average_loan_tx = get_average_loan_amount(texas_fips, fiscal_year=2019)
    print(f"Average Loan Amount to Texas in FY 2019: ${average_loan_tx:.2f}")
except Exception as e:
    print(f"Error: {e}")
