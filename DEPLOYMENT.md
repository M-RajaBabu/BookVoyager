# 🚀 BookVoyager Deployment Guide

This guide will help you deploy your BookVoyager application to various cloud platforms.

## 📋 Prerequisites

1. **GitHub Account**: You'll need a GitHub account to host your code
2. **Groq API Key**: Get a free API key from [groq.com](https://groq.com)
3. **Python Knowledge**: Basic understanding of Python and web deployment

## 🎯 Quick Deployment Options

### Option 1: Streamlit Cloud (Recommended)

**Pros**: Free, Easy, Fast, No server management
**Cons**: Limited customization

**Steps**:
1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Get Groq API Key**:
   - Visit [groq.com](https://groq.com)
   - Sign up for free account
   - Copy your API key

3. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `main.py`
   - Add environment variable: `GROQ_API_KEY`
   - Click "Deploy app"

**Deployment Time**: 2-3 minutes

### Option 2: Railway

**Pros**: Free tier, Good performance, Easy setup
**Cons**: Limited free usage

**Steps**:
1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub** repository
3. **Add environment variable**:
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key
4. **Deploy** - Railway auto-detects Python apps

### Option 3: Render

**Pros**: Free tier, Reliable, Good documentation
**Cons**: Slower cold starts

**Steps**:
1. **Sign up** at [render.com](https://render.com)
2. **Create new Web Service**
3. **Connect** GitHub repository
4. **Configure**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run main.py --server.port $PORT --server.address 0.0.0.0`
5. **Add environment variable**:
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key
6. **Deploy**

## 🔧 Advanced Deployment

### Heroku Deployment

**Prerequisites**: Heroku CLI installed

1. **Create Procfile**:
   ```
   web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy**:
   ```bash
   heroku create your-app-name
   heroku config:set GROQ_API_KEY=your_api_key
   git push heroku main
   ```

### Docker Deployment

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   EXPOSE 8501
   
   CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run**:
   ```bash
   docker build -t bookvoyager .
   docker run -p 8501:8501 -e GROQ_API_KEY=your_key bookvoyager
   ```

## 🔑 Environment Variables

All deployments require this environment variable:

| Variable | Description | Example |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | `gsk_abc123...` |

## 📊 Deployment Comparison

| Platform | Free Tier | Setup Time | Performance | Custom Domain |
|----------|-----------|------------|-------------|---------------|
| Streamlit Cloud | ✅ | 5 min | ⭐⭐⭐⭐ | ❌ |
| Railway | ✅ | 10 min | ⭐⭐⭐⭐⭐ | ✅ |
| Render | ✅ | 15 min | ⭐⭐⭐ | ✅ |
| Heroku | ❌ | 20 min | ⭐⭐⭐⭐ | ✅ |

## 🐛 Troubleshooting

### Common Issues

1. **"GROQ_API_KEY not found"**
   - Solution: Add the environment variable in your deployment platform

2. **"Module not found"**
   - Solution: Ensure `requirements.txt` is in the root directory

3. **"Port already in use"**
   - Solution: Use `$PORT` environment variable in start command

4. **"Build failed"**
   - Solution: Check Python version compatibility (3.8+)

### Debug Commands

```bash
# Test locally
streamlit run main.py

# Check dependencies
pip list

# Test API connection
python -c "from langchain_helper import test_api_connection; test_api_connection()"
```

## 📈 Monitoring & Maintenance

### Health Checks
- Monitor your app's uptime
- Check API usage limits
- Review error logs

### Updates
- Keep dependencies updated
- Monitor for security patches
- Test new features locally first

## 🆘 Support

If you encounter issues:

1. **Check logs** in your deployment platform
2. **Test locally** first
3. **Verify API key** is correct
4. **Check** [Streamlit documentation](https://docs.streamlit.io)
5. **Create issue** on GitHub

---

**Happy Deploying! 🚀**

Your BookVoyager app will be live and ready to help readers discover their next favorite books! 