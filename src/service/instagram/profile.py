import json
import bs4
import requests
from fake_headers import Headers

class Instagram:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build_param(username):
        params = {
            'username': username,
        }
        return params

    @staticmethod
    def build_headers(username):
        return {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'referer': f'https://www.instagram.com/{username}/',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': Headers().generate()['User-Agent'],
            'x-asbd-id': '198387',
            'x-csrftoken': 'VUm8uVUz0h2Y2CO1SwGgVAG3jQixNBmg',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': '0',
            'x-requested-with': 'XMLHttpRequest',
        }

    @staticmethod
    def make_request(url, params, headers, proxy=None):
        response = None
        if proxy:
            proxy_dict = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            response = requests.get(
                url, headers=headers, params=params, proxies=proxy_dict)
        else:
            response = requests.get(
                url, headers=headers, params=params)
        return response

    @staticmethod
    def scrap(username, proxy = None):
        try:
            headers = Instagram.build_headers(username)
            params = Instagram.build_param(username)
            response = Instagram.make_request('https://www.instagram.com/api/v1/users/web_profile_info/',
            headers=headers, params=params, proxy=proxy)
            if response.status_code == 200:
                profile_data = response.json()['data']['user']
                return json.dumps(profile_data)
            else:
                print('Error : ', response.status_code, response.text)
        except Exception as ex:
            print(ex)
    
    @staticmethod
    def posts(short_code,username, proxy = None):
        headers = Instagram.build_headers(username)
        params = Instagram.build_param(username)
        response = Instagram.make_request(f'https://instagram.com/p/{short_code}',
        headers=headers, params=params, proxy=proxy)
        if response.status_code == 200:
            # profile_data = response.json()['data']['user']
            # return json.dumps(profile_data)
            html = bs4.BeautifulSoup(response.text, 'html.parser')
            # find the meta tag containing the link to the post's media.
            meta = html.find(attrs={"property": "al:ios:url"})
            media_id = meta.attrs['content'].replace("instagram://media?id=", "")
            print(media_id)
            # use the media id to get the same response as ?__a=1 for the post.
            media_api_url = f"https://i.instagram.com/api/v1/media/{media_id}/info"
            print(media_api_url)
            print(headers)
            media_api_response = requests.get(media_api_url,headers=headers)
            # print(media_api_response.text)
            # htmls = bs4.BeautifulSoup(media_api_response.text, 'html.parser')
            # print(htmls)
            # media_json = media_api_response.json()
            # return json.dumps(media_json)
        else:
            print('Error : ', response.status_code, response.text)

