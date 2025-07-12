#!/usr/bin/env python3
"""
Production startup script for Discord Bot
Ensures proper startup order and environment handling for deployment
"""

import os
import sys
import asyncio
import logging
import signal

# Configure basic logging for startup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def check_environment():
    """Check if required environment variables are set."""
    required_vars = ['DISCORD_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
        logger.info("You'll need to set your Discord bot token to run the bot.")
        return False
    
    return True

def setup_directories():
    """Create necessary directories."""
    directories = ['logs', 'data']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")

async def main():
    """Main entry point that starts both Discord bot and web server."""
    from main import ModerationBot
    from web_server import BotWebServer
    
    # Get Discord token from environment
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        logger.error("DISCORD_TOKEN environment variable not found!")
        return
    
    # Create bot instance
    bot = ModerationBot()
    
    # Start web server first for health checks
    web_server = BotWebServer(bot)
    port = int(os.getenv('PORT', 5000))
    
    try:
        # Start web server
        web_runner = await web_server.start_server(host='0.0.0.0', port=port)
        logger.info(f"Web server started on port {port} for health checks")
        
        # Connection retry logic for Discord bot
        max_retries = 5
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                logger.info(f"Starting Discord bot (attempt {retry_count + 1}/{max_retries})")
                await bot.start(token)
                break  # If successful, break out of retry loop
                
            except Exception as e:
                retry_count += 1
                logger.warning(f"Bot connection failed: {e}. Retrying in 5 seconds... ({retry_count}/{max_retries})")
                if retry_count < max_retries:
                    await asyncio.sleep(5)
                else:
                    logger.error("Max retries exceeded. Bot startup failed.")
                    
    except Exception as e:
        logger.error(f"Fatal error during startup: {e}")
        raise

if __name__ == "__main__":
    logger.info("Starting Discord Bot deployment...")
    
    # Check environment
    if not check_environment():
        logger.error("Environment check failed. Exiting.")
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Set default port if not specified
    if not os.getenv('PORT'):
        os.environ['PORT'] = '5000'
    
    logger.info("Environment checks passed. Starting bot and web server...")
    
    try:
        # Run the main bot function
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error during bot startup: {e}")
        sys.exit(1)