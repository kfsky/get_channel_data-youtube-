from apiclient.discovery import build
from apiclient.errors import HttpError
import pandas as pd

# get API
API_KEY = 'your_api_key'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)


# get video data
def get_video_datas(CHANNEL_ID):

    channels = []
    searches = []
    videos = []

    nextPagetoken = None
    nextpagetoken = None

    channel_response = youtube.channels().list(
        part='snippet, statistics',
        id=CHANNEL_ID,
    ).execute()

    for channel_result in channel_response.get('items', []):
        if channel_result['kind'] == 'youtube#channel':
            channels.append([channel_result['snippet']['title'],
                             channel_result['statistics']['subscriberCount'],
                             channel_result['statistics']['videoCount'],
                             channel_result["snippet"]["publishedAt"]])

    while True:
        if nextPagetoken != None:
            nextpagetoken = nextPagetoken

        search_response = youtube.search().list(
            part='snippet',
            channelId=CHANNEL_ID,
            maxResults=50,
            order='date',
            pageToken=nextpagetoken
        ).execute()

        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                searches.append(search_result['id']['videoId'])

        try:
            nextPagetoken = search_response["nextPageToken"]

        except:
            break

    for result in searches:
        video_response = youtube.videos().list(
            part='snippet, statistics',
            id=result,
        ).execute()

        for video_result in video_response.get('items', []):
            if video_result['kind'] == 'youtube#video':
                videos.append([video_result['snippet']['title'],
                               video_result['statistics']['viewCount'],
                               video_result['statistics']['likeCount'],
                               video_result['statistics']['dislikeCount'],
                               video_result['statistics']['commentCount'],
                               video_result['snippet']['publishedAt']])

    return channels, videos


def write_csv(channels, videos):
    videos_report = pd.DataFrame(videos, columns=['title', 'viewCount', 'likeCount', 'dislikeCount',
                                                  'commentCount', 'publishedAt'])
    videos_report.to_csv("videos_report.csv", index=None)

    channel_report = pd.DataFrame(channels, columns=['title', 'subscriberCount', 'videoCount', 'publishedAt'])
    channel_report.to_csv("channels_report.csv", index=None)


CHANNEL_ID = 'target_channel_id'
channels, videos = get_video_datas(CHANNEL_ID)
write_csv(channels, videos)

print('end')



