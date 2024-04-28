import requests
from bs4 import BeautifulSoup
from consts import HEADERS, BASE_URL


def get_squads_from_team(team_url):
    # TODO: loop through all the years until no result
    url = BASE_URL + team_url

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        responsive_div = soup.find('div', class_='responsive-table')

        if responsive_div:
            items_table = responsive_div.find('table', class_='items')

            if items_table:
                rows = items_table.find_all('tr', class_=["odd", "even"])
                data_list = []
                for row in rows:
                    # Getting the wanted data by the class of the td
                    player_number_elem = row.select_one('.rn_nummer')
                    player_number = player_number_elem.text.strip() if player_number_elem else None

                    image_link_elem = row.select_one(
                        '.bilderrahmen-fixed.lazy')
                    image_link = image_link_elem['data-src'] if image_link_elem else None

                    player_name_elem = row.select_one('.hauptlink')
                    player_name = player_name_elem.text.strip() if player_name_elem else None

                    birth_date_elem = row.select_one(
                        'td.zentriert:nth-of-type(3)')
                    birth_date_text = birth_date_elem.text.strip() if birth_date_elem else None

                    birth_date, age_at_club = map(str.strip,
                                                  birth_date_text.rsplit('(', 1) if birth_date_text else (None, None))
                    age_at_club = age_at_club[:-1] if age_at_club else None

                    nationality_elem = row.select_one('.flaggenrahmen')
                    nationality = nationality_elem['title'] if nationality_elem else None

                    profile_ref_elem = row.select_one('.hauptlink a')
                    profile_ref = profile_ref_elem['href'] if profile_ref_elem else None

                    position_elem = row.select(
                        '.posrela table td:nth-of-type(1)')[-1]
                    position = position_elem.text.strip() if position_elem else None

                    print("\nPlayer Name:", player_name)
                    print("Player Number:", player_number)
                    print("Image Link:", image_link)
                    print("Birth Date:", birth_date)
                    print("Age at Club:", age_at_club)
                    print("Nationality:", nationality)
                    print("Profile Reference:", profile_ref)
                    print("Position:", position)
                    data_list.append((player_name, player_number, image_link,
                                      birth_date, age_at_club, nationality, profile_ref, position))

                return data_list
            else:
                print("Table with class 'items' not found.")
        else:
            print("Div with class 'responsive-table' not found.")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

    raise "Error retrieving the web page. Status code: " + \
        str(response.status_code)


def get_teams_from_league(league_url):
    url = BASE_URL + league_url

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        responsive_div = soup.find('div', class_='responsive-table')

        if responsive_div:
            items_table = responsive_div.find('table', class_='items')

            if items_table:
                rows = items_table.find_all(
                    'td', class_='zentriert no-border-rechts')

                data_list = []

                for row in rows:
                    a_tag = row.find('a')
                    title = a_tag.get('title') if a_tag else None
                    href = a_tag.get('href') if a_tag else None

                    img_src = row.find('img')['src'] if row.find(
                        'img') else None

                    data_list.append((title, href, img_src))

                return data_list
            else:
                print("Table with class 'items' not found.")
        else:
            print("Div with class 'responsive-table' not found.")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

    raise "Error retrieving the web page. Status code: " + \
        str(response.status_code)
    return []


def print_tuple_list(tuple_list):
    print("\n".join(list(map(lambda x: str(x), tuple_list))))


# print_tuple_list(get_teams_from_league(
#     "/ligat-haal/startseite/wettbewerb/ISR1"))
get_squads_from_team("/maccabi-tel-aviv/startseite/verein/119/saison_id/2023")
