# 📱 Mobile App Setup Guide

## Quick Start

### For Windows Users:
1. **Double-click** `start_mobile.bat` or run `start_mobile.ps1` in PowerShell
2. **Open your phone's browser** and go to the IP address shown in the terminal
3. **Add to Home Screen** for a native app experience

### For Mac/Linux Users:
1. **Run** `chmod +x start_mobile.sh && ./start_mobile.sh`
2. **Open your phone's browser** and go to the IP address shown in the terminal
3. **Add to Home Screen** for a native app experience

## Requirements

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Same WiFi network** for your computer and phone

## Features

✅ **Progressive Web App (PWA)** - Install like a native app  
✅ **Real-time nutrition analysis** - Powered by Python ML engine  
✅ **Personalized meal plans** - Based on your profile and biometrics  
✅ **Mobile-optimized UI** - Touch-friendly interface  
✅ **Offline capability** - Works without internet (cached data)  

## Troubleshooting

### Can't access from phone?
- Make sure your computer and phone are on the same WiFi network
- Check if your firewall is blocking ports 3000 and 8000
- Try the IP address manually: http://YOUR_IP:3000

### Backend errors?
- Install Python dependencies: `pip install -r requirements.txt`
- Check if port 8000 is available
- Look for error messages in the terminal

### Frontend errors?
- Install Node.js dependencies: `cd frontend && npm install`
- Check if port 3000 is available
- Clear browser cache and reload

## Manual Setup

If the automated scripts don't work, you can start manually:

### 1. Start Backend
```bash
pip install -r requirements.txt
python app.py
```

### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Access on Mobile
Open `http://YOUR_COMPUTER_IP:3000` on your phone

## PWA Installation

1. Open the app in your phone's browser
2. Look for "Add to Home Screen" or "Install App" option
3. Follow the prompts to install
4. The app will appear on your home screen like a native app

## Docker Alternative (Optional)

If you prefer Docker:

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access on mobile
# http://YOUR_COMPUTER_IP:3000
```

## API Documentation

Once running, visit `http://YOUR_COMPUTER_IP:8000/docs` to see the complete API documentation.

## Support

- Check logs in the terminal for error messages
- Ensure all dependencies are installed
- Verify network connectivity between devices