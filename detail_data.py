Code scrawl specific data using the url we got from animedata.json
Also added Clean Process

---------------------------------------------------------------------
import scrapy
import json


class AnimeDetailSpider(scrapy.Spider):
    name = "anime_detail"
    allowed_domains = ["myanimelist.net"]

    def start_requests(self):
        # Load URLs from the JSON file
        with open('animedata.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        # Start with the first entry
        if self.data:
            first_entry = self.data[0]
            yield scrapy.Request(url=first_entry['url'], callback=self.parse_anime_page, meta={'index': 0})

    def clean_data(self, data):
        """
        Helper function to clean extracted data.
        Removes empty strings and strips whitespace from lists and strings.
        """
        if isinstance(data, list):
            return [item.strip() for item in data if item.strip()]
        elif isinstance(data, str):
            return data.strip()
        else:
            return data

    def parse_anime_page(self, response):
        index = response.meta['index']

        # Extract detailed information
        description = self.clean_data(response.xpath(
            '//p[@itemprop="description"]/text() | //p[@itemprop="description"]/br/following-sibling::text()').getall())
        character_names = self.clean_data(
            response.xpath('//td[@class="borderClass"]/h3[@class="h3_characters_voice_actors"]/a/text()').getall())
        character_types = self.clean_data(
            response.xpath('//td[@class="borderClass"]/div[@class="spaceit_pad"]/small/text()').getall())
        voice_actor_names = self.clean_data(response.xpath('//td[@class="va-t ar pl4 pr4"]/a/text()').getall())
        languages = self.clean_data(response.xpath('//td[@class="va-t ar pl4 pr4"]/small/text()').getall())
        character_images = self.clean_data(response.css('div.picSurround img::attr(data-src)').getall())
        voice_actor_images = self.clean_data(
            response.css('td.va-t.ar.pl4.pr4 + td div.picSurround img::attr(data-src)').getall())

        statuses = self.clean_data(response.css('div.review-ratio__box a::text').getall())
        numbers = self.clean_data(response.css('div.review-ratio__box a strong::text').getall())

        synonyms = self.clean_data(
            response.xpath('//div[@class="spaceit_pad"][contains(., "Synonyms")]/text()').getall())
        japanese_title = self.clean_data(
            response.xpath('//div[@class="spaceit_pad"][contains(., "Japanese")]/text()').getall())
        english_title = self.clean_data(
            response.xpath('//div[@class="spaceit_pad"][contains(., "English")]/text()').getall())
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

        yield {
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
            'anime_type': anime_type,
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
            'score': score,
            'ranked': ranked,
            'popularity': popularity,
            'members': members,
            'favorites': favorites,
        }
# Proceed to the next URL
        next_index = index + 1
        if next_index < len(self.data):
            next_entry = self.data[next_index]
            yield scrapy.Request(url=next_entry['url'], callback=self.parse_anime_page, meta={'index': next_index})
