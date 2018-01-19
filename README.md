# YoutubeVideosDataCrawler
This project crawls youtube videos data by videos url seed.
This project reads seed file located in seed directory. and get all URLS which it has to crawl.
then it crawl URL one by one and get Information like

1- Published Date  
2- Title  
3- Description  
4- Thumbnail Image URL  

we then download image and put it into a directory provided in configuration file in conf/ directory
and put generated XML file into XML directory provided into configuration file in conf/ directory
