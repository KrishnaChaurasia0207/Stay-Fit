# 🍽️ Multi-Agent Nutrition System - Quick Start Guide

## 🚀 Easy Execution

Run the nutrition system with a single command:

```bash
python run.py
```

This will present you with a simple menu to choose how you want to run the system:

1. **Interactive Nutrition System** - Provide your personal data for personalized meal planning
2. **Demo System** - Experience the system with sample data
3. **Run Tests** - Verify that all system components work correctly
4. **System Information** - Learn about the system architecture
5. **Start Backend API Server** - Launch the FastAPI backend for external integration
6. **Run End-to-End Scenarios** - Demonstrate various meal planning use cases
7. **Exit** - Close the application

## 🎯 What Each Option Does

### Option 1: Interactive Nutrition System
- **Personalized**: Takes your real personal data and health metrics
- **Complete**: Full multi-agent system with real-time adaptation
- **Interactive**: You provide all the information needed for your personalized plan

### Option 2: Demo System
- **Sample Data**: Uses predefined user profiles for demonstration
- **Quick**: No input required, see results immediately
- **Educational**: Shows how the system works with different scenarios

### Option 3: Run Tests
- **Comprehensive**: Runs all 15 system tests
- **Verification**: Confirms all components work correctly
- **Debugging**: Helps identify any issues with the system

### Option 4: System Information
- Learn about the system architecture
- Understand the technology stack
- See what makes this system special

### Option 5: Start Backend API Server
- **FastAPI Backend**: Production-ready REST API
- **External Integration**: Connect other applications to the nutrition engine
- **Documentation**: Auto-generated API docs at http://localhost:8000/docs
- **Real-time**: Handles multiple requests with async support

### Option 6: Run End-to-End Scenarios
- **Use Cases**: Demonstrates 4 different meal planning scenarios
- **Real-world**: Shows how the system handles various user types
- **API Testing**: Verifies the backend API functionality

### Option 7: Exit
- Close the application gracefully

## 🌐 Backend API Server

The system includes a production-ready FastAPI backend that can be used for external integration.

### Starting the Server
```bash
python start_backend.py
```

Or use the menu option (Option 5) which provides the same functionality.

### API Endpoints
- **GET /** - Health check
- **GET /health-check** - Comprehensive system health check
- **GET /foods** - Retrieve all foods in the database
- **POST /meal-plan** - Generate personalized meal plans

### API Documentation
Once the server is running, visit http://localhost:8000/docs for interactive API documentation.

## 🧪 End-to-End Scenarios

The end-to-end scenarios demonstrate various real-world use cases:

1. **Basic Meal Planning** - Standard healthy adult
2. **Diabetic Patient** - Meal planning with glucose monitoring
3. **Athlete Training** - High-protein requirements
4. **Budget-Conscious Student** - Cost-optimized meal planning

Run these scenarios using Option 6 in the menu or directly with:
```bash
python end_to_end_scenarios.py
```

## 📋 How It Works

### Personal Data Input
The system asks for:
- Basic information (name, age, sex, weight, height)
- Activity level
- Dietary preferences and restrictions
- Budget constraints
- Health concerns

### Nutritionally Optimal Output
The system provides:
- Personalized daily calorie and macronutrient targets
- Complete meal plans with breakfast, lunch, and dinner
- Detailed nutrition breakdowns
- Cost estimates
- Real-time adaptations when needed
- Shopping lists for meal preparation

## ✅ System Status

All 15 tests are passing, confirming the system is working correctly:
- ✅ Core imports
- ✅ Agent messaging
- ✅ Nutrition database
- ✅ Data validation
- ✅ Meal optimization
- ✅ Adaptation logic
- ✅ Food filtering
- ✅ Genetic analysis
- ✅ Biometric analysis
- ✅ Async operations

## 🎉 Ready to Use

The system is production-ready and suitable for public release as requested. You can now run the complete nutrition system with just one simple command!