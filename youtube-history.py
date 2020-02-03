#Get a key here: https://developers.google.com/youtube/v3/getting-started
#A key is not essential. It is only to get the length of a youtube video

YOUR_API_KEY = ""


#Get your youtube data here: https://takeout.google.com
#Follow this tutorial by Scoby Tech: https://www.youtube.com/watch?v=zlzzO1e6dws

HTML_FILE = "/Users/Ayoola_PC/Downloads/takeout-20200123T180813Z-001/Takeout/YouTube/history/watch-history.html"
#alternatively, 
#HTML_FILE = "watch-history.html"



###importing packages

from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import json



###defining functions

def match_class(target): 
    """    Gets a specific class from a html target (Resource: https://stackoverflow.com/a/11346297)
    Input: div tags before target
    Output: text of matches
    """    

    def do_match(tag):                                                          
        classes = tag.get('class', [])                                          
        return all(c in classes for c in target)                                
    return do_match 


def texttomatches(textfile): 
    """    Gets instances of youtube video history from html text file (Resource: https://stackoverflow.com/a/1454936)
    Input: string of videos html data
    Output: list of matches
    """

    pattern = re.compile(r'(?<=\<div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"\>)(.*?)(?=\</div\>,)')
    return re.findall(pattern, textfile)


def matchestodetails(match):
    """    Gets the useful metadata from each match
    Input: string from texttomatches function
    
    Outputs: 
    video_name: title of video, 
    video_link: link to YouTube video, 
    channel_name: name of YouTube channel, 
    channel_link: link to YouTube channel, 
    date: date video was watched
    """

    pattern_link = re.compile(r'(?<=\<a href\=")(.*?)(?="\>)')
    video_link, channel_link = re.findall(pattern_link, match)

    pattern_name = re.compile(r'(?<="\>)(.*?)(?=\</a\>\<br/\>)')
    video_name, channel_name = re.findall(pattern_name, match)

    pattern_date = re.compile(r'(?<=\</a\>\<br/\>)(.*?)(?=$)')
    date_pre = re.findall(pattern_date, match)[0]
    date = re.findall(pattern_date, date_pre)[0]
    
    return video_name, video_link, channel_name, channel_link, date


def getvideoid(videourl): 
    """    Gets the id of a youtube video from its link. Used for querying the YouTube Data API
    Input: string, e.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ
    Output: id string, e.g. dQw4w9WgXcQ
    """

    return videourl.replace('https://www.youtube.com/watch?v=', '')


def urltotime(url_list, apikey = YOUR_API_KEY): 
    """    Gets the length of a video from the YouTube Data API. (Resource: https://stackoverflow.com/a/15605838)
    Input: a list of video ids
    Output: a list of the lengths of the respective videos
    """

    separator = ','
    urlstoevaluate = separator.join(url_list) #joins urls in list

    url = 'https://www.googleapis.com/youtube/v3/videos?id=' + urlstoevaluate + '&part=contentDetails&key=' + apikey
    request  = requests.get(url)
    data = request.text
    json_output = json.loads(data)['items'] #converts the text output as a dictionary
    return [x['contentDetails']['duration'] for x in json_output]


def extracttime(inputstring): 
    """    Converts the time to seconds 
    Input: string from urltotime function, e.g. PT6M27S
    Output: string of length in seconds, e.g. 747
    """

    inputstring = inputstring.replace('PT', '')

    pattern_minutes = re.compile(r'\d*(?=M)')
    minutes = re.findall(pattern_minutes, inputstring)

    pattern_seconds = re.compile(r'\d*(?=S)')
    seconds = re.findall(pattern_seconds, inputstring)

    try: 
        totalseconds = int(minutes[0]) * 60 + int(seconds[0])
    except: 
        try: 
            totalseconds = int(minutes[0])
        except: 
            totalseconds = int(seconds[0])

    return totalseconds



###extracting data

histfile = open(HTML_FILE, 'r', encoding = 'utf8') #open html file

soup = BeautifulSoup(histfile, 'html.parser') #parse with beautiful soup

textfile =  str(soup.find_all(match_class(["content-cell",  "mdl-cell",  "mdl-cell--6-col", "mdl-typography--body-1"]))) #extract relevant class

matches = texttomatches(textfile) #extract relevant matches

video_details_list = [] 
for match in matches: #extracts details from matchess
    try: 
        video_details_list.append(matchestodetails(match))
    except ValueError: 
        pass

video_history_df = pd.DataFrame(video_details_list) #converting list of lists to pandas dataframe
video_history_df.columns = ['Video_Title', 'Video_URL', 'Channel', 'Channel_URL', 'Date_Watched'] #renaming columns


print('Finished extracting videos \n', video_history_df.head(10))



###Extracting video lengths

Video_Length = []
for x in range(45, len(video_history_df), 45): #url request can only handle 50 ids at once

    urllist = [getvideoid(url) for url in video_history_df['Video_URL'][x - 45:x]]
    batch = urltotime(urllist)
    for y in batch: 
        try: 
            Video_Length.append(extracttime(y))
        except: 
            print(y)

if len(Video_Length) != len(video_history_df): #checking for ommitted entries
    difference = len(video_history_df) - len(Video_Length)
    urllist = [getvideoid(url) for url in video_history_df['Video_URL'][len(Video_Length):]]
    print(len(urllist))
    batch = urltotime(urllist)
    for y in batch: 
        try: 
            Video_Length.append(extracttime(y))
        except: 
            print(y)

assert(len(Video_Length) == len(video_history_df))

video_history_df['Video_Length'] = Video_Length
print('Finished extracting video lengths \n', video_history_df.head(10))
