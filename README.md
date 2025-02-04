# Web-Scraping
Using Python to scrawl data from Myanimelist.net
I Download Info of top 4400 Anime on MyAnimeList.Net (Code in the file detail_data.py)
Then Save the data i scrawl into a json file call 'animedata.json'
I wrote a new code that go in every url in the file 'anime.json' i scrawled and get detail infomation of every 4400 animes. The data also cleaned.
How to run: 
1. Open CMD, cd to the file scrapy which have folder venv (already activate scrapy project),active venv on cmd by typing: venv\scripts\activate
2. pip install scrapy
3. cd to folder spiders , paste the code in the reposities : scraping code (full) to the file spider.py (remember to change file name or moving files that you need to use)
4. in cmd, type   scrapy crawl [spider_name] -o anime.json    to save file
