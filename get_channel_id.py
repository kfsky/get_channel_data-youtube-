from apiclient.discovery import build
import pandas as pd


# get API key
API_KEY = 'your_api_key'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)


def get_channel_id(keyword):
    search_response = youtube.search().list(
        q=keyword,
        part='id, snippet',
        maxResults=25
    ).execute()

    channels = []

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#channel':
            channels.append([search_result['snippet']['title'],
                           search_result['id']['channelId']])

    return channels


search = input('keyword:')
results = get_channel_id(search)

dfs = pd.DataFrame(results, columns=['channel', 'id'])
dfs.to_csv('./search_id.csv', index=None)

print('end')
