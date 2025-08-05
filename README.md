# 📚 BookVoyager - AI-Powered Book Recommendation System

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-00FF00?style=for-the-badge&logo=langchain&logoColor=black)](https://langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **Discover your next literary adventure with AI-powered book recommendations and personalized reading journeys.**

## 🌟 Live Demo

**🚀 Deployed on Streamlit Cloud:** [BookVoyager App](https://bookvoyager.streamlit.app)

## 📖 Overview

BookVoyager is an intelligent book recommendation system that uses advanced AI to analyze your reading preferences and suggest personalized book recommendations. Whether you're looking for your next favorite novel or exploring new genres, BookVoyager creates curated reading journeys tailored to your taste.

## ✨ Key Features

### 🎯 Core Features
- **AI-Powered Recommendations**: Advanced language model analyzes thousands of books
- **Personalized Reading Journeys**: Curated thematic progression through books
- **Smart Filtering**: Filter by genre, era, reading level, and book length
- **Book Cover Images**: Visual book covers from Google Books API
- **Reading Time Estimates**: Practical time planning for your reading

### 📊 Enhanced Features
- **Reading Analytics Dashboard**: Track your reading patterns and preferences
- **Reading Lists**: Organize books into "To Read", "Currently Reading", "Completed"
- **Reading History**: Remember and search through your past explorations
- **Enhanced Search**: Better book discovery with recent search suggestions
- **Export Features**: Save your reading lists and history in multiple formats

### 🎨 User Experience
- **Dark/Light Theme**: Toggle between themes for comfortable reading
- **Responsive Design**: Works perfectly on desktop and mobile
- **WhatsApp Sharing**: Share recommendations with friends
- **Reading Speed Settings**: Customize reading time estimates

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Groq API key (free at [groq.com](https://groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/M-RajaBabu/BookVoyager.git
   cd BookVoyager
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 🛠️ How It Works

### Architecture
```
BookVoyager/
├── main.py                 # Main Streamlit application
├── langchain_helper.py     # AI recommendation engine
├── enhanced_features.py    # Book covers & reading lists
├── analytics_helper.py     # Analytics & export features
├── requirements.txt        # Python dependencies
└── README.md             # This file
```

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **AI Engine**: LangChain + Groq LLM
- **Book Data**: Google Books API
- **Styling**: Custom CSS with theme support
- **Data Storage**: Streamlit session state

### AI Recommendation Process
1. **Input Analysis**: User provides a book title or topic
2. **AI Processing**: LangChain analyzes the input using Groq LLM
3. **Book Matching**: Finds similar books based on themes, genres, and style
4. **Journey Creation**: Generates a personalized reading progression
5. **Enhanced Display**: Shows covers, reading time, and detailed descriptions

## 📊 Features in Detail

### 🎯 Smart Recommendations
- **Contextual Analysis**: AI understands complex literary patterns
- **Genre Filtering**: Focus on specific genres or explore broadly
- **Era Preferences**: Choose from Classic, Modern, or Contemporary
- **Reading Level**: Beginner, Intermediate, or Advanced
- **Book Length**: Short, Medium, or Long books

### 📈 Reading Analytics
- **Reading Streaks**: Track your daily reading consistency
- **Genre Preferences**: Discover your favorite book categories
- **Search History**: Remember your past book explorations
- **Most Viewed Books**: See which recommendations resonated most

### 📚 Reading Lists Management
- **To Read**: Save books for future reading
- **Currently Reading**: Track your active reads
- **Completed**: Keep a record of finished books
- **Export Options**: Download lists in CSV, JSON, or TXT formats

### 🎨 User Interface
- **Theme Toggle**: Switch between dark and light modes
- **Responsive Design**: Optimized for all screen sizes
- **Visual Elements**: Book covers, icons, and intuitive navigation
- **Accessibility**: High contrast and readable text

## 🔧 Configuration

### Environment Variables
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### Customization Options
- **Reading Speed**: Adjust time estimates (Slow/Normal/Fast)
- **Book Covers**: Toggle cover image display
- **Enhanced Features**: Enable/disable advanced features
- **Theme**: Choose between dark and light modes

## 📦 Deployment

### Streamlit Cloud (Recommended - Free)

**Current Status**: ✅ Already deployed at [https://bookvoyager.streamlit.app](https://bookvoyager.streamlit.app)

**To deploy your own version:**

1. **Fork/Clone** this repository to your GitHub account
2. **Get a Groq API Key**:
   - Visit [groq.com](https://groq.com)
   - Sign up for a free account
   - Get your API key from the dashboard
3. **Go to** [share.streamlit.io](https://share.streamlit.io)
4. **Sign in** with your GitHub account
5. **Connect** your repository
6. **Set environment variables**:
   - Click "Advanced settings"
   - Add: `GROQ_API_KEY` = `your_groq_api_key_here`
7. **Deploy!** - Click "Deploy app"

**Deployment Time**: ~2-3 minutes

### Option 2: Railway (Alternative - Free Tier)

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect** your GitHub repository
3. **Add environment variable**:
   - `GROQ_API_KEY`: Your Groq API key
4. **Deploy** - Railway will auto-detect it's a Python app

### Option 3: Render (Alternative - Free Tier)

1. **Sign up** at [render.com](https://render.com)
2. **Create new Web Service**
3. **Connect** your GitHub repository
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run main.py --server.port $PORT`
5. **Add environment variable**:
   - `GROQ_API_KEY`: Your Groq API key
6. **Deploy**

### Option 4: Heroku (Paid)

1. **Install Heroku CLI**
2. **Create** `Procfile`:
   ```
   web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
   ```
3. **Deploy**:
   ```bash
   heroku create your-app-name
   heroku config:set GROQ_API_KEY=your_api_key
   git push heroku main
   ```

### Environment Variables Required

All deployment platforms need this environment variable:
- `GROQ_API_KEY`: Your Groq API key from [groq.com](https://groq.com)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Areas for Contribution
- **New Features**: Additional recommendation algorithms
- **UI Improvements**: Better user experience
- **Bug Fixes**: Report and fix issues
- **Documentation**: Improve guides and examples
- **Testing**: Add comprehensive tests

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit Team**: For the amazing web framework
- **LangChain**: For the powerful AI framework
- **Groq**: For the fast and reliable LLM API
- **Google Books API**: For book cover images and metadata
- **Open Source Community**: For inspiration and tools

## 📞 Support

If you encounter any issues or have questions:

1. **Check the documentation** in this README
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Contact the author** for direct support

---

## 👨‍💻 Author

**Raja Babu Meena**

- **GitHub**: [M-RajaBabu](https://github.com/M-RajaBabu)
- **LinkedIn**: [Raja Babu Meena](https://linkedin.com/in/raja-babu-meena)
- **Email**: raja.babu.meena@gmail.com

---

<div align="center">

**Made with ❤️ by Raja Babu Meena**

*Discover your next literary adventure with BookVoyager!*

[![BookVoyager](https://img.shields.io/badge/BookVoyager-📚-blue?style=for-the-badge)](https://github.com/M-RajaBabu/BookVoyager)

</div> 