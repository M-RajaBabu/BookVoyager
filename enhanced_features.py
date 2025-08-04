import requests
import json
import re
from typing import Dict, List, Optional, Tuple
import streamlit as st

class EnhancedFeatures:
    """Enhanced features for BookVoyager including book covers, reading time, and reading lists"""
    
    def __init__(self):
        self.reading_speeds = {
            'slow': 150,      # words per minute
            'normal': 250,    # words per minute  
            'fast': 350       # words per minute
        }
        
        # Initialize reading lists in session state
        if 'reading_lists' not in st.session_state:
            st.session_state.reading_lists = {
                'to_read': [],
                'currently_reading': [],
                'completed': []
            }
    
    def get_book_cover(self, title: str, author: str = "") -> Optional[str]:
        """Get book cover image URL from Google Books API with improved error handling"""
        try:
            # Clean up the title and author
            title = title.strip() if title else ""
            author = author.strip() if author else ""
            
            if not title:
                return None
            
            # Search query - try different combinations
            search_queries = [
                f"{title} {author}".strip(),
                title,
                f"{title} book"
            ]
            
            for query in search_queries:
                if not query:
                    continue
                    
                url = "https://www.googleapis.com/books/v1/volumes"
                params = {
                    'q': query,
                    'maxResults': 1,
                    'fields': 'items(volumeInfo(imageLinks,title,authors))'
                }
                
                response = requests.get(url, params=params, timeout=10)  # Increased timeout
                response.raise_for_status()
                
                data = response.json()
                if 'items' in data and len(data['items']) > 0:
                    volume_info = data['items'][0]['volumeInfo']
                    if 'imageLinks' in volume_info and 'thumbnail' in volume_info['imageLinks']:
                        return volume_info['imageLinks']['thumbnail']
            
            return None
            
        except requests.exceptions.Timeout:
            print(f"Timeout fetching book cover for: {title}")
            return None
        except Exception as e:
            print(f"Error fetching book cover for '{title}': {e}")
            return None
    
    def estimate_reading_time(self, book_info: Dict, reading_speed: str = 'normal') -> Tuple[int, str]:
        """Estimate reading time based on book information"""
        try:
            # Try to extract page count from book info
            page_count = None
            
            # Look for page count in various formats
            if 'pages' in book_info:
                page_count = book_info['pages']
            elif 'page_count' in book_info:
                page_count = book_info['page_count']
            
            # If no page count, estimate based on description length
            if not page_count:
                description = book_info.get('description', '')
                # Rough estimate: 1 page ≈ 250 words
                estimated_pages = max(200, len(description.split()) // 250)
                page_count = estimated_pages
            
            # Calculate reading time
            words_per_page = 250  # Average words per page
            total_words = page_count * words_per_page
            wpm = self.reading_speeds.get(reading_speed, 250)
            minutes = total_words / wpm
            
            # Convert to hours and minutes
            hours = int(minutes // 60)
            remaining_minutes = int(minutes % 60)
            
            if hours > 0:
                time_str = f"{hours}h {remaining_minutes}m"
            else:
                time_str = f"{remaining_minutes}m"
            
            return int(minutes), time_str
            
        except Exception as e:
            print(f"Error estimating reading time: {e}")
            return 0, "Unknown"
    
    def extract_book_details(self, markdown_text: str) -> List[Dict]:
        """Extract detailed book information from markdown text with improved parsing"""
        books = []
        lines = markdown_text.split('\n')
        current_book = {}
        
        # Debug: Print the first few lines to see the format
        print("DEBUG: First 10 lines of markdown:")
        for i, line in enumerate(lines[:10]):
            print(f"Line {i}: {line}")
        
        for line in lines:
            line = line.strip()
            
            # Check for numbered list items (1., 2., etc.)
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
                if current_book and len(current_book) > 1:  # Only add if we have some data
                    books.append(current_book)
                current_book = {'number': line.split('.')[0]}
            
            # Check for title in various formats
            elif line.startswith('**Title**:') or line.startswith('**Title:**'):
                current_book['title'] = line.replace('**Title**:', '').replace('**Title:**', '').strip()
            elif 'Title' in line and ':' in line:
                # Handle cases like "Title: [Book Name]"
                title_part = line.split(':', 1)
                if len(title_part) > 1:
                    current_book['title'] = title_part[1].strip()
            
            # Check for author in various formats
            elif line.startswith('**Author**:') or line.startswith('**Author:**'):
                current_book['author'] = line.replace('**Author**:', '').replace('**Author:**', '').strip()
            elif 'Author' in line and ':' in line:
                author_part = line.split(':', 1)
                if len(author_part) > 1:
                    current_book['author'] = author_part[1].strip()
            
            # Check for year in various formats
            elif line.startswith('**Year**:') or line.startswith('**Year:**'):
                current_book['year'] = line.replace('**Year**:', '').replace('**Year:**', '').strip()
            elif 'Year' in line and ':' in line:
                year_part = line.split(':', 1)
                if len(year_part) > 1:
                    current_book['year'] = year_part[1].strip()
            
            # Check for description in various formats
            elif line.startswith('**Description**:') or line.startswith('**Description:**'):
                current_book['description'] = line.replace('**Description**:', '').replace('**Description:**', '').strip()
            elif 'Description' in line and ':' in line:
                desc_part = line.split(':', 1)
                if len(desc_part) > 1:
                    current_book['description'] = desc_part[1].strip()
            
            # Check for why recommended in various formats
            elif line.startswith('**Why Recommended**:') or line.startswith('**Why Recommended:**'):
                current_book['reason'] = line.replace('**Why Recommended**:', '').replace('**Why Recommended:**', '').strip()
            elif 'Why Recommended' in line and ':' in line:
                reason_part = line.split(':', 1)
                if len(reason_part) > 1:
                    current_book['reason'] = reason_part[1].strip()
            
            # Handle multi-line descriptions
            elif current_book and line and not line.startswith('**') and not line.startswith('*'):
                if 'description' in current_book:
                    current_book['description'] += ' ' + line
                elif 'reason' in current_book:
                    current_book['reason'] += ' ' + line
        
        # Add the last book if it has data
        if current_book and len(current_book) > 1:
            books.append(current_book)
        
        # Debug: Print extracted books
        print(f"DEBUG: Extracted {len(books)} books:")
        for i, book in enumerate(books):
            print(f"Book {i+1}: {book}")
        
        return books
    
    def add_to_reading_list(self, book: Dict, list_name: str) -> bool:
        """Add a book to a reading list"""
        try:
            if list_name not in st.session_state.reading_lists:
                st.session_state.reading_lists[list_name] = []
            
            # Check if book already exists in the list
            for existing_book in st.session_state.reading_lists[list_name]:
                if (existing_book.get('title') == book.get('title') and 
                    existing_book.get('author') == book.get('author')):
                    return False  # Book already exists
            
            # Add book to list
            st.session_state.reading_lists[list_name].append(book)
            return True
            
        except Exception as e:
            print(f"Error adding to reading list: {e}")
            return False
    
    def remove_from_reading_list(self, book: Dict, list_name: str) -> bool:
        """Remove a book from a reading list"""
        try:
            if list_name not in st.session_state.reading_lists:
                return False
            
            # Find and remove the book
            for i, existing_book in enumerate(st.session_state.reading_lists[list_name]):
                if (existing_book.get('title') == book.get('title') and 
                    existing_book.get('author') == book.get('author')):
                    st.session_state.reading_lists[list_name].pop(i)
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error removing from reading list: {e}")
            return False
    
    def get_reading_list(self, list_name: str) -> List[Dict]:
        """Get books from a specific reading list"""
        return st.session_state.reading_lists.get(list_name, [])
    
    def get_all_reading_lists(self) -> Dict[str, List[Dict]]:
        """Get all reading lists"""
        return st.session_state.reading_lists
    
    def clear_reading_list(self, list_name: str) -> bool:
        """Clear all books from a reading list"""
        try:
            if list_name in st.session_state.reading_lists:
                st.session_state.reading_lists[list_name] = []
                return True
            return False
        except Exception as e:
            print(f"Error clearing reading list: {e}")
            return False
    
    def export_reading_list(self, list_name: str) -> str:
        """Export reading list as formatted text"""
        books = self.get_reading_list(list_name)
        if not books:
            return f"No books in {list_name} list"
        
        export_text = f"📚 {list_name.replace('_', ' ').title()} List\n\n"
        for i, book in enumerate(books, 1):
            export_text += f"{i}. **{book.get('title', 'Unknown Title')}**\n"
            export_text += f"   Author: {book.get('author', 'Unknown Author')}\n"
            if book.get('year'):
                export_text += f"   Year: {book.get('year')}\n"
            if book.get('description'):
                export_text += f"   Description: {book.get('description')}\n"
            export_text += "\n"
        
        return export_text 