#!/bin/bash

echo "🚀 Ticketmaster Bot Deployment Script"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "requirements.txt" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📋 Checking prerequisites..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Prerequisites check passed!"

echo ""
echo "🔧 Setting up frontend..."

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Build the project
echo "🏗️ Building frontend..."
npm run build

echo "✅ Frontend build completed!"

# Go back to root
cd ..

echo ""
echo "📝 Deployment Instructions:"
echo "=========================="
echo ""
echo "1. 🎯 Deploy Frontend to Netlify:"
echo "   - Go to https://netlify.com"
echo "   - Click 'New site from Git'"
echo "   - Connect your repository"
echo "   - Set Base directory: frontend"
echo "   - Set Build command: npm run build"
echo "   - Set Publish directory: build"
echo ""
echo "2. 🔧 Deploy Backend to Railway:"
echo "   - Go to https://railway.app"
echo "   - Click 'New Project' > 'Deploy from GitHub repo'"
echo "   - Connect your repository"
echo "   - Add environment variables from your .env file"
echo ""
echo "3. 🔗 Connect Frontend and Backend:"
echo "   - Get your Railway backend URL"
echo "   - In Netlify, go to Site settings > Environment variables"
echo "   - Add: REACT_APP_API_URL = your_backend_url"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo ""
echo "🎉 Happy deploying!" 