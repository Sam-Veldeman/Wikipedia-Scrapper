from Scraper.leaders_scraper import get_leaders, save, count_leaders

def main():
    # Start the scraper and get the leaders data
    leaders_data = get_leaders()

    # Save the leaders data to a JSON file
    save(leaders_data)
    print("Leaders data saved successfully.")

    count_leaders(get_leaders())

if __name__ == "__main__":
    main()