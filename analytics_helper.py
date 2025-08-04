import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import csv
from io import StringIO

class AnalyticsHelper:
    """Helper class for reading analytics, history, and export features"""
    
    def __init__(self):
        # Initialize analytics data in session state
        if 'reading_history' not in st.session_state:
            st.session_state.reading_history = []
        if 'search_history' not in st.session_state:
            st.session_state.search_history = []
        if 'reading_stats' not in st.session_state:
            st.session_state.reading_stats = {
                'total_searches': 0,
                'total_recommendations': 0,
                'favorite_genres': {},
                'reading_streak': 0,
                'last_reading_date': None
            }
    
    def add_to_reading_history(self, book_data: Dict, search_query: str):
        """Add a book to reading history with timestamp"""
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'search_query': search_query,
            'book_title': book_data.get('title', 'Unknown'),
            'book_author': book_data.get('author', 'Unknown'),
            'book_year': book_data.get('year', 'Unknown'),
            'action': 'viewed'
        }
        st.session_state.reading_history.append(history_entry)
    
    def add_to_search_history(self, query: str, num_results: int):
        """Add a search to search history"""
        search_entry = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'num_results': num_results
        }
        st.session_state.search_history.append(search_entry)
        st.session_state.reading_stats['total_searches'] += 1
    
    def update_reading_stats(self, genres: List[str]):
        """Update reading statistics"""
        for genre in genres:
            if genre in st.session_state.reading_stats['favorite_genres']:
                st.session_state.reading_stats['favorite_genres'][genre] += 1
            else:
                st.session_state.reading_stats['favorite_genres'][genre] = 1
        
        # Update reading streak
        today = datetime.now().date()
        if st.session_state.reading_stats['last_reading_date']:
            last_date = datetime.fromisoformat(st.session_state.reading_stats['last_reading_date']).date()
            if today == last_date + timedelta(days=1):
                st.session_state.reading_stats['reading_streak'] += 1
            elif today > last_date + timedelta(days=1):
                st.session_state.reading_stats['reading_streak'] = 1
        else:
            st.session_state.reading_stats['reading_streak'] = 1
        
        st.session_state.reading_stats['last_reading_date'] = today.isoformat()
        st.session_state.reading_stats['total_recommendations'] += 1
    
    def get_reading_analytics(self) -> Dict:
        """Get comprehensive reading analytics"""
        if not st.session_state.reading_history:
            return {
                'total_books_viewed': 0,
                'total_searches': 0,
                'favorite_genres': {},
                'reading_streak': 0,
                'most_viewed_books': [],
                'search_trends': []
            }
        
        # Calculate analytics
        total_books = len(st.session_state.reading_history)
        total_searches = len(st.session_state.search_history)
        
        # Most viewed books
        book_counts = {}
        for entry in st.session_state.reading_history:
            book_key = f"{entry['book_title']} by {entry['book_author']}"
            book_counts[book_key] = book_counts.get(book_key, 0) + 1
        
        most_viewed = sorted(book_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Search trends (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_searches = [
            entry for entry in st.session_state.search_history
            if datetime.fromisoformat(entry['timestamp']) > week_ago
        ]
        
        return {
            'total_books_viewed': total_books,
            'total_searches': total_searches,
            'favorite_genres': st.session_state.reading_stats['favorite_genres'],
            'reading_streak': st.session_state.reading_stats['reading_streak'],
            'most_viewed_books': most_viewed,
            'search_trends': recent_searches
        }
    
    def search_reading_history(self, query: str) -> List[Dict]:
        """Search through reading history"""
        if not query:
            return st.session_state.reading_history[-10:]  # Last 10 entries
        
        query_lower = query.lower()
        results = []
        
        for entry in st.session_state.reading_history:
            if (query_lower in entry['book_title'].lower() or 
                query_lower in entry['book_author'].lower() or
                query_lower in entry['search_query'].lower()):
                results.append(entry)
        
        return results
    
    def export_reading_history(self, format_type: str = 'csv') -> str:
        """Export reading history in various formats"""
        if not st.session_state.reading_history:
            return "No reading history to export"
        
        if format_type == 'csv':
            # Create CSV
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(['Date', 'Search Query', 'Book Title', 'Author', 'Year', 'Action'])
            
            for entry in st.session_state.reading_history:
                date = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
                writer.writerow([
                    date,
                    entry['search_query'],
                    entry['book_title'],
                    entry['book_author'],
                    entry['book_year'],
                    entry['action']
                ])
            
            return output.getvalue()
        
        elif format_type == 'json':
            return json.dumps(st.session_state.reading_history, indent=2)
        
        elif format_type == 'txt':
            output = []
            output.append("📚 Reading History Export")
            output.append("=" * 50)
            output.append("")
            
            for entry in st.session_state.reading_history:
                date = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
                output.append(f"📅 {date}")
                output.append(f"🔍 Search: {entry['search_query']}")
                output.append(f"📖 Book: {entry['book_title']} by {entry['book_author']}")
                output.append(f"📅 Year: {entry['book_year']}")
                output.append("")
            
            return "\n".join(output)
        
        return "Invalid export format"
    
    def export_reading_lists(self, lists_data: Dict, format_type: str = 'csv') -> str:
        """Export reading lists in various formats"""
        if not lists_data:
            return "No reading lists to export"
        
        if format_type == 'csv':
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(['List', 'Title', 'Author', 'Year', 'Description'])
            
            for list_name, books in lists_data.items():
                for book in books:
                    writer.writerow([
                        list_name.replace('_', ' ').title(),
                        book.get('title', 'Unknown'),
                        book.get('author', 'Unknown'),
                        book.get('year', 'Unknown'),
                        book.get('description', '')[:100] + '...' if len(book.get('description', '')) > 100 else book.get('description', '')
                    ])
            
            return output.getvalue()
        
        elif format_type == 'json':
            return json.dumps(lists_data, indent=2)
        
        elif format_type == 'txt':
            output = []
            output.append("📚 Reading Lists Export")
            output.append("=" * 50)
            output.append("")
            
            for list_name, books in lists_data.items():
                output.append(f"📖 {list_name.replace('_', ' ').title()}")
                output.append("-" * 30)
                
                for i, book in enumerate(books, 1):
                    output.append(f"{i}. {book.get('title', 'Unknown')}")
                    output.append(f"   Author: {book.get('author', 'Unknown')}")
                    if book.get('year'):
                        output.append(f"   Year: {book.get('year')}")
                    if book.get('description'):
                        output.append(f"   Description: {book.get('description')}")
                    output.append("")
            
            return "\n".join(output)
        
        return "Invalid export format"
    
    def clear_reading_history(self):
        """Clear all reading history"""
        st.session_state.reading_history = []
        st.session_state.search_history = []
        st.session_state.reading_stats = {
            'total_searches': 0,
            'total_recommendations': 0,
            'favorite_genres': {},
            'reading_streak': 0,
            'last_reading_date': None
        }
    
    def get_recent_searches(self, limit: int = 5) -> List[str]:
        """Get recent search queries"""
        recent = []
        for entry in reversed(st.session_state.search_history):
            if entry['query'] not in recent:
                recent.append(entry['query'])
            if len(recent) >= limit:
                break
        return recent 