import configparser
import requests
import json
import thread
from Finalize import FinalizeVideo



parser = configparser.ConfigParser()
parser.read("conf/configuration.ini")

def confParser(section):
    if not parser.has_section(section):
        print("No section information are available in config file for", section)
        return
    # Build dict
    tmp_dict = {}
    for option, value in parser.items(section):
        option = str(option)
        value = value
        tmp_dict[option] = value
    return tmp_dict

def read_seed_file(file_name):
    videos_list = []
    file = open(file_name,"r")
    line = file.readline().split("\n")[0]
    while line != "":
        videos_list.append(line)
        line = file.readline().split("\n")[0]

    file.close()

    return videos_list

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError

def get_video_details(vid_url, vid_id, key, src, finalize):
    payload = {'id': vid_id, 'part': 'contentDetails,statistics,snippet','key': key}
    l = requests.Session().get('https://www.googleapis.com/youtube/v3/videos', params=payload)
    resp_dict = json.loads(l.content)
    title = resp_dict['items'][0]['snippet']['title']
    img_url = resp_dict['items'][0]['snippet']['thumbnails']['high']['url']
    published_date = resp_dict['items'][0]['snippet']['publishedAt']
    description = resp_dict['items'][0]['snippet']['localized']['description']
    temp = description.split("\n")
    description = "".join(temp)

    finalize.DownloadAndStoreImage(img_url, vid_url, IMAGE_DIR, IMAGE_THUMBNAIL_DIR, src, IMAGE_TOLERANCE, XML_DIR, title, published_date, description)
    #thread.start_new_thread(finalize.DownloadAndStoreImage,(img_url, vid_url, IMAGE_DIR, IMAGE_THUMBNAIL_DIR, src, IMAGE_TOLERANCE, XML_DIR, title, published_date, description))

if __name__ == '__main__':

    general_conf = confParser("general_conf")
    video_urls_seed_file = general_conf['video_urls_seed_file']
    youtube_api_key = general_conf['youtube_api_key']
    IMAGE_TOLERANCE = str_to_bool(general_conf["image_tolerance"])
    IMAGE_THUMBNAIL_DIR = general_conf["srv_thumbnail_dir"]
    IMAGE_DIR = general_conf["image_dir"]
    XML_DIR = general_conf["xml_dir"]
    RETRY_LIMIT = int(general_conf["retry_limit"])
    source = "youtube"

    finalize = FinalizeVideo(RETRY_LIMIT)

    videos_urls_list = read_seed_file(video_urls_seed_file)

    for video_url in videos_urls_list:
        video_id = video_url.split("=")[-1]
        get_video_details(video_url, video_id, youtube_api_key, source, finalize)


