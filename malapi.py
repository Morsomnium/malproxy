from urllib import request


class MalAPI:
    mal_api_url = "https://api.myanimelist.net/v2"
    anime_statuses = [
        'watching',
        'completed',
        'on_hold',
        'dropped',
        'plan_to_watch',
    ]
    sorting_options = [
        'list_updated_at',
        'list_score',
        'anime_title',
        'anime_start_date'
    ]

    def __init__(self, token):
        self.user = '@me'
        self.token = token

    def get_anime_list(self, status=anime_statuses[0], sort=sorting_options[0], limit=100, offset=0):
        anime_list_url = f'/users/{self.user}/animelist'
        full_url = self.mal_api_url + anime_list_url
        data = {
            'status': status,
            'sort': sort,
            'limit': limit,
            'offset': offset
        }
        req = request.Request(full_url, data=data, method='GET')
        req.add_header('Authorization', f'Bearer {self.token}')
        anime_list = request.urlopen(req)
        return anime_list
