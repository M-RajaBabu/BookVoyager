import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_groq import ChatGroq
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Validate API key
def validate_api_key():
    """Validate that the GROQ API key is available"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")
    if len(api_key) < 10:  # Basic validation
        raise ValueError("GROQ_API_KEY appears to be invalid. Please check your .env file.")
    return api_key

# Initialize Groq LLM with error handling
try:
    api_key = validate_api_key()
    llm = ChatGroq(
        temperature=0.75,
        model_name="llama3-70b-8192",
        api_key=api_key
    )
    logger.info("Groq LLM initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Groq LLM: {str(e)}")
    llm = None

def generate_book_recommendations(book_title, num_books=5, genres=None, era=None, reading_level=None, book_length=None):
    """
    Generate book recommendations with comprehensive error handling
    
    Args:
        book_title (str): The book title or topic to base recommendations on
        num_books (int): Number of recommendations to generate (3-10)
        genres (list): List of genres to filter by
        era (str): Era preference
    
    Returns:
        dict: Dictionary containing 'book_recommendations' and 'reading_journey'
    
    Raises:
        ValueError: For invalid inputs
        Exception: For API or processing errors
    """
    
    # Input validation
    if not book_title or not isinstance(book_title, str):
        raise ValueError("Book title must be a non-empty string")
    
    if not isinstance(num_books, int) or num_books < 3 or num_books > 10:
        raise ValueError("Number of books must be an integer between 3 and 10")
    
    if genres and not isinstance(genres, list):
        raise ValueError("Genres must be a list")
    
    if era and not isinstance(era, str):
        raise ValueError("Era must be a string")
    
    # Check if LLM is available
    if llm is None:
        raise Exception("AI service is not available. Please check your API configuration.")
    
    try:
        # Prepare genre filter
        genre_filter = ""
        if genres and len(genres) > 0:
            genre_filter = f" Focus on {', '.join(genres)} genres."
        
        # Prepare era filter
        era_filter = ""
        if era and era != "Any":
            era_filter = f" Prefer books from the {era} era."
        
        # Prepare reading level filter
        level_filter = ""
        if reading_level and reading_level != "Any":
            level_filter = f" Focus on {reading_level} reading level books."
        
        # Prepare book length filter
        length_filter = ""
        if book_length and book_length != "Any":
            if "Short" in book_length:
                length_filter = " Prefer shorter books (under 200 pages)."
            elif "Medium" in book_length:
                length_filter = " Prefer medium-length books (200-400 pages)."
            elif "Long" in book_length:
                length_filter = " Prefer longer books (over 400 pages)."
        
        # Chain 1: Generate book recommendations
        prompt_template_books = PromptTemplate(
            input_variables=['book_title'],
            template=f"""
            Recommend {num_books} books related to the book or topic "{{book_title}}".
            If "{{book_title}}" is not a book, treat it as a topic and suggest books that are relevant, informative, or interesting for someone interested in that topic.
            If you cannot find direct matches, suggest the closest possible books or general reading material.
            {genre_filter}
            {era_filter}
            {level_filter}
            {length_filter}
            For each book, provide:
            - Title
            - Author
            - Publication Year
            - 1-sentence description
            - Reason it's recommended for fans of or those interested in "{{book_title}}"
            
            Format EXACTLY as follows (use this exact format for each book):
            1. **Title**: [Book Title]  
               **Author**: [Author Name]  
               **Year**: [Publication Year]  
               **Description**: [One sentence description of the book]  
               **Why Recommended**: [Why this book is recommended for fans of {{book_title}}]
            2. **Title**: [Book Title]  
               **Author**: [Author Name]  
               **Year**: [Publication Year]  
               **Description**: [One sentence description of the book]  
               **Why Recommended**: [Why this book is recommended for fans of {{book_title}}]
            3. **Title**: [Book Title]  
               **Author**: [Author Name]  
               **Year**: [Publication Year]  
               **Description**: [One sentence description of the book]  
               **Why Recommended**: [Why this book is recommended for fans of {{book_title}}]
            [Continue for all {num_books} books...]
            """
        )
        
        books_chain = LLMChain(
            llm=llm,
            prompt=prompt_template_books,
            output_key="book_recommendations"
        )

        # Chain 2: Generate personalized reading journey
        prompt_template_list = PromptTemplate(
            input_variables=['book_recommendations'],
            template="""
            Create a personalized reading journey based on these recommendations:
            {book_recommendations}
            
            Format as:
            ## 🌟 Your Reading Journey
            
            **Start with**: [First Book] - [Brief reason why to start here]  
            **Continue with**: [Second Book] - [Brief reason for progression]  
            **Explore**: [Third Book] - [Brief reason for thematic exploration]  
            **Dive into**: [Fourth Book] - [Brief reason for deeper dive]  
            **Finish with**: [Fifth Book] - [Brief reason for climactic finish]  
            
            **Overall Journey Theme**: [1-sentence theme connecting all books]
            """
        )
        
        list_chain = LLMChain(
            llm=llm,
            prompt=prompt_template_list,
            output_key="reading_journey"
        )

        # Combine chains
        chain = SequentialChain(
            chains=[books_chain, list_chain],
            input_variables=['book_title'],
            output_variables=['book_recommendations', 'reading_journey']
        )
        
        # Execute the chain
        logger.info(f"Generating recommendations for: {book_title}")
        result = chain({'book_title': book_title})
        
        # Validate the response
        if not result:
            raise Exception("No response received from AI service")
        
        if 'book_recommendations' not in result or not result['book_recommendations']:
            raise Exception("No book recommendations generated")
        
        if 'reading_journey' not in result or not result['reading_journey']:
            raise Exception("No reading journey generated")
        
        logger.info("Recommendations generated successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        
        # Check for specific API errors
        error_str = str(e).lower()
        if "503" in error_str or "service unavailable" in error_str:
            raise Exception("The AI service is temporarily unavailable. Please try again in a few minutes. If the problem persists, check https://groqstatus.com/ for service status.")
        elif "401" in error_str or "unauthorized" in error_str:
            raise Exception("API key authentication failed. Please check your API configuration.")
        elif "429" in error_str or "rate limit" in error_str:
            raise Exception("Rate limit exceeded. Please wait a moment and try again.")
        elif "timeout" in error_str:
            raise Exception("Request timed out. Please try again.")
        else:
            raise Exception(f"Failed to generate recommendations: {str(e)}")

def test_api_connection():
    """Test the API connection and return status"""
    try:
        validate_api_key()
        if llm is None:
            return False, "LLM not initialized"
        
        # Try a simple test query
        test_response = llm.invoke("Say 'Hello'")
        if test_response and hasattr(test_response, 'content'):
            return True, "API connection successful"
        else:
            return False, "Invalid response from API"
    except Exception as e:
        return False, f"API connection failed: {str(e)}"