import streamlit as st
import langchain_helper
import enhanced_features
import analytics_helper
import base64
import requests
import urllib.parse
import re

# Set page config
st.set_page_config(
    page_title="BookVoyager - Discover Your Next Read",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state with proper defaults
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'reading_journey' not in st.session_state:
    st.session_state.reading_journey = None
if 'error_message' not in st.session_state:
    st.session_state.error_message = None
if 'reading_speed' not in st.session_state:
    st.session_state.reading_speed = 'normal'
if 'show_book_covers' not in st.session_state:
    st.session_state.show_book_covers = True
if 'enhanced_features' not in st.session_state:
    st.session_state.enhanced_features = enhanced_features.EnhancedFeatures()
if 'analytics_helper' not in st.session_state:
    st.session_state.analytics_helper = analytics_helper.AnalyticsHelper()

# Theme toggle in sidebar
theme = st.sidebar.radio('Theme', options=['dark', 'light'], index=0 if st.session_state['theme']=='dark' else 1)
st.session_state['theme'] = theme

# Custom CSS for styling
def local_css(theme='dark'):
    if theme == 'dark':
        sidebar_bg = '#000'
        sidebar_text = '#fff'
        input_bg = '#1a1a1a'
        input_text = '#fff'
        dropdown_bg = '#222'
        dropdown_text = '#fff'
        main_text = '#fff'
        overlay = 'rgba(30,30,30,0.85)'
    else:
        sidebar_bg = '#fff'
        sidebar_text = '#222'
        input_bg = '#fff'
        input_text = '#000'
        dropdown_bg = '#fff'
        dropdown_text = '#000'
        main_text = '#000'
        overlay = 'rgba(240,248,255,0.9)'
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: rgba(255, 255, 255, 0.95);
        background-image: linear-gradient({overlay}, {overlay}), url('https://images.unsplash.com/photo-1507842217343-583bb7270b66?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {sidebar_text if theme == 'dark' else '#ddd'};
    }}
    /* Ensure sidebar has proper contrast in light mode */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        color: {sidebar_text} !important;
    }}
    /* Sidebar text elements */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div {{
        color: {sidebar_text} !important;
    }}
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: {sidebar_text} !important;
        font-weight: bold;
    }}
    /* Sidebar input elements */
    [data-testid="stSidebar"] .stTextInput>div>div>input,
    [data-testid="stSidebar"] .stSelectbox>div>div>select,
    [data-testid="stSidebar"] .stSlider>div>div>div>div,
    [data-testid="stSidebar"] .stMultiSelect>div>div>div>input {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 1px solid {sidebar_text if theme == 'dark' else '#ccc'} !important;
    }}
    /* Specific styling for dropdown input fields */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="combobox"] {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div[role="combobox"] {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    /* Dropdown input field text */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="combobox"] span {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div[role="combobox"] span {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    /* Dropdown placeholder text */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="combobox"] div {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div[role="combobox"] div {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    /* Dropdown menu and options - more specific targeting */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] div[data-baseweb="select"] [role="option"],
    [data-testid="stSidebar"] div[data-baseweb="select"] [role="listbox"],
    [data-testid="stSidebar"] div[data-baseweb="select"] input,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[role="combobox"] {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Dropdown popup/overlay styling */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[role="listbox"] {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
        border: 1px solid {sidebar_text if theme == 'dark' else '#ccc'} !important;
    }}
    /* Individual dropdown options */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[role="option"] {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Dropdown option hover */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[role="option"]:hover {{
        background-color: {sidebar_bg if theme == 'dark' else '#e3f2fd'} !important;
        color: {dropdown_text} !important;
    }}
    /* Multi-select dropdown options */
    [data-testid="stSidebar"] .stMultiSelect [role="option"],
    [data-testid="stSidebar"] .stMultiSelect [role="listbox"] {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Additional dropdown styling for better visibility */
    [data-testid="stSidebar"] .stSelectbox [role="option"],
    [data-testid="stSidebar"] .stSelectbox [role="listbox"] {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Dropdown option hover states */
    [data-testid="stSidebar"] .stSelectbox [role="option"]:hover,
    [data-testid="stSidebar"] .stMultiSelect [role="option"]:hover {{
        background-color: {sidebar_bg if theme == 'dark' else '#e3f2fd'} !important;
        color: {dropdown_text} !important;
    }}
    /* Dropdown listbox background */
    [data-testid="stSidebar"] .stSelectbox [role="listbox"],
    [data-testid="stSidebar"] .stMultiSelect [role="listbox"] {{
        background-color: {dropdown_bg} !important;
        border: 1px solid {sidebar_text if theme == 'dark' else '#ccc'} !important;
    }}
    /* Ensure dropdown text is visible */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {{
        color: {dropdown_text} !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] span {{
        color: {dropdown_text} !important;
    }}
    /* Selected values in dropdowns */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="combobox"] {{
        color: {dropdown_text} !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div[role="combobox"] {{
        color: {dropdown_text} !important;
    }}
    /* Selected dropdown values - more specific targeting */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="combobox"] span {{
        color: {dropdown_text} !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div[role="combobox"] span {{
        color: {dropdown_text} !important;
    }}
    /* Multi-select selected items */
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div[role="combobox"] div {{
        color: {dropdown_text} !important;
        background-color: {dropdown_bg} !important;
    }}
    /* Multi-select chips/tags */
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div[role="combobox"] div[data-testid="selected"] {{
        color: {dropdown_text} !important;
        background-color: {dropdown_bg} !important;
        border: 1px solid {sidebar_text if theme == 'dark' else '#ccc'} !important;
    }}
    /* Multi-select chip text */
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div[role="combobox"] div[data-testid="selected"] span {{
        color: {dropdown_text} !important;
    }}
    /* All dropdown text elements */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] *,
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] * {{
        color: {dropdown_text} !important;
    }}
    /* Universal dropdown styling - catch all */
    [data-testid="stSidebar"] div[data-baseweb="select"] * {{
        color: {dropdown_text} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] div {{
        background-color: {dropdown_bg} !important;
    }}
    /* Dropdown overlay/popup container */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Dropdown option text specifically */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[role="option"] span {{
        color: {dropdown_text} !important;
    }}
    /* Dropdown overlay styling */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] div {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Dropdown option list container */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] div[role="listbox"] {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Force all text in dropdown to be visible */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] * {{
        color: {dropdown_text} !important;
    }}
    /* Specific styling for dropdown list items (li elements) */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul li {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul li div {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Dropdown option hover for list items */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul li:hover {{
        background-color: {sidebar_bg if theme == 'dark' else '#e3f2fd'} !important;
        color: {dropdown_text} !important;
    }}
    /* Make dropdown background transparent/white in light mode */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] {{
        background-color: {dropdown_bg} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] div {{
        background-color: {dropdown_bg} !important;
    }}
    /* Additional styling for dropdown containers */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul {{
        background-color: {dropdown_bg} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul div {{
        background-color: {dropdown_bg} !important;
    }}
    /* Ensure all dropdown elements have proper background */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] * {{
        background-color: {dropdown_bg} !important;
    }}
    /* Force white background for all dropdown elements in light mode */
    [data-testid="stSidebar"] div[data-baseweb="select"] * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Force white background for popover and all its children */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] {{
        background-color: {dropdown_bg} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Force white background for all list elements */
    [data-testid="stSidebar"] div[data-baseweb="select"] ul {{
        background-color: {dropdown_bg} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] ul * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Force white background for all div elements in dropdown */
    [data-testid="stSidebar"] div[data-baseweb="select"] div {{
        background-color: {dropdown_bg} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] div * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Override any Streamlit default styling */
    [data-testid="stSidebar"] div[data-baseweb="select"] [style*="background"] {{
        background-color: {dropdown_bg} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] [style*="color"] {{
        color: {dropdown_text} !important;
    }}
    /* Force all elements to have proper styling */
    [data-testid="stSidebar"] div[data-baseweb="select"] span,
    [data-testid="stSidebar"] div[data-baseweb="select"] p,
    [data-testid="stSidebar"] div[data-baseweb="select"] li,
    [data-testid="stSidebar"] div[data-baseweb="select"] div {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* More aggressive styling for dropdown elements */
    [data-testid="stSidebar"] div[data-baseweb="select"] [role="option"] {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] [role="listbox"] {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Target the specific dropdown container */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] {{
        background-color: {dropdown_bg} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] div {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Force all children of popover to have white background */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Ultra aggressive styling to override any black backgrounds */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul {{
        background-color: {dropdown_bg} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul li {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul li div {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul li span {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Override any inline styles */
    [data-testid="stSidebar"] div[data-baseweb="select"] [style] {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Target Streamlit's specific dropdown structure */
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div[data-testid="popover"] {{
        background-color: {dropdown_bg} !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div[data-testid="popover"] * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[data-testid="popover"] {{
        background-color: {dropdown_bg} !important;
    }}
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[data-testid="popover"] * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Force all dropdown elements to have white background */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul li,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul li div,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="popover"] ul li span {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Target the specific ul element you mentioned */
    [data-testid="stSidebar"] div[data-baseweb="select"] ul {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] ul * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Target any ul element in the sidebar */
    [data-testid="stSidebar"] ul {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    [data-testid="stSidebar"] ul * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Ultra aggressive styling for all ul elements */
    ul {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    ul * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Target any element with role="listbox" */
    [role="listbox"] {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    [role="listbox"] * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Target the specific DOM structure you mentioned */
    div[data-baseweb="select"] ul {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    div[data-baseweb="select"] ul * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Force all dropdown containers to have white background */
    div[data-baseweb="select"] {{
        background-color: {dropdown_bg} !important;
    }}
    div[data-baseweb="select"] * {{
        background-color: {dropdown_bg} !important;
        color: {dropdown_text} !important;
    }}
    /* Header/Navigation bar styling */
    header {{
        background-color: {sidebar_bg} !important;
        color: {sidebar_text} !important;
    }}
    header * {{
        color: {sidebar_text} !important;
    }}
    /* Streamlit header elements */
    [data-testid="stHeader"] {{
        background-color: {sidebar_bg} !important;
        color: {sidebar_text} !important;
    }}
    [data-testid="stHeader"] * {{
        color: {sidebar_text} !important;
    }}
    /* Navigation bar text */
    nav {{
        background-color: {sidebar_bg} !important;
        color: {sidebar_text} !important;
    }}
    nav * {{
        color: {sidebar_text} !important;
    }}
    /* Any header-related elements */
    div[data-testid="stHeader"],
    div[data-testid="stHeader"] div,
    div[data-testid="stHeader"] span,
    div[data-testid="stHeader"] p {{
        background-color: {sidebar_bg} !important;
        color: {sidebar_text} !important;
    }}
    /* Additional header styling for better coverage */
    div[data-testid="stHeader"] h1,
    div[data-testid="stHeader"] h2,
    div[data-testid="stHeader"] h3,
    div[data-testid="stHeader"] h4,
    div[data-testid="stHeader"] h5,
    div[data-testid="stHeader"] h6 {{
        color: {sidebar_text} !important;
    }}
    /* Force all text in header to be visible */
    div[data-testid="stHeader"] * {{
        color: {sidebar_text} !important;
    }}
    /* Override any inline styles in header */
    div[data-testid="stHeader"] [style] {{
        color: {sidebar_text} !important;
    }}
    /* Dropdown background for selected values */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="combobox"] {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div[role="combobox"] {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    /* Force all dropdown input elements to have proper background */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] * {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    /* Ensure dropdown input fields are visible */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="combobox"] {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 1px solid {sidebar_text if theme == 'dark' else '#ccc'} !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div[role="combobox"] {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 1px solid {sidebar_text if theme == 'dark' else '#ccc'} !important;
    }}
    /* Override any inline styles for dropdown inputs */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] [style],
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] [style] {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    /* Dropdown placeholder text */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] input::placeholder {{
        color: {dropdown_text} !important;
        opacity: 0.7;
    }}
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] input::placeholder {{
        color: {dropdown_text} !important;
        opacity: 0.7;
    }}
    /* Radio button labels */
    [data-testid="stSidebar"] .stRadio > label {{
        color: {sidebar_text} !important;
    }}
    /* Slider labels */
    [data-testid="stSidebar"] .stSlider > label {{
        color: {sidebar_text} !important;
    }}
    /* Main text color */
    body, p, li, div, .stApp, .stMarkdown, .stTextInput, .stSelectbox, .stMultiSelect {{
        color: {main_text} !important;
    }}
    /* Ensure all text elements are visible */
    .stMarkdown p, .stMarkdown div, .stMarkdown span {{
        color: {main_text} !important;
    }}
    /* Specific styling for recommendation cards */
    div[data-testid="stMarkdown"] {{
        color: {main_text} !important;
    }}
    div[data-testid="stMarkdown"] p {{
        color: {main_text} !important;
    }}
    div[data-testid="stMarkdown"] strong {{
        color: {main_text} !important;
    }}
    div[data-testid="stMarkdown"] em {{
        color: {main_text} !important;
    }}
    /* Headers */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
        color: {main_text} !important;
        font-family: 'Georgia', serif;
    }}
    /* Buttons */
    .stButton>button {{
        background-color: #3498db !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        border: none !important;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: #2980b9 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    /* WhatsApp Button */
    .whatsapp-btn {{
        background-color: #25D366 !important;
        color: white !important;
    }}
    .whatsapp-btn:hover {{
        background-color: #128C7E !important;
    }}
    /* Cards for recommendations */
    div[data-testid="stMarkdown"] h3 {{
        border-bottom: 2px solid #3498db;
        padding-bottom: 8px;
        color: {main_text} !important;
    }}
    /* Recommendation text styling */
    div[data-testid="stMarkdown"] ul, div[data-testid="stMarkdown"] ol {{
        color: {main_text} !important;
    }}
    div[data-testid="stMarkdown"] li {{
        color: {main_text} !important;
    }}
    /* Ensure all recommendation text is visible */
    div[data-testid="stMarkdown"] * {{
        color: {main_text} !important;
    }}
    /* Markdown text */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
        color: {main_text} !important;
    }}
    /* Hero section */
    .hero-text {{
        padding: 20px;
        background: {sidebar_bg if theme == 'dark' else 'rgba(236, 240, 241, 0.7)'};
        border-radius: 15px;
        margin-top: 20px;
        color: {main_text} !important;
        border: 1px solid {sidebar_text if theme == 'dark' else '#ddd'};
    }}
    .hero-text h3 {{
        color: {main_text} !important;
        font-size: 28px !important;
    }}
    .hero-text p {{
        color: {main_text} !important;
    }}
    /* Testimonials */
    .testimonial {{
        background: {sidebar_bg if theme == 'dark' else '#f8f9fa'};
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #3498db;
        font-style: italic;
        margin-bottom: 20px;
        color: {main_text} !important;
        border: 1px solid {sidebar_text if theme == 'dark' else '#ddd'};
    }}
    .testimonial p {{
        color: {main_text} !important;
    }}
    .author {{
        text-align: right;
        font-weight: bold;
        color: {main_text} !important;
        margin-top: 10px;
        font-style: normal;
    }}
    /* Spinner */
    .stSpinner>div {{
        border-color: #3498db transparent transparent transparent !important;
    }}
    /* Share container */
    .share-container {{
        background-color: {sidebar_bg if theme == 'dark' else '#f0f8ff'};
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #3498db;
        margin-top: 20px;
        color: {main_text} !important;
    }}
    .share-container p {{
        color: {main_text} !important;
    }}
    /* Error message styling */
    .error-message {{
        background-color: {sidebar_bg if theme == 'dark' else '#ffebee'};
        color: {main_text if theme == 'dark' else '#c62828'};
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #f44336;
        margin: 10px 0;
        border: 1px solid {sidebar_text if theme == 'dark' else '#ddd'};
    }}
    /* Success message styling */
    .stSuccess {{
        background-color: {sidebar_bg if theme == 'dark' else '#d4edda'};
        color: {main_text if theme == 'dark' else '#155724'};
        border: 1px solid {sidebar_text if theme == 'dark' else '#c3e6cb'};
    }}
    </style>
    """, unsafe_allow_html=True)

# Apply styling
local_css(st.session_state['theme'])

# Main content
st.title("📚 BookVoyager")
st.subheader("Discover Your Next Literary Adventure")

# Function to validate input
def validate_book_title(book_title):
    """Validate book title input"""
    if not book_title or not book_title.strip():
        return False, "Please enter a book title or topic."
    
    # Remove extra whitespace
    book_title = book_title.strip()
    
    # Check for minimum length
    if len(book_title) < 2:
        return False, "Book title must be at least 2 characters long."
    
    # Check for reasonable maximum length
    if len(book_title) > 200:
        return False, "Book title is too long. Please enter a shorter title."
    
    return True, book_title

# Function to extract book information from markdown
def extract_book_info_from_markdown(markdown_text):
    """Extract book information from markdown formatted text"""
    books = []
    lines = markdown_text.split('\n')
    current_book = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
            if current_book:
                books.append(current_book)
            current_book = {'number': line.split('.')[0]}
        elif line.startswith('**Title**:'):
            current_book['title'] = line.replace('**Title**:', '').strip()
        elif line.startswith('**Author**:'):
            current_book['author'] = line.replace('**Author**:', '').strip()
        elif line.startswith('**Year**:'):
            current_book['year'] = line.replace('**Year**:', '').strip()
        elif line.startswith('**Description**:'):
            current_book['description'] = line.replace('**Description**:', '').strip()
        elif line.startswith('**Why Recommended**:'):
            current_book['reason'] = line.replace('**Why Recommended**:', '').strip()
    
    if current_book:
        books.append(current_book)
    
    return books

# Sidebar with inputs (now dark theme)
with st.sidebar:
    st.markdown("<h1>🔍 Find Your Next Read</h1>", unsafe_allow_html=True)
    
    # Enhanced search with recent searches
    recent_searches = st.session_state.analytics_helper.get_recent_searches()
    
    # Search input with suggestions
    book_title = st.text_input(
        "Enter a book you love:",
        placeholder="Harry Potter, The Alchemist...",
        key="book_input"
    )
    
    # Show recent searches if available
    if recent_searches:
        st.markdown("**🔍 Recent Searches:**")
        for search in recent_searches:
            if st.button(f"📖 {search}", key=f"recent_{search}", use_container_width=True):
                st.session_state.book_input = search
                st.rerun()
    
    # Number of recommendations
    num_books = st.slider(
        "Number of recommendations:",
        min_value=3,
        max_value=10,
        value=5
    )
    
    # Genre selection
    genres = st.multiselect(
        "Filter by genres:",
        ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Historical", 
         "Thriller", "Biography", "Self-Help", "Classic", "Contemporary"],
        default=[]  # No default selections
    )
    
    # Era selection
    era = st.selectbox(
        "Preferred era:",
        ["Any", "Classic (pre-1950)", "Modern (1950-2000)", "Contemporary (2000+)"]
    )
    
    # Enhanced filtering options
    st.markdown("---")
    st.markdown("<h3>🎯 Enhanced Filters</h3>", unsafe_allow_html=True)
    
    # Reading level
    reading_level = st.selectbox(
        "Reading Level:",
        ["Any", "Beginner", "Intermediate", "Advanced"]
    )
    
    # Book length
    book_length = st.selectbox(
        "Book Length:",
        ["Any", "Short (<200 pages)", "Medium (200-400 pages)", "Long (>400 pages)"]
    )
    
    # Reading speed for time estimates
    reading_speed = st.selectbox(
        "Reading Speed (for time estimates):",
        ["Slow (150 wpm)", "Normal (250 wpm)", "Fast (350 wpm)"],
        index=1
    )
    st.session_state.reading_speed = reading_speed.split()[0].lower()
    
    # Book cover toggle
    show_covers = st.checkbox("Show book covers", value=True)
    st.session_state.show_book_covers = show_covers
    
    st.markdown("---")
    st.markdown("<h3>📚 Reading Lists</h3>", unsafe_allow_html=True)
    
    # Reading History Section
    st.markdown("<h4>📖 Reading History</h4>", unsafe_allow_html=True)
    
    # Search history
    history_search = st.text_input("Search your history:", placeholder="Search books, authors...")
    if history_search:
        history_results = st.session_state.analytics_helper.search_reading_history(history_search)
        if history_results:
            st.markdown("**Found in your history:**")
            for entry in history_results[:5]:  # Show last 5
                date = entry['timestamp'][:10]  # Just the date part
                st.markdown(f"📅 {date}: **{entry['book_title']}** by {entry['book_author']}")
        else:
            st.markdown("No matching history found")
    
    # Quick history stats
    analytics = st.session_state.analytics_helper.get_reading_analytics()
    if analytics['total_books_viewed'] > 0:
        st.markdown(f"**📊 Stats:** {analytics['total_books_viewed']} books viewed, {analytics['reading_streak']} day streak")
        
        # Clear history option
        if st.button("🗑️ Clear History", key="clear_history"):
            st.session_state.analytics_helper.clear_reading_history()
            st.success("Reading history cleared!")
            st.rerun()
    
    # Reading lists management
    list_tab = st.tabs(["📖 To Read", "📚 Currently Reading", "✅ Completed"])
    
    with list_tab[0]:
        to_read_books = st.session_state.enhanced_features.get_reading_list('to_read')
        if to_read_books:
            for i, book in enumerate(to_read_books):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{book.get('title', 'Unknown')}**")
                    st.write(f"by {book.get('author', 'Unknown')}")
                with col2:
                    if st.button("Remove", key=f"remove_to_read_{i}"):
                        st.session_state.enhanced_features.remove_from_reading_list(book, 'to_read')
                        st.rerun()
        else:
            st.write("No books in your To Read list")
    
    with list_tab[1]:
        current_books = st.session_state.enhanced_features.get_reading_list('currently_reading')
        if current_books:
            for i, book in enumerate(current_books):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{book.get('title', 'Unknown')}**")
                    st.write(f"by {book.get('author', 'Unknown')}")
                with col2:
                    if st.button("Remove", key=f"remove_current_{i}"):
                        st.session_state.enhanced_features.remove_from_reading_list(book, 'currently_reading')
                        st.rerun()
        else:
            st.write("No books in your Currently Reading list")
    
    with list_tab[2]:
        completed_books = st.session_state.enhanced_features.get_reading_list('completed')
        if completed_books:
            for i, book in enumerate(completed_books):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{book.get('title', 'Unknown')}**")
                    st.write(f"by {book.get('author', 'Unknown')}")
                with col2:
                    if st.button("Remove", key=f"remove_completed_{i}"):
                        st.session_state.enhanced_features.remove_from_reading_list(book, 'completed')
                        st.rerun()
        else:
            st.write("No books in your Completed list")
    
    st.markdown("---")
    st.markdown("<h3>How It Works</h3>", unsafe_allow_html=True)
    st.markdown("<p>1. Enter a book you enjoy</p>", unsafe_allow_html=True)
    st.markdown("<p>2. Set your preferences</p>", unsafe_allow_html=True)
    st.markdown("<p>3. Discover personalized recommendations</p>", unsafe_allow_html=True)
    st.markdown("<p>4. Get your reading journey roadmap</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p>Built with ❤️ using LangChain & Streamlit</p>", unsafe_allow_html=True)

# Clear error message when input changes
if book_title != st.session_state.get('last_book_title', ''):
    st.session_state.error_message = None
    st.session_state.last_book_title = book_title

# Generate recommendations
if book_title:
    # Validate input
    is_valid, validation_result = validate_book_title(book_title)
    
    if not is_valid:
        st.error(validation_result)
    else:
        # Clear previous error
        st.session_state.error_message = None
        
        try:
            with st.spinner("📖 Exploring the literary universe for perfect recommendations..."):
                response = langchain_helper.generate_book_recommendations(
                    validation_result,  # Use validated title
                    num_books=num_books,
                    genres=genres,
                    era=era,
                    reading_level=reading_level,
                    book_length=book_length
                )
                
                # Track analytics
                st.session_state.analytics_helper.add_to_search_history(validation_result, num_books)
                st.session_state.analytics_helper.update_reading_stats(genres)
                
                # Validate response
                if not response or 'book_recommendations' not in response or 'reading_journey' not in response:
                    raise Exception("Invalid response from AI service")
                
                # Store in session state
                st.session_state.recommendations = response['book_recommendations']
                st.session_state.reading_journey = response['reading_journey']
        
            # Display recommendations with enhanced features
            st.subheader(f"✨ Books Similar to '{validation_result}'")
            
            # Extract book details for enhanced display
            books = st.session_state.enhanced_features.extract_book_details(st.session_state.recommendations)
            
            # Debug: Show how many books were extracted
            print(f"DEBUG: Extracted {len(books)} books from recommendations")
            
            # Display books with covers and enhanced features
            if books:
                for i, book in enumerate(books):
                    # Track book in reading history
                    st.session_state.analytics_helper.add_to_reading_history(book, validation_result)
                    with st.container():
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            # Book cover
                            if st.session_state.show_book_covers:
                                cover_url = st.session_state.enhanced_features.get_book_cover(
                                    book.get('title', ''), 
                                    book.get('author', '')
                                )
                                if cover_url:
                                    st.image(cover_url, width=120, caption="Book Cover")
                                else:
                                    # Placeholder for no cover
                                    st.markdown("""
                                    <div style="width: 120px; height: 160px; background: #f0f0f0; 
                                             display: flex; align-items: center; justify-content: center; 
                                             border: 1px solid #ddd; border-radius: 8px;">
                                        <span style="color: #666; font-size: 12px;">No Cover</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        with col2:
                            # Book information
                            book_title = book.get('title', 'Unknown Title')
                            book_author = book.get('author', 'Unknown Author')
                            
                            st.markdown(f"### {book_title}")
                            st.markdown(f"**Author:** {book_author}")
                            if book.get('year'):
                                st.markdown(f"**Year:** {book.get('year')}")
                            
                            # Reading time estimate
                            reading_time_minutes, reading_time_str = st.session_state.enhanced_features.estimate_reading_time(
                                book, st.session_state.reading_speed
                            )
                            st.markdown(f"**⏱️ Estimated Reading Time:** {reading_time_str}")
                            
                            # Book description
                            if book.get('description'):
                                st.markdown(f"**Description:** {book.get('description')}")
                            
                            # Why recommended
                            if book.get('reason'):
                                st.markdown(f"**Why Recommended:** {book.get('reason')}")
                            
                            # Reading list buttons
                            col_btn1, col_btn2, col_btn3 = st.columns(3)
                            with col_btn1:
                                if st.button("📖 To Read", key=f"to_read_{i}"):
                                    if st.session_state.enhanced_features.add_to_reading_list(book, 'to_read'):
                                        st.success("Added to To Read list!")
                                    else:
                                        st.info("Already in To Read list")
                            
                            with col_btn2:
                                if st.button("📚 Currently Reading", key=f"current_{i}"):
                                    if st.session_state.enhanced_features.add_to_reading_list(book, 'currently_reading'):
                                        st.success("Added to Currently Reading list!")
                                    else:
                                        st.info("Already in Currently Reading list")
                            
                            with col_btn3:
                                if st.button("✅ Completed", key=f"completed_{i}"):
                                    if st.session_state.enhanced_features.add_to_reading_list(book, 'completed'):
                                        st.success("Added to Completed list!")
                                    else:
                                        st.info("Already in Completed list")
                        
                        st.markdown("---")
            else:
                # Fallback if no books were extracted
                st.warning("⚠️ Could not parse book details from recommendations. Showing original format below.")
                st.markdown("### 📝 Original Recommendations")
                st.markdown(st.session_state.recommendations, unsafe_allow_html=True)
            
            # Also show the original markdown for compatibility
            st.markdown("### 📝 Detailed Recommendations")
            st.markdown(st.session_state.recommendations, unsafe_allow_html=True)
        
            # Reading journey
            st.subheader("🌟 Your Personalized Reading Journey")
            st.markdown(st.session_state.reading_journey, unsafe_allow_html=True)
            
            # Analytics Dashboard Section
            st.markdown("---")
            st.subheader("📊 Reading Analytics Dashboard")
            
            analytics = st.session_state.analytics_helper.get_reading_analytics()
            
            # Analytics overview
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📖 Books Viewed", analytics['total_books_viewed'])
            with col2:
                st.metric("🔍 Total Searches", analytics['total_searches'])
            with col3:
                st.metric("🔥 Reading Streak", f"{analytics['reading_streak']} days")
            with col4:
                if analytics['favorite_genres']:
                    top_genre = max(analytics['favorite_genres'].items(), key=lambda x: x[1])
                    st.metric("🎯 Top Genre", f"{top_genre[0]} ({top_genre[1]})")
                else:
                    st.metric("🎯 Top Genre", "None yet")
            
            # Most viewed books
            if analytics['most_viewed_books']:
                st.markdown("### 📈 Most Viewed Books")
                for book, count in analytics['most_viewed_books']:
                    st.markdown(f"• **{book}** - Viewed {count} times")
            
            # Export options
            st.markdown("### 📤 Export Options")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Export Reading History"):
                    export_data = st.session_state.analytics_helper.export_reading_history('csv')
                    st.download_button(
                        label="📥 Download CSV",
                        data=export_data,
                        file_name="reading_history.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("📚 Export Reading Lists"):
                    lists_data = st.session_state.enhanced_features.get_all_reading_lists()
                    export_data = st.session_state.analytics_helper.export_reading_lists(lists_data, 'csv')
                    st.download_button(
                        label="📥 Download CSV",
                        data=export_data,
                        file_name="reading_lists.csv",
                        mime="text/csv"
                    )
            
            # Reading Lists Management Section
            st.markdown("---")
            st.subheader("📚 Reading Lists Management")
            
            # Export options
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📤 Export To Read List"):
                    export_text = st.session_state.enhanced_features.export_reading_list('to_read')
                    st.text_area("To Read List Export", export_text, height=200)
            
            with col2:
                if st.button("📤 Export Currently Reading"):
                    export_text = st.session_state.enhanced_features.export_reading_list('currently_reading')
                    st.text_area("Currently Reading Export", export_text, height=200)
            
            with col3:
                if st.button("📤 Export Completed"):
                    export_text = st.session_state.enhanced_features.export_reading_list('completed')
                    st.text_area("Completed List Export", export_text, height=200)
            
            # Clear lists options
            st.markdown("### 🗑️ Clear Lists")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Clear To Read List"):
                    if st.session_state.enhanced_features.clear_reading_list('to_read'):
                        st.success("To Read list cleared!")
                    else:
                        st.error("Failed to clear list")
            
            with col2:
                if st.button("Clear Currently Reading"):
                    if st.session_state.enhanced_features.clear_reading_list('currently_reading'):
                        st.success("Currently Reading list cleared!")
                    else:
                        st.error("Failed to clear list")
            
            with col3:
                if st.button("Clear Completed"):
                    if st.session_state.enhanced_features.clear_reading_list('completed'):
                        st.success("Completed list cleared!")
                    else:
                        st.error("Failed to clear list")
            
            # Success message
            st.success("🎉 Happy reading! May your literary journey be unforgettable!")
            
            # WhatsApp sharing button
            st.markdown("---")
            st.subheader("📤 Share Your Recommendations")
            st.markdown("""
            <div class="share-container">
                <p>Share these book recommendations with friends on WhatsApp!</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💬 Share via WhatsApp", key="whatsapp_share", use_container_width=True, type="primary"):
                st.balloons()
                
                try:
                    # Create WhatsApp message with better parsing
                    whatsapp_message = f"📚 *Book Recommendations from BookVoyager!*\n\n"
                    whatsapp_message += f"I discovered these amazing books similar to *{validation_result}*:\n\n"
                    
                    # Extract book information using the new function
                    books = extract_book_info_from_markdown(st.session_state.recommendations)
                    
                    for i, book in enumerate(books[:5]):  # Limit to 5 books for WhatsApp
                        if 'title' in book and 'author' in book:
                            whatsapp_message += f"• **{book['title']}** by {book['author']}"
                            if 'year' in book:
                                whatsapp_message += f" ({book['year']})"
                            whatsapp_message += "\n"
                    
                    whatsapp_message += "\n🌟 *My Personalized Reading Journey:*\n"
                    
                    # Add reading journey highlights with better parsing
                    if st.session_state.reading_journey:
                        # Extract journey steps using regex
                        journey_pattern = r'\*\*(Start with|Continue with|Explore|Dive into|Finish with)\*\*: ([^-\n]+)'
                        journey_matches = re.findall(journey_pattern, st.session_state.reading_journey)
                        
                        for step_type, description in journey_matches:
                            clean_description = description.strip()
                            whatsapp_message += f"→ **{step_type}**: {clean_description}\n"
                    
                    whatsapp_message += "\nDiscover your next read at BookVoyager!"
                    
                    # Encode for WhatsApp URL
                    encoded_message = urllib.parse.quote(whatsapp_message)
                    whatsapp_url = f"https://wa.me/?text={encoded_message}"
                    
                    # Show success and link
                    st.success("✅ WhatsApp message created! Click the button below to share:")
                    st.markdown(f'''
                        <a href="{whatsapp_url}" target="_blank" style="
                            display: inline-block;
                            background-color: #25D366;
                            color: #fff !important;
                            font-weight: bold;
                            font-size: 1.2rem;
                            padding: 14px 28px;
                            border-radius: 8px;
                            text-decoration: none;
                            margin-top: 12px;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                            transition: background 0.2s;
                        " onmouseover="this.style.backgroundColor='#128C7E'" onmouseout="this.style.backgroundColor='#25D366'">
                            💬 Open WhatsApp to Share
                        </a>
                    ''', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error creating WhatsApp message: {str(e)}")
        
        except Exception as e:
            error_msg = str(e)
            st.error(error_msg)
            st.session_state.error_message = error_msg
            
            # Show helpful information when API is down
            if "temporarily unavailable" in error_msg.lower():
                st.info("💡 **What you can do:**")
                st.markdown("""
                - **Try again in a few minutes** - This is usually a temporary issue
                - **Check service status** - Visit [Groq Status](https://groqstatus.com/) for updates
                - **Try a different book** - Sometimes specific requests can cause issues
                """)
                
                # Provide some basic recommendations as fallback
                st.markdown("---")
                st.subheader("📚 While we wait, here are some popular book recommendations:")
                
                fallback_recommendations = """
                **Popular Fantasy Books:**
                1. **Title**: The Lord of the Rings  
                   **Author**: J.R.R. Tolkien  
                   **Year**: 1954  
                   **Description**: Epic fantasy trilogy about a quest to destroy a powerful ring.
                   **Why Recommended**: Classic fantasy that has influenced the genre for decades.

                2. **Title**: Harry Potter and the Sorcerer's Stone  
                   **Author**: J.K. Rowling  
                   **Year**: 1997  
                   **Description**: The first book in the magical series about a young wizard.
                   **Why Recommended**: Beloved children's fantasy that appeals to all ages.

                **Popular Self-Help Books:**
                1. **Title**: Atomic Habits  
                   **Author**: James Clear  
                   **Year**: 2018  
                   **Description**: A guide to building good habits and breaking bad ones.
                   **Why Recommended**: Practical advice for personal development.

                2. **Title**: The 7 Habits of Highly Effective People  
                   **Author**: Stephen Covey  
                   **Year**: 1989  
                   **Description**: Classic self-help book about personal and professional effectiveness.
                   **Why Recommended**: Timeless principles for success and leadership.
                """
                
                st.markdown(fallback_recommendations, unsafe_allow_html=True)
            
            # Clear previous results
            st.session_state.recommendations = None
            st.session_state.reading_journey = None

# Display error message if exists
if st.session_state.error_message:
    st.markdown(f"""
    <div class="error-message">
        <strong>Error:</strong> {st.session_state.error_message}
    </div>
    """, unsafe_allow_html=True)

else:
    # Hero section
    col1, col2 = st.columns([1, 2])
    with col1:
        # Using an online book icon
        st.image("https://cdn-icons-png.flaticon.com/512/2909/2909473.png", width=200)
    with col2:
        st.markdown("""
        <div class="hero-text">
            <h3>Discover Your Next Favorite Book</h3>
            <p>Our AI-powered recommendation system analyzes thousands of books to find perfect matches for your taste.</p>
            <p>Just tell us a book you love, and we'll create a personalized reading journey!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("---")
    st.subheader("🚀 Why BookVoyager?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📚 Intelligent Recommendations")
        st.markdown("Our AI understands complex literary patterns to find books you'll truly love.")
    
    with col2:
        st.markdown("### 🗺️ Reading Journeys")
        st.markdown("We don't just recommend books - we create curated reading experiences with thematic progression.")
    
    with col3:
        st.markdown("### 🎯 Personalized Filters")
        st.markdown("Filter by genre, era, or mood to get recommendations that match your current reading preferences.")
    
    # Testimonials
    st.markdown("---")
    st.subheader("📣 What Readers Say")
    testimonial1, testimonial2 = st.columns(2)
    
    with testimonial1:
        st.markdown("""
        <div class="testimonial">
            "BookVoyager helped me discover three new favorite authors! 
            The reading journey feature is brilliant - it made my book club selections effortless."
            <div class="author">- Sarah J., Avid Reader</div>
        </div>
        """, unsafe_allow_html=True)
    
    with testimonial2:
        st.markdown("""
        <div class="testimonial">
            "As a librarian, I'm impressed by the quality of recommendations. 
            The AI understands literary connections better than most humans!"
            <div class="author">- David R., Public Librarian</div>
        </div>
        """, unsafe_allow_html=True)