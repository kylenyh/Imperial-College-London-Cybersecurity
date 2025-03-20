# Scenario: Creating a SQL Injection Scanner for a bank

# Problem: 
# You are a cybersecurity analyst working for a financial services company. 
# The company has recently launched a new customer portal that includes login forms, search functionalities, and feedback submission features.
# Due to the sensitive nature of financial data, your team is responsible for testing the website for vulnerabilities. 
# One of the key tasks in this assessment is to check whether the website is susceptible to SQL Injection attacks, which can lead to unauthorized access to the database.

# Beautiful Soup is a library that makes it easy to scrape information from web pages. 
# It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.

# Import the libraries 
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

# Initialize an HTTP session with a user-agent to mimic a browser
s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

# Function that fetches all forms from the given URL using BeautifulSoup
def get_all_forms(url):
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")

# Function that extracts and returns form details such as action, method and inputs
def get_form_details(form):
    return {
        "action": form.attrs.get("action", "").lower(),
        "method": form.attrs.get("method", "get").lower(),
        "inputs": [
            {"type": i.attrs.get("type", "text"), "name": i.attrs.get("name"), "value": i.attrs.get("value", "")}
            for i in form.find_all("input")
        ],
    }

# Function that checks for common SQL error messages in the response indicating vulnerability
def is_vulnerable(response):
    errors = {"you have an error in your sql syntax;", "warning: mysql", "unclosed quotation mark", "quoted string not properly terminated"}
    return any(error in response.content.decode().lower() for error in errors)

# Function that performs SQL injection scan on the URL and its forms
def scan_sql_injection(url):
    # Test for URL-based SQL Injection
    for c in "\"'":
        test_url = f"{url}{c}"
        print(f"[!] Trying {test_url}")
        if is_vulnerable(s.get(test_url)):
            print(f"[+] SQL Injection vulnerability detected at {test_url}")
            return

    # Extracts forms for further testing
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")

    # Tests forms for SQL Injection
    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            # Prepare data payload by injecting test input
            data = {i['name']: (i['value'] + c if i['type'] == 'hidden' or i['value'] else f"test{c}") for i in form_details['inputs'] if i.get('name')}
            target_url = urljoin(url, form_details['action'])
            res = s.post(target_url, data=data) if form_details['method'] == 'post' else s.get(target_url, params=data)
            
            if is_vulnerable(res):
                print(f"[+] SQL Injection vulnerability detected at {target_url}")
                print(f"[+] Form Details: {form_details}")
                return

if __name__ == "__main__":
    # Target URL for scanning
    url = "https://www.lloydsbank.com/"
    scan_sql_injection(url)
