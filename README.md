# youtube-history


The program takes an html file of the youtube history data and converts it into a Pandas dataframe that can be exported. 

The html file can be obtained from a Google user's [Takeout](https://takeout.google.com) page by following the instructions in this [video](https://www.youtube.com/watch?v=zlzzO1e6dws)

Obtaining an API key from [Google Developers](https://developers.google.com/youtube/v3/getting-started) adds the length of the videos watched to the dataframe. 

#### Initial HTML File
<img src="https://github.com/ayoola-babatunde/youtube-history/blob/master/ReadMe%20images/watch-history-html.png" alt="HTML file" width="650"/>

#### Final Dataframe
<img src="https://github.com/ayoola-babatunde/youtube-history/blob/master/ReadMe%20images/dataframe-final.png" alt="Dataframe" width="1000"/>

One of the challenges encountered in this project was using regular expressions to obtain video urls, watch dates, times, and so on. 

I would love to do some analysis on the patterns in my own data. For example, what channels I watch the most in a month, how much the time I spend on Youtube changes over time, what genre of videos I like, and so on. I would have loved to have information about repeated watchings of the same video, but the history data resets every time a video is watch. 

### In Progress
* Adding OAuth so that a person can just run the program and sign in to their Google Account
* Adding a Bokeh plot to generate dynamic user-determined plots. For example, the most viewed channels in a specified time interval. 
* Generating a word cloud of most common terms in video titles
