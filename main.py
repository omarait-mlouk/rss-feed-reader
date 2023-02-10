import json
import sys
import requests
from bs4 import BeautifulSoup

# Get the elements from the command line arguments
urls = sys.argv[1:]


def read_rss_feed(url):
    """
       Read an RSS feed from the given URL and extract the title, description, and link of each item.
    """
    try:
        # Make a GET request to the URL
        response = requests.get(url)

        # check if the request was successful
        if response.status_code == 200:
            # Parse the RSS feed data using BeautifulSoup
            soup = BeautifulSoup(response.content, "lxml")

            items = []
            # Extract the information from each item
            for item in soup.find_all("item"):
                title = item.find("title").text
                link = item.find("guid").text
                description = item.find("description").text
                if description:
                    # remove the CDATA section
                    description = description.replace("<![CDATA[", "").replace("]]>", "")
                else:
                    description = "No description available."
                link = item.find("guid").text
                items.append({"title": title, "description": description, "link": link})
                output = f"Title: {title}\nDescription: {description}\nLink: {link}\n"
                # Print the information
                print(output)
            with open("data.json", "w") as file:
                json.dump(items, file, indent=2)
            print("Data saved to file successfully")
        else:
            # handle non-200 response status codes
            raise Exception(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        # handle request exceptions
        print(f"Request error: {e}")
    except Exception as e:
        # handle other exceptions
        print(f"Error: {e}")


for url in urls:
    read_rss_feed(url)
