#!/usr/bin/env python3
"""
Script to systematically remove duplicate prefix commands that have slash equivalents
"""

import os
import re

def remove_duplicate_commands():
    """Remove duplicate prefix commands from all cogs"""
    
    # Commands to remove (prefix versions that have slash equivalents)
    commands_to_remove = [
        # Interactive commands
        ('interactive.py', 'buttoncolor'),
        
        # Emoji commands 
        ('emoji.py', 'steal'),
        
        # Ticket commands
        ('tickets.py', 'ticketpanel'),
        ('tickets.py', 'closeticket'),
        
        # Starboard commands
        ('starboard.py', 'starboard'),
        
        # Reaction role commands
        ('reaction_roles.py', 'reactionrole'),
        
        # Reminder commands
        ('reminders.py', 'remind'),
        ('reminders.py', 'reminders'),
        
        # Utility commands
        ('utility.py', 'ping'),
        
        # Ping user commands
        ('ping_user.py', 'pinguser'),
        ('ping_user.py', 'finduserid'),
        
        # Snipe commands
        ('snipe.py', 'snipe'),
        
        # Help commands
        ('help.py', 'about'),
        
        # Auto role commands
        ('auto_role.py', 'autorole'),
    ]
    
    print("=== Removing Duplicate Commands ===")
    
    for filename, command_name in commands_to_remove:
        filepath = f"cogs/{filename}"
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Find the command definition
                pattern = rf'@commands\.command\(name=\'{command_name}\'\).*?(?=\n    @|\n\nclass|\Z)'
                
                # Use more specific patterns for some commands
                if command_name == 'buttoncolor':
                    pattern = rf'@commands\.command\(name=\'buttoncolor\'.*?(?=\n    @app_commands\.command|\n    def _|\nclass|\Z)'
                elif command_name == 'steal':
                    pattern = rf'@commands\.command\(name=\'steal\'.*?(?=\n    @app_commands\.command|\n    def _|\nclass|\Z)'
                
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    # Remove the command
                    new_content = content.replace(match.group(0), '')
                    
                    # Write back the modified content
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    
                    print(f"✅ Removed !{command_name} from {filename}")
                else:
                    print(f"❌ Could not find !{command_name} in {filename}")
                    
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")
        else:
            print(f"❌ File not found: {filepath}")
    
    print("\n=== Command Removal Complete ===")

if __name__ == "__main__":
    remove_duplicate_commands()