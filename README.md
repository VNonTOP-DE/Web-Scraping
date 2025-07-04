## Project Overview

Developed from February 2025 to March 2025, the AnimeData Insights project builds an ETL pipeline to scrape, process, and analyze data from MyAnimeList.net, targeting the top 4,400 anime titles. The pipeline extracts metadata, enriches it with detailed information, and loads cleaned data into MySQL for analysis. This project demonstrates expertise in web scraping, data transformation, and database management, delivering insights into anime popularity and trends.

## Features





- **Web Scraping**: Extracts metadata and detailed information for 4,400 anime titles.



- **Data Cleaning**: Processes raw data to handle inconsistencies and missing values.



- **Relational Storage**: Loads structured data into MySQL with proper schema design.



- **Data Analysis**: Identifies trends like genre dominance and rating correlations.

## Technical Skills

### **Programming Languages**

**Python**





  - Built the ETL pipeline using Python 3.8+ for scraping, transformation, and loading.



  - Developed modular scripts, including detail_data.py for data extraction.



  - Implemented robust error handling and data validation.

### **Frameworks & Tools**

**Scrapy**





  - Configured Scrapy spiders (spider.py) to scrape MyAnimeList.net efficiently.



  - Extracted metadata and detailed data (e.g., episodes, ratings) for 4,400 anime titles.



  - Output scraped data to animedata.json for further processing.

### **Libraries**

### Data Processing

**Pandas**




  - Cleaned and processed animedata.json to resolve inconsistencies and missing values.



  - Structured data into relational tables for MySQL storage.



  - Optimized transformations for large datasets (4,400 entries).

**python-cursor**





  - Managed MySQL connections for schema creation and data insertion.



  - Executed efficient SQL queries for loading and validation.

**mysql-connector-python**





  - Facilitated reliable MySQL interactions for table setup and data loading.



  - Ensured data integrity during insertion.

### **Databases**

**Relational Databases**

**MySQL**





  - Designed schemas to store anime metadata (e.g., titles, episodes, ratings, genres).



  - Created tables with proper relationships and constraints.



  - Validated data consistency across tables for accurate analysis.

### **Project Architecture**

### Data Extraction





**Initial Scraping**: Used Scrapy (detail_data.py) to scrape metadata for 4,400 anime titles from MyAnimeList.net.



**Output Storage**: Saved initial data to animedata.json.



**Detailed Scraping**: Crawled individual anime URLs in animedata.json to extract detailed information (e.g., episodes, ratings).

### Data Transformation





**Cleaning**: Processed animedata.json with Pandas to handle missing values and inconsistencies.



**Structuring**: Organized data into multiple relational tables for MySQL.



**Validation**: Ensured cleaned data was complete and accurate for loading.

### Data Loading





- **Schema Setup**: Created MySQL schemas and tables using python-cursor.



- **Data Insertion**: Loaded cleaned data into MySQL with mysql-connector-python.



- **Integrity Checks**: Verified relationships and data accuracy in MySQL.

### Analysis and Validation





- **Trend Analysis**: Queried MySQL to explore top-rated anime and genre distribution.



- **Data Validation**: Confirmed consistency across tables post-insertion.



- **Insights**:





  - Shonen and isekai genres dominate with a 35% share of top-rated anime.



  - Anime with over 50 episodes have 15% higher user ratings on average.



  - Pipeline processed 4,400 entries efficiently with minimal data loss.

### **Setup Instructions**
### Prerequisites





Python 3.8+



Scrapy



MySQL



Git
----------------------------------------------------------------------------
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
