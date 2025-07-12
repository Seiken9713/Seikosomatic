#!/usr/bin/env python3
"""
Update Help Systems Script
Comprehensively updates all help guides, menus, and command lists after duplicate removal
"""

import re
import os
import json

def get_current_commands():
    """Extract current command structure from all cogs"""
    
    commands = {
        'prefix': {},
        'slash': {},
        'total_count': 0
    }
    
    cog_files = []
    for file in os.listdir('cogs'):
        if file.endswith('.py') and not file.startswith('__'):
            cog_files.append(os.path.join('cogs', file))
    
    for filepath in cog_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cog_name = os.path.basename(filepath).replace('.py', '')
            commands['prefix'][cog_name] = []
            commands['slash'][cog_name] = []
            
            # Find prefix commands
            prefix_pattern = r'@commands\.command\([^)]*name=[\'"]([^\'"]+)[\'"][^)]*\)\s*(?:@[^\n]*\s*)*async def (\w+)'
            prefix_matches = re.findall(prefix_pattern, content, re.MULTILINE)
            
            for cmd_name, func_name in prefix_matches:
                commands['prefix'][cog_name].append(cmd_name)
            
            # Find slash commands
            slash_pattern = r'@app_commands\.command\([^)]*name=[\'"]([^\'"]+)[\'"][^)]*\)\s*(?:@[^\n]*\s*)*async def (\w+)'
            slash_matches = re.findall(slash_pattern, content, re.MULTILINE)
            
            for cmd_name, func_name in slash_matches:
                commands['slash'][cog_name].append(cmd_name)
            
            commands['total_count'] += len(prefix_matches) + len(slash_matches)
            
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    return commands

def generate_command_categories():
    """Generate organized command categories for help system"""
    
    categories = {
        'Core Management': [
            '!help', '/help', '!commands', '!about', '/listallcommands',
            '!kick', '!ban', '!timeout', '!warn', '!unban', '!untimeout',
            '!warnings', '!clearwarning', '!purge', '!modsetup',
            '/ungag', '/gaglist'
        ],
        'Community Features': [
            '/afk', '/afklist', '/afkclean', '/afksetup',
            '!autorole', '!autoroletest', '!autorolesetup', '!welcomemsg',
            '!reactionrole', '!reactionrolesetup', '!toggleremove',
            '!starboard', '!starboardsetup'
        ],
        'Engagement & Fun': [
            '!button', '/button', '!buttonstats', '!resetbutton', '!removebutton',
            '!globalbuttonstats', '!interactivesetup',
            '!steal', '!emojiinfo', '!listemojis', '!emojisetup',
            '!snipe', '/snipe', '!snipeedit', '!snipelist', '!snipesetup'
        ],
        'Utilities & Tools': [
            '!serverinfo', '/serverinfo', '!ping', '/ping', '!botinfo', '/botinfo',
            '!userinfo', '!avatar', '!invite',
            '/ticketpanel', '/closeticket', '!listtickets', '!ticketstats', '!ticketsetup',
            '/pinguser', '/finduserid', '!pinguserhelp'
        ],
        'System Configuration': [
            '!logchannel', '!removelog', '!logstatus', '!loggingsetup',
            '!botstatus', '!botpresence', '!statuspresets', '!statussetup',
            '!rssfeed', '!rsssetup',
            '!welcomeimages', '!welcomeimagesetup', '!testwelcome',
            '!automod', '!infractions', '!automodsetup',
            '/accessibility', '/accessibilitytest'
        ]
    }
    
    return categories

def update_help_cog():
    """Update the help cog with current command structure"""
    
    commands = get_current_commands()
    categories = generate_command_categories()
    
    # Calculate total commands
    total_prefix = sum(len(cmds) for cmds in commands['prefix'].values())
    total_slash = sum(len(cmds) for cmds in commands['slash'].values())
    total_commands = total_prefix + total_slash
    
    print(f"Found {total_commands} total commands ({total_prefix} prefix, {total_slash} slash)")
    
    # Update the list_all_commands_slash function
    with open('cogs/help.py', 'r') as f:
        content = f.read()
    
    # Find and update the command listing section
    new_command_listing = f'''
    @app_commands.command(name="listallcommands", description="List all available bot commands with their types")
    @app_commands.default_permissions(send_messages=True)
    async def list_all_commands_slash(self, interaction: discord.Interaction):
        """Slash command to list all available commands with indicators."""
        
        embed = discord.Embed(
            title="📋 Complete Command List",
            description=f"All {total_commands} available bot commands\\n\\n"
                       "**Format Legend:**\\n"
                       "`!command` - Prefix command only\\n"
                       "`/command` - Slash command only\\n"
                       "`!command` or `/command` - Available as both",
            color=discord.Color.blue()
        )
        
        categories = {{
            "🛡️ Core Management": [
                "!help or /help", "!commands", "!about or /about", "/listallcommands",
                "!kick", "!ban", "!timeout", "!warn", "!unban", "!untimeout",
                "!warnings", "!clearwarning", "!purge", "!modsetup",
                "/ungag", "/gaglist"
            ],
            "🏠 Community Features": [
                "/afk", "/afklist", "/afkclean", "/afksetup",
                "!autorole", "!autoroletest", "!autorolesetup", "!welcomemsg",
                "!reactionrole", "!reactionrolesetup", "!toggleremove",
                "!starboard", "!starboardsetup"
            ],
            "🎮 Engagement & Fun": [
                "!button or /button", "!buttonstats", "!resetbutton", "!removebutton",
                "!globalbuttonstats", "!interactivesetup",
                "!steal", "!emojiinfo", "!listemojis", "!emojisetup",
                "!snipe or /snipe", "!snipeedit", "!snipelist", "!snipesetup"
            ],
            "🔧 Utilities & Tools": [
                "!serverinfo or /serverinfo", "!ping or /ping", "!botinfo or /botinfo",
                "!userinfo", "!avatar", "!invite",
                "/ticketpanel", "/closeticket", "!listtickets", "!ticketstats", "!ticketsetup",
                "/pinguser", "/finduserid", "!pinguserhelp"
            ],
            "⚙️ System Configuration": [
                "!logchannel", "!removelog", "!logstatus", "!loggingsetup",
                "!botstatus", "!botpresence", "!statuspresets", "!statussetup",
                "!rssfeed", "!rsssetup",
                "!welcomeimages", "!welcomeimagesetup", "!testwelcome",
                "!automod", "!infractions", "!automodsetup",
                "/accessibility", "/accessibilitytest"
            ]
        }}
        
        for cat_name, cmd_list in categories.items():
            # Split commands into chunks if too long
            if len(cmd_list) > 10:
                mid = len(cmd_list) // 2
                chunk1 = cmd_list[:mid]
                chunk2 = cmd_list[mid:]
                
                embed.add_field(
                    name=f"{cat_name} (Part 1)",
                    value="\\n".join(f"• `{cmd}`" for cmd in chunk1),
                    inline=True
                )
                embed.add_field(
                    name=f"{cat_name} (Part 2)",
                    value="\\n".join(f"• `{cmd}`" for cmd in chunk2),
                    inline=True
                )
                embed.add_field(name="\\u200b", value="\\u200b", inline=True)  # Spacer
            else:
                embed.add_field(
                    name=cat_name,
                    value="\\n".join(f"• `{cmd}`" for cmd in cmd_list),
                    inline=True
                )
        
        embed.add_field(
            name="📊 Command Statistics",
            value=f"**Total Commands:** {total_commands}\\n"
                  f"**Prefix Commands:** {total_prefix}\\n"
                  f"**Slash Commands:** {total_slash}\\n"
                  f"**Categories:** {len(categories)}",
            inline=False
        )
        
        embed.set_footer(text="Use !help <command> or /help to explore specific commands")
        
        await interaction.response.send_message(embed=embed)
    '''
    
    return new_command_listing

def update_category_help():
    """Update help category descriptions"""
    
    categories = {
        'Core Management': 'Essential moderation and administrative commands for server management',
        'Community Features': 'Tools to build and manage your server community',
        'Engagement & Fun': 'Interactive features to keep your community engaged',
        'Utilities & Tools': 'Helpful utility commands and server information tools',
        'System Configuration': 'Advanced configuration and logging systems'
    }
    
    return categories

def main():
    """Main function to update all help systems"""
    
    print("=== Updating Help Systems ===\\n")
    
    # Get current command structure
    commands = get_current_commands()
    
    print("Current Command Structure:")
    for cog, cmds in commands['prefix'].items():
        if cmds:
            print(f"  {cog}: {len(cmds)} prefix commands")
    for cog, cmds in commands['slash'].items():
        if cmds:
            print(f"  {cog}: {len(cmds)} slash commands")
    
    print(f"\\nTotal Commands: {commands['total_count']}")
    
    # Generate updated help content
    new_listing = update_help_cog()
    categories = update_category_help()
    
    print("\\n✅ Help system analysis complete!")
    print("\\nNext steps:")
    print("1. Update help.py with new command listings")
    print("2. Update setup guides in all cogs")
    print("3. Verify all help menus are accurate")
    
    return {
        'commands': commands,
        'new_listing': new_listing,
        'categories': categories
    }

if __name__ == "__main__":
    result = main()