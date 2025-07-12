"""
Discord Moderation Bot - Main Entry Point
A modular Discord bot for server moderation with extensible architecture.
"""

import discord
from discord.ext import commands
import asyncio
import json
import logging
import os
from datetime import datetime

from utils.optimization import PerformanceMonitor, CacheManager
from utils.db_manager import db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/bot_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ModerationBot(commands.Bot):
    """Main bot class with initialization and configuration loading."""
    
    def __init__(self):
        # Load configuration
        self.config = self.load_config()
        
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.moderation = True
        intents.presences = True  # Required for presence/activity status logging
        intents.dm_messages = True  # Enable DM message processing
        intents.guild_messages = True  # Enable guild message processing
        
        # Initialize bot with prefix and intents (custom help command will be added by help cog)
        super().__init__(
            command_prefix=self.config['prefix'],
            intents=intents,
            help_command=None
        )
        
        # Enable slash command error handling
        self.tree.on_error = self.on_app_command_error
        
        # Web server will be managed by run.py for deployment
        
    def load_config(self):
        """Load configuration from config.json file."""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            logger.info("Configuration loaded successfully")
            return config
        except FileNotFoundError:
            logger.error("config.json not found. Using default configuration.")
            return {
                "prefix": "!",
                "log_channel": None,
                "mute_role": "Muted",
                "max_warnings": 3,
                "auto_mod": {
                    "enabled": False,
                    "spam_threshold": 5,
                    "spam_interval": 10
                }
            }
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config.json: {e}")
            return {}
    
    async def setup_hook(self):
        """Load all cogs and initialize database when bot starts up."""
        # Initialize database
        try:
            await db.initialize()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            # Continue without database for now, some features may not work
        
        cogs = [
            'cogs.accessibility',
            'cogs.help',
            'cogs.moderation',
            'cogs.logging',
            'cogs.utility',
            'cogs.emoji',
            'cogs.interactive',
            'cogs.reaction_roles',
            'cogs.snipe',
            'cogs.afk',
            'cogs.auto_role',
            'cogs.starboard',
            'cogs.bot_status',
            'cogs.rss_feeds',
            'cogs.welcome_images',
            'cogs.welcome_animations',
            'cogs.automod',
            'cogs.reminders',
            'cogs.user_app',
            'cogs.ping_user'
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
                logger.info(f"Loaded cog: {cog}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog}: {e}")
        
        # Sync slash commands to Discord
        try:
            # Sync globally - let Discord handle duplicates naturally
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} slash commands globally to Discord")
                    
        except Exception as e:
            logger.error(f"Failed to sync slash commands: {e}")
            # Try guild-specific sync as fallback only if global sync fails
            for guild in self.guilds:
                try:
                    guild_synced = await self.tree.sync(guild=guild)
                    logger.info(f"Fallback: Synced {len(guild_synced)} commands to guild {guild.name}")
                    break  # Only sync to one guild as fallback
                except Exception as fallback_e:
                    logger.error(f"Fallback sync failed for guild {guild.name}: {fallback_e}")
        
        # Web server management delegated to run.py for proper deployment handling
        logger.info("All cogs loaded successfully. Web server will be managed by run.py.")
    
    async def on_ready(self):
        """Event triggered when bot is ready and connected."""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')
        
        # Set bot activity
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{self.config['prefix']}help | Moderating servers"
        )
        await self.change_presence(activity=activity)
    
    async def on_message(self, message):
        """Process messages and commands, including DMs."""
        # Debug: Log all message reception
        logger.info(f"Message received from {message.author} in {'DM' if message.guild is None else message.guild.name}: {message.content[:50]}...")
        
        # Ignore bot messages
        if message.author.bot:
            logger.debug(f"Ignoring bot message from {message.author}")
            return
        
        # Log command attempts
        if message.content.startswith('!'):
            logger.info(f"Command detected: {message.content}")
            
        # Log DM messages for debugging
        if message.guild is None:
            logger.info(f"DM received from {message.author}: {message.content}")
            # Additional debug info for DMs
            if message.content.startswith('!'):
                logger.info(f"DM command detected, processing: {message.content}")
        
        # Process commands
        try:
            logger.info(f"About to process command: {message.content}")
            await self.process_commands(message)
            logger.info(f"Finished processing command: {message.content}")
        except Exception as e:
            logger.error(f"Error processing command {message.content}: {e}")
            raise
    
    async def on_disconnect(self):
        """Event triggered when bot disconnects."""
        logger.warning("Bot has disconnected from Discord")
    
    async def on_resumed(self):
        """Event triggered when bot resumes connection."""
        logger.info("Bot connection resumed")
    
    async def on_command_error(self, ctx, error):
        """Global error handler for commands."""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore command not found errors
        
        elif isinstance(error, commands.MissingPermissions):
            return  # Silently ignore permission errors - don't respond at all
        
        elif isinstance(error, commands.CheckFailure):
            return  # Silently ignore check failures - don't respond at all
        
        elif isinstance(error, commands.BotMissingPermissions):
            # Only respond if user has permission to use the command at all
            if await self._user_has_basic_permissions(ctx):
                await ctx.send("❌ I don't have the required permissions to execute this command.")
        
        elif isinstance(error, commands.MissingRequiredArgument):
            # Only respond if user has permission to use the command at all
            if await self._user_has_basic_permissions(ctx):
                await ctx.send(f"❌ Missing required argument: {error.param}")
        
        elif isinstance(error, commands.BadArgument):
            # Only respond if user has permission to use the command at all
            if await self._user_has_basic_permissions(ctx):
                await ctx.send("❌ Invalid argument provided.")
        
        elif isinstance(error, commands.CommandOnCooldown):
            # Only respond if user has permission to use the command at all
            if await self._user_has_basic_permissions(ctx):
                await ctx.send(f"❌ Command is on cooldown. Try again in {error.retry_after:.2f} seconds.")
        
        else:
            # Log all errors but only respond if user has permissions
            logger.error(f"Unhandled error in command {ctx.command}: {error}")
            if await self._user_has_basic_permissions(ctx):
                await ctx.send("❌ An unexpected error occurred. Please try again later.")
    

    
    async def _user_has_basic_permissions(self, ctx):
        """Check if user has any permissions to use bot commands."""
        # DM context - allow all commands
        if ctx.guild is None:
            return True
        
        # Server owner and bot owner always have permissions
        if ctx.author == ctx.guild.owner or await self.is_owner(ctx.author):
            return True
        
        # Define safe commands that anyone can use
        safe_commands = [
            'help', 'ping', 'serverinfo', 'si', 'userinfo', 'ui', 'avatar', 
            'botinfo', 'invite', 'afk', 'unafk', 'afklist', 'snipe', 'editsnipe', 
            'snipelist', 'emojiinfo', 'listemojis', 'button', 'buttonstats',
            'purge'
        ]
        
        # Allow everyone to use safe commands
        if ctx.command and ctx.command.name in safe_commands:
            return True
        
        # For moderation/administrative commands, check permissions
        if (ctx.author.guild_permissions.administrator or
            ctx.author.guild_permissions.kick_members or
            ctx.author.guild_permissions.ban_members or
            ctx.author.guild_permissions.manage_messages or
            ctx.author.guild_permissions.moderate_members or
            ctx.author.guild_permissions.manage_guild or
            ctx.author.guild_permissions.manage_roles):
            return True
        
        # Check role-based permissions from config
        mod_roles = self.config.get('permissions', {}).get('moderator_roles', [])
        admin_roles = self.config.get('permissions', {}).get('admin_roles', [])
        
        user_roles = [role.name for role in ctx.author.roles]
        
        return any(role in user_roles for role in mod_roles + admin_roles)
    
    async def on_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        """Handle slash command errors."""
        logger.error(f"Slash command error in {interaction.command}: {error}")
        logger.error(f"Error type: {type(error)}")
        logger.error(f"User: {interaction.user}, Guild: {interaction.guild}")
        
        try:
            if isinstance(error, discord.app_commands.CommandOnCooldown):
                await interaction.response.send_message(
                    f"❌ Command is on cooldown. Try again in {error.retry_after:.2f} seconds.",
                    ephemeral=True
                )
            elif isinstance(error, discord.app_commands.MissingPermissions):
                logger.warning(f"Permission error for user {interaction.user} in command {interaction.command}")
                # Silently ignore permission errors
                if not interaction.response.is_done():
                    await interaction.response.defer(ephemeral=True)
            else:
                logger.error(f"Unexpected slash command error: {error}")
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"❌ An error occurred: {str(error)}",
                        ephemeral=True
                    )
        except Exception as e:
            logger.error(f"Error in error handler: {e}")

async def main():
    """Main function to run the bot with reconnection logic."""
    # Get Discord token from environment
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        logger.error("DISCORD_TOKEN environment variable not found!")
        return
    
    # Create bot instance
    bot = ModerationBot()
    
    # Connection retry logic
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            logger.info(f"Starting bot (attempt {retry_count + 1}/{max_retries})")
            await bot.start(token)
            break  # If successful, break out of retry loop
            
        except discord.LoginFailure:
            logger.error("Invalid Discord token provided!")
            break  # Don't retry on auth failure
            
        except discord.ConnectionClosed:
            retry_count += 1
            logger.warning(f"Connection closed, retrying in 5 seconds... ({retry_count}/{max_retries})")
            if retry_count < max_retries:
                await asyncio.sleep(5)
            
        except discord.HTTPException as e:
            if e.status == 429:  # Rate limited
                retry_count += 1
                logger.warning(f"Rate limited, retrying in 10 seconds... ({retry_count}/{max_retries})")
                if retry_count < max_retries:
                    await asyncio.sleep(10)
            else:
                logger.error(f"HTTP error: {e}")
                break
                
        except Exception as e:
            retry_count += 1
            logger.error(f"Unexpected error: {e}")
            if retry_count < max_retries:
                logger.info(f"Retrying in 5 seconds... ({retry_count}/{max_retries})")
                await asyncio.sleep(5)
            else:
                logger.error("Max retries reached, giving up")
                break
    
    # Cleanup
    if not bot.is_closed():
        await bot.close()

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Run the bot with proper signal handling
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
