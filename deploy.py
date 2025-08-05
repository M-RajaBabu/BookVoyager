#!/usr/bin/env python3
"""
BookVoyager Deployment Helper Script
This script helps you prepare and deploy your BookVoyager application.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if we're in the right directory
    required_files = ['main.py', 'requirements.txt', 'langchain_helper.py']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("⚠️  No .env file found. You'll need to set GROQ_API_KEY in your deployment platform.")
    
    print("✅ Prerequisites check completed!")
    return True

def test_local_deployment():
    """Test if the app runs locally"""
    print("🧪 Testing local deployment...")
    
    try:
        # Test if streamlit is installed (try virtual environment first)
        streamlit_cmd = 'venv\\Scripts\\streamlit.exe' if os.name == 'nt' else 'venv/bin/streamlit'
        
        if os.path.exists(streamlit_cmd):
            result = subprocess.run([streamlit_cmd, '--version'], 
                                  capture_output=True, text=True, timeout=10)
        else:
            # Fallback to system streamlit
            result = subprocess.run(['streamlit', '--version'], 
                                  capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            print("❌ Streamlit not found. Please install it first:")
            print("   pip install streamlit")
            return False
        
        print("✅ Streamlit is installed")
        return True
        
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it first:")
        print("   pip install streamlit")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Timeout while checking streamlit")
        return False

def generate_deployment_info():
    """Generate deployment information"""
    print("📋 Generating deployment information...")
    
    deployment_info = {
        "app_name": "BookVoyager",
        "main_file": "main.py",
        "requirements": "requirements.txt",
        "environment_variables": {
            "GROQ_API_KEY": "Your Groq API key from groq.com"
        },
        "deployment_platforms": {
            "streamlit_cloud": {
                "url": "https://share.streamlit.io",
                "steps": [
                    "Sign in with GitHub",
                    "Click 'New app'",
                    "Select your repository",
                    "Set main file path to 'main.py'",
                    "Add GROQ_API_KEY environment variable",
                    "Click 'Deploy app'"
                ]
            },
            "railway": {
                "url": "https://railway.app",
                "steps": [
                    "Sign up and connect GitHub",
                    "Add GROQ_API_KEY environment variable",
                    "Deploy (auto-detects Python app)"
                ]
            },
            "render": {
                "url": "https://render.com",
                "steps": [
                    "Create new Web Service",
                    "Connect GitHub repository",
                    "Set build command: pip install -r requirements.txt",
                    "Set start command: streamlit run main.py --server.port $PORT --server.address 0.0.0.0",
                    "Add GROQ_API_KEY environment variable",
                    "Deploy"
                ]
            }
        }
    }
    
    # Save deployment info
    with open('deployment_info.json', 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    print("✅ Deployment information saved to deployment_info.json")
    return deployment_info

def main():
    """Main deployment helper function"""
    print("🚀 BookVoyager Deployment Helper")
    print("=" * 40)
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites not met. Please fix the issues above.")
        sys.exit(1)
    
    # Test local deployment
    if not test_local_deployment():
        print("❌ Local deployment test failed.")
        sys.exit(1)
    
    # Generate deployment info
    deployment_info = generate_deployment_info()
    
    print("\n🎉 Deployment preparation completed!")
    print("\n📋 Next Steps:")
    print("1. Get your Groq API key from https://groq.com")
    print("2. Choose a deployment platform:")
    
    for platform, info in deployment_info["deployment_platforms"].items():
        print(f"   - {platform.replace('_', ' ').title()}: {info['url']}")
    
    print("\n3. Follow the steps in DEPLOYMENT.md")
    print("4. Set the GROQ_API_KEY environment variable")
    print("5. Deploy your app!")
    
    print(f"\n📄 Detailed instructions: DEPLOYMENT.md")
    print(f"📄 Deployment info: deployment_info.json")

if __name__ == "__main__":
    main() 