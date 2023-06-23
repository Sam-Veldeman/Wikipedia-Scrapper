"""
importing the needed libraries
"""
import requests, re, json
from bs4 import BeautifulSoup
"""
Create global variable 'urls' dictionary for ease of use and readability of code later on.
"""
urls =  {
        'root_url' : 'https://country-leaders.onrender.com',
        'status_url' : 'https://country-leaders.onrender.com/status',
        'countries_url' : 'https://country-leaders.onrender.com/countries',
        'cookie_url' : 'https://country-leaders.onrender.com/cookie',
        'leaders_url' : 'https://country-leaders.onrender.com/leaders'
        }
"""""
Define a function 'get_first_parapraph' to scrape the 1st paragraph on the wikipedia_url that is found in the 'leaders_per_country' library returned from the 'get_leaders' function
"""""
def get_first_paragraph(wikipedia_url, session):
    #print(wikipedia_url)
    regex_list = [
    r"\[\d+\]",                 # Matches a pattern that starts with an opening square bracket, followed by one or more digits, and ends with a closing square bracket.
    r"\[[^\]]*\]|\([^)]*\)",    # Matches patterns enclosed in square brackets or parentheses.
    r"\n",                      # Matches a newline character.
    r"\t",                      # Matches a tab character.
    r"\xa0",                    # Matches a non-breaking space character.
    r"\([^)\s]+\s?\)",          # Matches patterns enclosed in parentheses.
    r"\s?\[.*?\]\s?",           # Matches patterns enclosed in square brackets with optional spaces.
    r"\s?\/.+\/[e].*",          # Matches a pattern that starts with an optional space, followed by a forward slash, any character one or more times (except newline), followed by "/[e]", and then followed by any characters zero or more times.
    r"\s?\/.+\/.",              # Matches a pattern that starts with an optional space, followed by a forward slash, any character one or more times (except newline), and then followed by any characters zero or more times.
]    
    soup = BeautifulSoup(session.get(wikipedia_url).text, "html.parser")
    paragraphs = soup.find_all("p")
    first_paragraph = None
    for paragraph in paragraphs:
        if paragraph.find_parent(class_="bandeau-cell") or paragraph.find_parent(class_="plainlist"): #this if is to exclude the 
            continue
        else:
            if paragraph.text.strip():
                first_paragraph = paragraph.text
                replace_string = ""
                for r in regex_list:
                    first_paragraph = re.sub(r,replace_string, first_paragraph,)
                break
    return first_paragraph
"""""
Define a function 'get_leaders' to itterate over the leaders in the 'leaders_per_country' dictionary and adding the 1st paragraph of each wiki url to the 'leader_per_country' dictionary for each leader in the dictionary.
"""""
def get_leaders():
    session = requests.Session()
    cookie = session.get(urls['cookie_url']).cookies              # makes a cookies request using the session method from requests. 
    countries = session.get(urls['countries_url'], cookies=cookie)  # makes countries request using the session method from requests.  
    leaders_per_country = {country: requests.get(urls['leaders_url'], params={"country": country}, cookies=cookie).json() for country in requests.get(urls['countries_url'], cookies=cookie).json()}
    for country in countries.json():
        while True:
            try:
                leaders = requests.get(urls['leaders_url'], params= {"country": country}, cookies=cookie)
                if leaders.status_code == 403:  # Check if cookies have expired
                    cookie = session.get(urls['cookie_url']).cookies  # Refresh the cookies
                    continue
                else:
                    leaders = leaders.json()
                    leaders_per_country[country] = []
                    for leader in leaders:
                        leader["first_paragraph"] = get_first_paragraph(leader["wikipedia_url"], session)
                        leaders_per_country[country].append(leader)
                        print(f"Name: {leader['first_name']} {leader['last_name']}")
                        print(f"First Paragraph: {leader['first_paragraph']}")
                        print()
                break
            except Exception as e:
                print(f"An error occurred for country '{country}': {str(e)}")
                break
    return leaders_per_country
"""
Define a function 'save' to save the leaders__per_country dictionary to a leaders.json file. This file is located in the project directory.
"""
def save(leaders_per_country):
    # Save the data as JSON file
    with open('leaders.json', 'w') as fp:
        json.dump(leaders_per_country, fp)
        
def count_leaders(leaders_per_country):
    total_leaders = 0

    for country, leaders in leaders_per_country.items():
        num_leaders = len(leaders)
        total_leaders += num_leaders
        print(f"Country: {country}, Number of Leaders: {num_leaders}")

    print(f"Total Number of Leaders: {total_leaders}")