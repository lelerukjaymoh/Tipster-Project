import requests
import bs4
import re


class Featured:
    def __init__(self, page_url):
        self.page_url = page_url

    def getgames(self):
        page = requests.get(self.page_url)
        game_info = []
        try:
            page.raise_for_status()
        except Exception as error:
            print('There was a problem getting cash1 data: %s' % error)
        cash_soup = bs4.BeautifulSoup(page.text, 'html.parser')
        if type(cash_soup) == bs4.BeautifulSoup:
            games = cash_soup.findAll("span", style="font-family: sans-serif;")
            games_num = len(games)
            print(games[2].getText())
            for match in range(games_num):
                get_reg = re.compile(r'(.*?)\s*(12|1x|1|2|x2|x|(un|ov)\d+.\d+)\s*(@\d+.\d+)')
                game_info.append(get_reg.findall(games[match].getText()))

        return game_info
