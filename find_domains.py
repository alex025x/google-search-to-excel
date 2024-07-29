import os
import pandas as pd
import requests

def get_domain(company_name, api_key):
    url = f"https://serpapi.com/search.json?q={company_name}&engine=google&api_key={api_key}"
    response = requests.get(url)
    results = response.json()
    try:
        first_result = results['organic_results'][0]['link']
        return first_result
    except (IndexError, KeyError) as e:
        print(f"Error fetching domain for {company_name}: {e}")
        return None

def main():
    # Read API key from env.py
    api_key = env.SERPAPI_KEY

    if not api_key:
        print("Error: SerpAPI key is not set.")
        return

    # Load the CSV file
    try:
        df = pd.read_csv('companies.csv')
    except FileNotFoundError:
        print("Error: companies.csv file not found.")
        return

    # Create a new column for domains
    df['Domain'] = df['Company'].apply(lambda x: get_domain(x, api_key))

    # Save the results back to a new CSV file
    df.to_csv('companies_with_domains.csv', index=False)
    print("Finished processing. The results are saved in 'companies_with_domains.csv'.")

if __name__ == "__main__":
    main()
