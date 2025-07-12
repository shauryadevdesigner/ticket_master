# 🚀 Deployment Guide

This guide will help you deploy your Ticketmaster Ticket Tracker to the web!

## 📋 Overview

This project consists of two parts:
1. **Frontend**: React app (deployed to Netlify)
2. **Backend**: Python Flask API (deployed to Railway/Render/Heroku)

## 🎯 Frontend Deployment (Netlify)

### Option 1: Deploy via Netlify UI (Recommended)

1. **Prepare your repository:**
   - Make sure your code is pushed to GitHub/GitLab/Bitbucket
   - Ensure the `frontend/` folder contains your React app

2. **Deploy to Netlify:**
   - Go to [netlify.com](https://netlify.com) and sign up/login
   - Click "New site from Git"
   - Connect your repository
   - Set build settings:
     - **Base directory**: `frontend`
     - **Build command**: `npm run build`
     - **Publish directory**: `build`
   - Click "Deploy site"

3. **Configure Environment Variables:**
   - In your Netlify dashboard, go to Site settings > Environment variables
   - Add: `REACT_APP_API_URL` = your backend URL (e.g., `https://your-backend.railway.app`)

### Option 2: Deploy via Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Navigate to frontend directory
cd frontend

# Build the project
npm run build

# Deploy to Netlify
netlify deploy --prod --dir=build
```

## 🔧 Backend Deployment

### Option 1: Railway (Recommended)

1. **Prepare for Railway:**
   - Create a `Procfile` in the root directory:
     ```
     web: python src/app.py
     ```
   - Ensure `requirements.txt` is in the root directory

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app) and sign up/login
   - Click "New Project" > "Deploy from GitHub repo"
   - Connect your repository
   - Railway will automatically detect it's a Python app
   - Set environment variables in Railway dashboard (copy from your `.env` file)

3. **Get your backend URL:**
   - Railway will provide a URL like `https://your-app.railway.app`
   - Use this URL as your `REACT_APP_API_URL` in Netlify

### Option 2: Render

1. **Prepare for Render:**
   - Create a `render.yaml` file in the root:
     ```yaml
     services:
       - type: web
         name: ticketmaster-bot
         env: python
         buildCommand: pip install -r requirements.txt
         startCommand: python src/app.py
     ```

2. **Deploy to Render:**
   - Go to [render.com](https://render.com) and sign up/login
   - Click "New" > "Web Service"
   - Connect your repository
   - Set build and start commands
   - Add environment variables

### Option 3: Heroku

1. **Prepare for Heroku:**
   - Create a `Procfile` in the root:
     ```
     web: python src/app.py
     ```
   - Create `runtime.txt`:
     ```
     python-3.10.0
     ```

2. **Deploy to Heroku:**
   ```bash
   # Install Heroku CLI
   # Create Heroku app
   heroku create your-app-name
   
   # Add environment variables
   heroku config:set DISCORD_WEBHOOK_URL=your_webhook_url
   heroku config:set TELEGRAM_BOT_TOKEN=your_bot_token
   # ... add other env vars
   
   # Deploy
   git push heroku main
   ```

## 🔗 Connecting Frontend and Backend

1. **Get your backend URL** from your hosting service
2. **Set the environment variable** in Netlify:
   - Go to Site settings > Environment variables
   - Add: `REACT_APP_API_URL` = your backend URL
3. **Redeploy** your frontend if needed

## 🌐 Environment Variables

### Backend (Railway/Render/Heroku)
Copy these from your `.env` file:
```
DISCORD_WEBHOOK_URL=your_discord_webhook
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
SLACK_WEBHOOK_URL=your_slack_webhook
EMAIL_ADDRESS=your_email
EMAIL_PASSWORD=your_app_password
```

### Frontend (Netlify)
```
REACT_APP_API_URL=https://your-backend-url.com
```

## 🧪 Testing Your Deployment

1. **Test the backend API:**
   ```bash
   curl https://your-backend-url.com/api/events
   ```

2. **Test the frontend:**
   - Visit your Netlify URL
   - Try adding an event
   - Try sending a test notification

## 🔧 Troubleshooting

### Common Issues:

1. **CORS errors:**
   - Make sure `flask-cors` is installed
   - Check that CORS is enabled in your Flask app

2. **Environment variables not working:**
   - Double-check variable names
   - Redeploy after adding new variables

3. **Build failures:**
   - Check build logs in Netlify
   - Ensure all dependencies are in `package.json`

4. **API not responding:**
   - Check your backend logs
   - Verify the URL is correct
   - Test the API directly

## 📞 Support

If you encounter issues:
1. Check the deployment logs
2. Verify all environment variables are set
3. Test the API endpoints directly
4. Check the browser console for frontend errors

## 🎉 Success!

Once deployed, you'll have:
- A beautiful React frontend at `https://your-app.netlify.app`
- A powerful Python backend API
- Real-time ticket monitoring and notifications!

Happy ticket hunting! 🎟️ 