# 📚 BookVoyager - AI-Powered Book Recommendation System

<div align="center">

![BookVoyager Logo](https://cdn-icons-png.flaticon.com/512/2909/2909473.png)

**Discover Your Next Favorite Book with Intelligent AI Recommendations**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36.0-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.2.0-green.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 🌟 Overview

BookVoyager is an intelligent book recommendation system that uses advanced AI to analyze your reading preferences and create personalized reading journeys. Built with modern web technologies and powered by Groq's LLM, it provides sophisticated book recommendations with enhanced features like reading analytics, book covers, and social sharing.

### ✨ Key Features

- **🤖 AI-Powered Recommendations**: Advanced LLM-based book suggestions
- **📊 Reading Analytics Dashboard**: Track your reading patterns and preferences
- **📚 Reading Lists Management**: Organize books into To Read, Currently Reading, and Completed lists
- **🖼️ Book Cover Integration**: Visual book covers from Google Books API
- **⏱️ Reading Time Estimates**: Plan your reading schedule with time estimates
- **🔍 Enhanced Search & Filtering**: Filter by genre, era, reading level, and book length
- **📈 Reading History**: Track your exploration journey
- **📤 Export Features**: Export reading lists and history in multiple formats
- **💬 Social Sharing**: Share recommendations via WhatsApp
- **🎨 Beautiful UI**: Modern, responsive design with dark/light theme support

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/M-RajaBabu/BookVoyager.git
   cd BookVoyager
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

---

## 🏗️ Architecture

### Core Components

- **`main.py`**: Main Streamlit application with UI and user interaction
- **`langchain_helper.py`**: AI recommendation engine using Groq LLM
- **`enhanced_features.py`**: Book covers, reading time estimation, and reading lists
- **`analytics_helper.py`**: Reading analytics, history tracking, and export features
- **`style.css`**: Custom styling for enhanced UI/UX

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI/ML**: LangChain + Groq LLM
- **APIs**: Google Books API (book covers)
- **Data Management**: Session state management
- **Styling**: Custom CSS with theme support

---

## 📖 How It Works

### 1. **Input Processing**
- Users enter a book they love
- System validates and processes the input
- Applies user-selected filters (genre, era, reading level)

### 2. **AI Analysis**
- LangChain processes the input through Groq LLM
- Generates personalized book recommendations
- Creates thematic reading journeys

### 3. **Enhanced Display**
- Extracts book details from AI response
- Fetches book covers from Google Books API
- Calculates reading time estimates
- Displays recommendations with rich metadata

### 4. **User Interaction**
- Add books to reading lists
- Track reading history and analytics
- Export data in multiple formats
- Share recommendations socially

---

## 🎯 Features in Detail

### 📊 Analytics Dashboard
- **Reading Statistics**: Total books viewed, searches performed
- **Reading Streak**: Track consecutive days of reading activity
- **Genre Analysis**: Most explored genres and preferences
- **Most Viewed Books**: Popular recommendations from your searches

### 📚 Reading Lists
- **To Read**: Books you want to read next
- **Currently Reading**: Books you're actively reading
- **Completed**: Books you've finished
- **Export Options**: Download lists in CSV, JSON, or TXT formats

### 🔍 Enhanced Filtering
- **Genre Filter**: Fantasy, Sci-Fi, Mystery, Romance, etc.
- **Era Filter**: Classic, Modern, Contemporary
- **Reading Level**: Beginner, Intermediate, Advanced
- **Book Length**: Short, Medium, Long
- **Reading Speed**: Slow, Normal, Fast

### 📤 Export Features
- **Reading History**: Export your exploration journey
- **Reading Lists**: Export organized book collections
- **Multiple Formats**: CSV, JSON, and TXT support
- **Detailed Metadata**: Book titles, authors, years, descriptions

---

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | Yes |

### Customization

You can customize the application by modifying:

- **`style.css`**: Change colors, fonts, and layout
- **`main.py`**: Modify UI components and layout
- **`langchain_helper.py`**: Adjust AI prompts and parameters
- **`enhanced_features.py`**: Customize book cover fetching and reading time calculation

---

## 📁 Project Structure

```
bookvoyager/
├── main.py                 # Main Streamlit application
├── langchain_helper.py     # AI recommendation engine
├── enhanced_features.py    # Book covers and reading lists
├── analytics_helper.py     # Analytics and export features
├── style.css              # Custom styling
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── background.jpg         # Background image
└── books_background.avif  # Books background image
```

---

## 🔧 Development

### Running in Development Mode

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
streamlit run main.py --server.runOnSave true
```

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and modular

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Raja Babu Meena**

- **GitHub**: [@rajababumeena](https://github.com/rajababumeena)
- **LinkedIn**: [Raja Babu Meena](https://linkedin.com/in/rajababumeena)
- **Email**: rajababumeena@example.com

---

## 🙏 Acknowledgments

- **Groq**: For providing the LLM API
- **Google Books API**: For book cover images
- **Streamlit**: For the amazing web framework
- **LangChain**: For the AI/ML framework
- **Open Source Community**: For inspiration and support

---

## 📞 Support

If you have any questions or need help, please:

1. Check the [Issues](https://github.com/M-RajaBabu/BookVoyager/issues) page
2. Create a new issue with detailed information
3. Contact the author directly

---

<div align="center">

**Made with ❤️ by Raja Babu Meena**

*Discover the joy of reading with AI-powered recommendations*

</div> 