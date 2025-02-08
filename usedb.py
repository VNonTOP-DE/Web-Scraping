Code to query data from anime.db
----------------------------------------------------------------------
import sqlite3
import pandas as pd
import os

# Connect to the database
conn = sqlite3.connect('animelist.db')

# Method 1: Direct SQL Queries
def get_top_rated_anime(min_score=8.0):
    """Retrieve top-rated anime above a certain score"""
    query = """
    SELECT DISTINCT title, score, type, episodes 
    FROM anime 
    WHERE score >= ? AND title IS NOT NULL
    ORDER BY score DESC 
    LIMIT 10
    """
    return pd.read_sql_query(query, conn, params=(min_score,))

# Method 2: Exploring Data with Pandas
def explore_anime_genres():
    """Get genre distribution"""
    query = """
    SELECT DISTINCT g.genre_name, COUNT(DISTINCT ag.anime_id) as anime_count
    FROM genres g
    JOIN anime_genres ag ON g.genre_id = ag.genre_id
    GROUP BY g.genre_name
    ORDER BY anime_count DESC
    """
    return pd.read_sql_query(query, conn)

# Method 3: Complex Joining
def get_anime_characters(anime_title):
    """Find characters for a specific anime"""
    query = """
    SELECT a.title, c.name, c.character_type, va.name as voice_actor
    FROM anime a
    JOIN characters c ON a.anime_id = c.anime_id
    JOIN anime_character_voice acv ON c.character_id = acv.character_id
    JOIN voice_actors va ON acv.voice_actor_id = va.voice_actor_id
    WHERE a.title = ?
    """
    return pd.read_sql_query(query, conn, params=(anime_title,))

def check_database_content():
    """Check if the database has any data"""
    try:
        # Connect to the database
        conn = sqlite3.connect('animelist.db')
        cursor = conn.cursor()
        
        # Check counts in main tables
        cursor.execute("SELECT COUNT(*) FROM anime")
        anime_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM genres")
        genre_count = cursor.fetchone()[0]
        
        print("\nDatabase Status:")
        print(f"Number of anime entries: {anime_count}")
        print(f"Number of genre entries: {genre_count}")
        
        if anime_count == 0:
            print("\nWarning: The database appears to be empty!")
            print("Please run animetodb.py first to populate the database.")
            
        return anime_count > 0
            
    except sqlite3.OperationalError as e:
        print(f"\nError: {str(e)}")
        print("The database might not be properly initialized.")
        return False
    finally:
        conn.close()

def explore_character_voices(limit=10):
    """
    Explore anime characters and their voice actors with anime titles
    Returns a sample of character-voice actor relationships
    """
    query = """
    SELECT 
        a.title as anime_title,
        c.name as character_name,
        c.character_type,
        va.name as voice_actor,
        va.language
    FROM anime a
    JOIN anime_character_voice acv ON a.anime_id = acv.anime_id
    JOIN characters c ON acv.character_id = c.character_id
    JOIN voice_actors va ON acv.voice_actor_id = va.voice_actor_id
    ORDER BY a.title
    LIMIT ?
    """
    return pd.read_sql_query(query, conn, params=(limit,))

def analyze_character_counts():
    """
    Analyze how many characters each anime has
    """
    query = """
    SELECT 
        a.title,
        COUNT(DISTINCT c.character_id) as character_count,
        COUNT(DISTINCT va.voice_actor_id) as voice_actor_count
    FROM anime a
    JOIN anime_character_voice acv ON a.anime_id = acv.anime_id
    JOIN characters c ON acv.character_id = c.character_id
    JOIN voice_actors va ON acv.voice_actor_id = va.voice_actor_id
    GROUP BY a.title
    ORDER BY character_count DESC
    LIMIT 10
    """
    return pd.read_sql_query(query, conn)

def get_anime_reviews():
    """
    Get review statistics for each anime
    Shows anime title, review status (Recommended/Mixed/Not Recommended), and number of reviews
    """
    query = """
    SELECT 
        a.title as anime_title,
        r.status as review_status,
        r.number_of_reviews,
        a.score
    FROM anime a
    JOIN reviews r ON a.anime_id = r.anime_id
    ORDER BY a.score DESC, r.number_of_reviews DESC
    """
    return pd.read_sql_query(query, conn)

def get_anime_review_summary():
    """
    Get a summary of reviews for each anime
    Shows total reviews and breakdown of recommendations
    """
    query = """
    SELECT 
        a.title as anime_title,
        a.score,
        SUM(CASE WHEN r.status = 'Recommended' THEN r.number_of_reviews ELSE 0 END) as recommended,
        SUM(CASE WHEN r.status = 'Mixed Feelings' THEN r.number_of_reviews ELSE 0 END) as mixed,
        SUM(CASE WHEN r.status = 'Not Recommended' THEN r.number_of_reviews ELSE 0 END) as not_recommended,
        SUM(r.number_of_reviews) as total_reviews
    FROM anime a
    JOIN reviews r ON a.anime_id = r.anime_id
    GROUP BY a.title, a.score
    ORDER BY total_reviews DESC
    LIMIT 20
    """
    return pd.read_sql_query(query, conn)

def main():
    # First check if database has content
    if not check_database_content():
        return
        
    # Connect to the database
    conn = sqlite3.connect('animelist.db')

    try:
        # Create directory if it doesn't exist
        if not os.path.exists('anime_query'):
            os.makedirs('anime_query')

        print("\nSaving query results to anime_query directory...")

        # Top Rated Anime
        print("Saving top rated anime...")
        top_anime = get_top_rated_anime()
        top_anime.to_csv('anime_query/top_rated_anime.csv', index=False)

        # Genre Distribution
        print("Saving genre distribution...")
        genres = explore_anime_genres()
        genres.to_csv('anime_query/genre_distribution.csv', index=False)
        
        # Character Voice Actors
        print("Saving character voice actors sample...")
        character_voices = explore_character_voices(20)
        character_voices.to_csv('anime_query/character_voices_sample.csv', index=False)
        
        # Anime Character Counts
        print("Saving character counts...")
        char_counts = analyze_character_counts()
        char_counts.to_csv('anime_query/character_counts.csv', index=False)
        
        # Anime Reviews Statistics
        print("Saving review statistics...")
        reviews = get_anime_reviews()
        reviews.to_csv('anime_query/review_statistics.csv', index=False)
        
        # Total Reviews by Status
        print("Saving review status totals...")
        total_by_status = reviews.groupby('review_status')['number_of_reviews'].sum().reset_index()
        total_by_status.to_csv('anime_query/review_status_totals.csv', index=False)
        
        # Top 20 Anime by Review Count
        print("Saving top reviewed anime...")
        review_summary = get_anime_review_summary()
        review_summary.to_csv('anime_query/top_reviewed_anime.csv', index=False)
        
        print("\nAll query results have been saved to the anime_query directory!")
        
        # Still print to console for immediate viewing
        print("\nQuery Results Preview:")
        print("\nTop Rated Anime:")
        print(top_anime)
        print("\nGenre Distribution:")
        print(genres)
        print("\nSample of Character Voice Actors:")
        print(character_voices)
        print("\nAnime Character Counts:")
        print(char_counts)
        print("\nAnime Reviews Statistics:")
        print(reviews)
        print("\nTotal Reviews by Status:")
        print(total_by_status)
        print("\nTop 20 Anime by Review Count:")
        print(review_summary)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
