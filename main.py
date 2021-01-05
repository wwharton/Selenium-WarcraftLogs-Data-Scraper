from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re


def populate_player_list():
    # For querying a list of player names separated by line breaks
    with open('PlayerList.txt', 'r', encoding='utf-8') as f1:
        PlayerList_ref = []
        for line in f1.readlines():
            PlayerList_ref.append(line.strip('\n'))
    return PlayerList_ref


def convert_api_output():
    # For querying a list of player names separated by other lines of data
    with open('PlayerListFromAPI.txt', 'r', encoding='utf-8') as f1:
        PlayerList_ref = []
        lines = f1.readlines()
        target_lines = lines[0::4]
        for line in target_lines:
            PlayerList_ref.append(line.strip('\n'))
    return PlayerList_ref


def main():

    # reads player list in from a lightly formatted txt file
    players = convert_api_output()

    # If you wanted to query your own list of players,
    #   this alternative func below will take a plain text
    #   list of player names separated by line breaks

    # players = populate_player_list()

    # Initialize headless Chrome Driver
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options, service_args=['--log-path=/chromedriver.log'])

    with open('Completed.txt', 'a', encoding='utf-8') as Completed_txt:
        # Finished and Current vars used to track progress ~
        finished = len(players)
        current = 1

        for player in players:
            url = f'https://classic.warcraftlogs.com/character/us/atiesh/{player}'
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            text_to_parse = str(soup.find(class_='median-and-all-star'))
            pattern = re.compile(r'\d\d\.\d\d?')
            matches = pattern.findall(text_to_parse)

            # prints and formats output into final txt file
            for match in matches:
                print(f'{player}, {match}', file=Completed_txt)

            # tracks progress
            print(f'{current} / {finished}')
            current = current + 1

if __name__ == '__main__':
    main()


