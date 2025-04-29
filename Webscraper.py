import os
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import httpx
import pandas as pd

# Here you specify the path you would like to save the commands. I recomend to make a new folder to store the pds if tyoue doing multiple. 
desktop_path = r"C:\Users\chaos\OneDrive\Desktop\LinuxCommands"

def is_valid_command(command):
    """
    Check if the extracted text is a valid Linux command.
    - Should be a single word (no spaces).
    - Should not contain numbers or mixed case.
    """
    return command.isalpha() and command.islower() and len(command) <= 30 #ehre we check to see if the command contains alpha characters, checks to see if its lowercase (most ere), and if its less that 30 characters. 
#i did this as it was picking up a lot of uncessisary information!! 

def fetch_linux_commands(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print(f"Website does not allow us to scrape them :( {url}")
        return [] #here we specifc the rules fdor scraping. If we get something otheer than code 200(successful), we will show a message indicating so.

    soup = BeautifulSoup(response.text, "html.parser") # Contains the raw HTML conetent that was recieved. Ut uses html parser to parse the response text
    commands_with_desc = [] #here, as the commands and secriptions are being processes, they will be stores here. 

    # Extract from tables (structured format)
    for row in soup.find_all("tr"):  
        cells = row.find_all("td")
        if len(cells) >= 2:
            command = cells[0].get_text(strip=True)
            description = cells[1].get_text(strip=True)
            if is_valid_command(command) and description:
                commands_with_desc.append((command, description)) # a lot of the sites had commands and descriptions in tables formats. So this was a must. 

    #Extract from lists (<ul>/<ol> with <li>)
    for item in soup.find_all("li"): #searches through all list items in a html document. 
        text = item.get_text(strip=True) #extarcts all text content from the current List itme removing the tag away fdrom it. 
        parts = text.split(" ", 1)  #This splits the content into 2 parts. This was a must for commands as most websites has commands lists as follows::: LS, List directory contents.
        if len(parts) == 2: #checks to see if more there are more than two parts. (pissible a white space).
            command, description = parts #If the the split prodes 2 parts (1 being command and the other being description).
            if is_valid_command(command) and description:
                commands_with_desc.append((command, description)) # Did you read this Christian? I hope you are.  

    return commands_with_desc #ez

def save_to_pdf(commands_with_desc, filename="linux_commands.pdf"):
    file_path = os.path.join(desktop_path, filename)
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    margin = 50
    max_width = width - 2 * margin  
    y_position = height - 40 # saves the commands tro a PDF.

    for cmd, desc in commands_with_desc:
        if y_position < 60:
            c.showPage()
            y_position = height - 40 # ensures that content is properly spaced!! I added this as the descritipns were getting cut off!!!! :(

        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y_position, cmd)
        y_position -= 20  # dumb things.

        c.setFont("Helvetica", 10)
        wrapped_text = simpleSplit(desc, "Helvetica", 10, max_width)
        for line in wrapped_text:
            c.drawString(margin, y_position, line)
            y_position -= 15  #dumb

        y_position -= 10  

    c.save()
    print(f"Saved to {file_path}") #just saces


# Add automated webscraper

def google_search(api_key, search_engine_id, query, **params):
    base_url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        **params
    }
    response = httpx.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

api_key = 'AIzaSyCVVjKbXuMiTM0Z8BVd4PNa5C0IePGNaLs'
search_engine_id = 'f759b83bdd6034a84' 
query = 'Linux Commands'

# Store URLs in a list
urls = []

# Loop to fetch up to 100 results (limited by API)
for i in range(1, 100, 10):
    response = google_search(
        api_key=api_key,
        search_engine_id=search_engine_id,
        query=query,
        start=i
    )
    items = response.get('items', [])  # Extract 'items' which contains search results
    urls.extend(item['link'] for item in items if 'link' in item)  # Store URLs in the list



if __name__ == "__main__":
    all_commands_with_desc = []
    for url in urls:
        all_commands_with_desc.extend(fetch_linux_commands(url))

    filtered_commands = [(cmd, desc) for cmd, desc in all_commands_with_desc if desc.strip()] # we filter out ocmmands with no description as som edid have some. 

    if filtered_commands:
        save_to_pdf(filtered_commands)
    else:
        print("No valid Linux commands found.")