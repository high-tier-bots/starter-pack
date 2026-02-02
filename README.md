# HighTierBots - Bot Starter Pack

## 📋 Overview

HighTierBots is a Telegram bot framework built with Pyrogram and Flask. It provides a modular structure for building scalable Telegram bots with database integration.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- MongoDB (for database)
- Telegram Bot Token (from BotFather)

### Installation & Local Start

#### Option 1: Using Start Script (Recommended)

**Windows:**
```bash
start-local.bat
```

**Linux/macOS:**
```bash
bash start-local.sh
```

#### Option 2: Manual Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**

   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

   **Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env` file and update with your credentials:
     - `API_ID`: Telegram API ID
     - `API_HASH`: Telegram API Hash
     - `BOT_TOKEN`: Your bot token from BotFather
     - `DB_URI`: MongoDB connection URI
     - `DB_NAME`: Database name
     - `OWNER_ID`: Your Telegram user ID
     - `LOG_GROUP_ID`: (Optional) Log group chat ID

5. **Run the application:**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
Explain folder sturcture here
```

## ⚙️ Configuration

### Environment Variables (.env)

```env
API_ID=your_api_id
API_HASH=your_api_hash
LOG_GROUP_ID=your_log_group_id
BOT_TOKEN=your_bot_token
DB_URI=mongodb://localhost:27017
DB_NAME=hightier_bots
OWNER_ID=your_user_id
```

## 🐳 Docker Deployment

### Build Docker Image:
```bash
docker build -t hightier-bots .
```

### Run Docker Container:
```bash
docker run -v $(pwd):/app -e API_ID=<id> -e API_HASH=<hash> -e BOT_TOKEN=<token> hightier-bots
```

The Docker container automatically restarts when files change (hot-reload).

## 📚 Features

- ✅ Modular bot handler system
- ✅ MongoDB database integration
- ✅ Flask API endpoint for health checks
- ✅ Advanced logging system
- ✅ Docker containerization with hot-reload
- ✅ Environment-based configuration

## 🔧 Main Components

### main.py
Entry point of the application that initializes:
- Flask server for health checks
- Pyrogram bot client
- Database connection
- Bot command registration

### handlers/
Contains all bot command handlers and message processors

### database.py
Manages MongoDB connections and database operations

### config.py
Loads and validates environment variables

### logger.py
Configures application logging

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Development

For local development, use the start scripts provided. The application includes:
- Hot-reload support in Docker
- Comprehensive logging
- Easy handler module structure

## 📞 Support

For issues or questions, please create an issue in the repository.