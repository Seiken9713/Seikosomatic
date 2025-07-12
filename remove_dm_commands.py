#!/usr/bin/env python3
"""
Script to remove all DM-related commands from moderation.py
"""

import re

def remove_dm_commands():
    # Read the moderation.py file
    with open('cogs/moderation.py', 'r') as f:
        content = f.read()
    
    # Define patterns for DM commands to remove
    dm_command_patterns = [
        r'@commands\.command\(name=["\']testdm["\']\).*?(?=@|async def setup|$)',
        r'@commands\.command\(name=["\']dmtest["\']\).*?(?=@|async def setup|$)',
        r'@commands\.command\(name=["\']purgedm["\']\).*?(?=@|async def setup|$)',
        r'@commands\.command\(name=["\']dmgag["\']\).*?(?=@|async def setup|$)',
        r'@commands\.command\(name=["\']dmungag["\']\).*?(?=@|async def setup|$)',
        r'@commands\.command\(name=["\']dmpurgeconvo["\']\).*?(?=@|async def setup|$)',
        r'@commands\.command\(name=["\']globaldmgag["\']\).*?(?=@|async def setup|$)',
        r'@commands\.command\(name=["\']dmgagstatus["\']\).*?(?=@|async def setup|$)',
    ]
    
    # Remove each pattern
    for pattern in dm_command_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Clean up excessive empty lines
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    
    # Write back to file
    with open('cogs/moderation.py', 'w') as f:
        f.write(content)
    
    print("Removed all DM commands from moderation.py")

if __name__ == "__main__":
    remove_dm_commands()