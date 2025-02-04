import scrapy
import logging

class AnimeSpider(scrapy.Spider):
    name = "anime"
    allowed_domains = ["myanimelist.net"]
    start_urls = ["https://myanimelist.net/topanime.php?limit=0"]

    # Add a download delay to avoid being blocked
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # 2 seconds delay between requests
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'LOG_LEVEL': 'DEBUG',  # Enable debug logging
    }

    def clean_data(self, data):
        """
        Helper function to clean extracted data.
        Removes empty strings and strips whitespace from lists and strings.
        """
        if isinstance(data, list):
            # Remove empty strings and strip whitespace from each item
            return [item.strip() for item in data if item.strip()]
        elif isinstance(data, str):
            # Strip whitespace from strings
            return data.strip()
        else:
            # Return the data as-is if it's not a list or string
            return data

    def parse(self, response):
        # Extract basic info and URLs from the top anime list
        animes = response.css('tr.ranking-list')
        for anime in animes:
            title = anime.css('h3.fl-l.fs14.fw-b.anime_ranking_h3 a::text').get()
            image_url = anime.css('a.hoverinfo_trigger.fl-l.ml12.mr8 img::attr(data-src)').get()
            score = anime.css('span.score-label::text').get()
            anime_url = anime.css('h3.fl-l.fs14.fw-b.anime_ranking_h3 a::attr(href)').get()

            # Yield a Request for each anime's detail page
            yield scrapy.Request(
                url=anime_url,
                callback=self.parse_anime_page,
                meta={'title': title, 'image_url': image_url, 'score': score}
            )

        # Handle pagination using the `limit` parameter
        current_limit = int(response.url.split('=')[-1])  # Extract the current limit value
        next_limit = current_limit + 50  # Increment by 50 for the next page

        # Stop pagination after a certain limit (e.g., 4400 for 88 pages)
        if next_limit <= 4400:
            next_page_url = f"https://myanimelist.net/topanime.php?limit={next_limit}"
            logging.info(f"Found next page: {next_page_url}")
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            logging.info("No more pages found.")

    def parse_anime_page(self, response):
        try:
            # Extract detailed information using provided selectors
            description = self.clean_data(response.xpath('//p[@itemprop="description"]/text() | //p[@itemprop="description"]/br/following-sibling::text()').getall())
            character_names = self.clean_data(response.xpath('//td[@class="borderClass"]/h3[@class="h3_characters_voice_actors"]/a/text()').getall())
            character_types = self.clean_data(response.xpath('//td[@class="borderClass"]/div[@class="spaceit_pad"]/small/text()').getall())
            voice_actor_names = self.clean_data(response.xpath('//td[@class="va-t ar pl4 pr4"]/a/text()').getall())
            languages = self.clean_data(response.xpath('//td[@class="va-t ar pl4 pr4"]/small/text()').getall())
            character_images = self.clean_data(response.css('div.picSurround img::attr(data-src)').getall())
            voice_actor_images = self.clean_data(response.css('td.va-t.ar.pl4.pr4 + td div.picSurround img::attr(data-src)').getall())

            # Extract review ratios
            statuses = self.clean_data(response.css('div.review-ratio__box a::text').getall())
            numbers = self.clean_data(response.css('div.review-ratio__box a strong::text').getall())

            # Extract additional information
            synonyms = self.clean_data(response.xpath('//div[@class="spaceit_pad"][contains(., "Synonyms")]/text()').getall())
            japanese_title = self.clean_data(response.xpath('//div[@class="spaceit_pad"][contains(., "Japanese")]/text()').getall())
            english_title = self.clean_data(response.xpath('//div[@class="spaceit_pad"][contains(., "English")]/text()').getall())
            anime_type = self.clean_data(response.css('div.spaceit_pad:contains("Type") a::text').get())
            episodes = self.clean_data(response.css('div.spaceit_pad:contains("Episodes")::text').getall())
            status = self.clean_data(response.css('div.spaceit_pad:contains("Status")::text').getall())
            aired = self.clean_data(response.css('div.spaceit_pad:contains("Aired")::text').getall())
            premiered = self.clean_data(response.css('div.spaceit_pad:contains("Premiered") a::text').get())
            broadcast = self.clean_data(response.css('div.spaceit_pad:contains("Broadcast")::text').getall())
            producers = self.clean_data(response.css('div.spaceit_pad:contains("Producers") a::text').getall())
            licensors = self.clean_data(response.css('div.spaceit_pad:contains("Licensors") a::text').getall())
            studios = self.clean_data(response.css('div.spaceit_pad:contains("Studios") a::text').getall())
            source = self.clean_data(response.css('div.spaceit_pad:contains("Source") a::text').getall())
            genres = self.clean_data(response.css('div.spaceit_pad:contains("Genres") a::text').getall())
            themes = self.clean_data(response.css('div.spaceit_pad:contains("Themes") a::text').getall())
            duration = self.clean_data(response.css('div.spaceit_pad:contains("Duration")::text').getall())
            rating = self.clean_data(response.css('div.spaceit_pad:contains("Rating")::text').getall())
            score = self.clean_data(response.css('span[itemprop="ratingValue"]::text').get())
            ranked = self.clean_data(response.css('div.spaceit_pad:contains("Ranked")::text').getall())
            popularity = self.clean_data(response.css('div.spaceit_pad:contains("Popularity")::text').getall())
            members = self.clean_data(response.css('div.spaceit_pad:contains("Members")::text').getall())
            favorites = self.clean_data(response.css('div.spaceit_pad:contains("Favorites")::text').getall())

            # Organize and yield the data
            yield {
                'title': self.clean_data(response.meta.get('title')),
                'image_url': self.clean_data(response.meta.get('image_url')),
                'score': self.clean_data(response.meta.get('score')),
                'description': description,
                'character_names': character_names,
                'character_types': character_types,
                'voice_actor_names': voice_actor_names,
                'languages': languages,
                'character_images': character_images,
                'voice_actor_images': voice_actor_images,
                'statuses': statuses,
                'numbers': numbers,
                'synonyms': synonyms,
                'japanese_title': japanese_title,
                'english_title': english_title,
                'type': anime_type,
                'episodes': episodes,
                'status': status,
                'aired': aired,
                'premiered': premiered,
                'broadcast': broadcast,
                'producers': producers,
                'licensors': licensors,
                'studios': studios,
                'source': source,
                'genres': genres,
                'themes': themes,
                'duration': duration,
                'rating': rating,
                'score_detail': score,
                'ranked': ranked,
                'popularity': popularity,
                'members': members,
                'favorites': favorites,
            }
        except Exception as e:
            logging.error(f"Error processing {response.url}: {e}")
