#!/usr/bin/env python3
"""
Fix Duplicate Function Definitions
Systematically remove duplicate function definitions that cause double messaging
"""

import re
import os

def fix_starboard_duplicates():
    """Fix duplicate functions in starboard.py"""
    
    with open('cogs/starboard.py', 'r') as f:
        content = f.read()
    
    # Find the second starboard_setup_guide function (line 555) and remove it
    # We'll look for the pattern and remove the entire duplicate function
    
    # Split into lines to work with line numbers
    lines = content.split('\n')
    
    # Find both occurrences
    first_setup_line = None
    second_setup_line = None
    
    for i, line in enumerate(lines):
        if 'async def starboard_setup_guide(self, ctx):' in line:
            if first_setup_line is None:
                first_setup_line = i
            else:
                second_setup_line = i
                break
    
    if second_setup_line is not None:
        print(f"Found duplicate starboard_setup_guide at line {second_setup_line + 1}")
        
        # Find the end of the second function (look for next function or end of class)
        end_line = len(lines)
        for i in range(second_setup_line + 1, len(lines)):
            if lines[i].strip().startswith('async def ') or lines[i].strip().startswith('def '):
                end_line = i
                break
            elif lines[i].strip() == 'async def setup(bot):':
                end_line = i
                break
        
        # Remove the duplicate function
        new_lines = lines[:second_setup_line] + lines[end_line:]
        new_content = '\n'.join(new_lines)
        
        with open('cogs/starboard.py', 'w') as f:
            f.write(new_content)
        
        print(f"Removed duplicate starboard_setup_guide function (lines {second_setup_line + 1} to {end_line})")
        return True
    
    return False

def fix_snipe_duplicates():
    """Fix duplicate functions in snipe.py"""
    
    with open('cogs/snipe.py', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Find both snipe_edited functions
    first_snipe_line = None
    second_snipe_line = None
    
    for i, line in enumerate(lines):
        if 'async def snipe_edited(self, ctx, index: int = 1):' in line:
            if first_snipe_line is None:
                first_snipe_line = i
            else:
                second_snipe_line = i
                break
    
    if second_snipe_line is not None:
        print(f"Found duplicate snipe_edited at line {second_snipe_line + 1}")
        
        # Find the end of the second function
        end_line = len(lines)
        for i in range(second_snipe_line + 1, len(lines)):
            if (lines[i].strip().startswith('async def ') or 
                lines[i].strip().startswith('def ') or
                lines[i].strip() == 'async def setup(bot):'):
                end_line = i
                break
        
        # Remove the duplicate function
        new_lines = lines[:second_snipe_line] + lines[end_line:]
        new_content = '\n'.join(new_lines)
        
        with open('cogs/snipe.py', 'w') as f:
            f.write(new_content)
        
        print(f"Removed duplicate snipe_edited function (lines {second_snipe_line + 1} to {end_line})")
        return True
    
    return False

def fix_tickets_duplicates():
    """Fix duplicate functions in tickets.py"""
    
    with open('cogs/tickets.py', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Find duplicate list_tickets functions
    first_tickets_line = None
    second_tickets_line = None
    
    for i, line in enumerate(lines):
        if 'async def list_tickets(self, ctx, status: str = \'open\'):' in line:
            if first_tickets_line is None:
                first_tickets_line = i
            else:
                second_tickets_line = i
                break
    
    if second_tickets_line is not None:
        print(f"Found duplicate list_tickets at line {second_tickets_line + 1}")
        
        # Find the end of the second function
        end_line = len(lines)
        for i in range(second_tickets_line + 1, len(lines)):
            if (lines[i].strip().startswith('async def ') or 
                lines[i].strip().startswith('def ') or
                lines[i].strip() == 'async def setup(bot):'):
                end_line = i
                break
        
        # Remove the duplicate function
        new_lines = lines[:second_tickets_line] + lines[end_line:]
        new_content = '\n'.join(new_lines)
        
        with open('cogs/tickets.py', 'w') as f:
            f.write(new_content)
        
        print(f"Removed duplicate list_tickets function (lines {second_tickets_line + 1} to {end_line})")
        return True
    
    return False

def fix_utility_duplicates():
    """Fix duplicate functions in utility.py"""
    
    with open('cogs/utility.py', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Find duplicate invite functions
    first_invite_line = None
    second_invite_line = None
    
    for i, line in enumerate(lines):
        if 'async def invite(self, ctx):' in line:
            if first_invite_line is None:
                first_invite_line = i
            else:
                second_invite_line = i
                break
    
    if second_invite_line is not None:
        print(f"Found duplicate invite at line {second_invite_line + 1}")
        
        # Find the end of the second function
        end_line = len(lines)
        for i in range(second_invite_line + 1, len(lines)):
            if (lines[i].strip().startswith('async def ') or 
                lines[i].strip().startswith('def ') or
                lines[i].strip() == 'async def setup(bot):'):
                end_line = i
                break
        
        # Remove the duplicate function
        new_lines = lines[:second_invite_line] + lines[end_line:]
        new_content = '\n'.join(new_lines)
        
        with open('cogs/utility.py', 'w') as f:
            f.write(new_content)
        
        print(f"Removed duplicate invite function (lines {second_invite_line + 1} to {end_line})")
        return True
    
    return False

def fix_help_duplicates():
    """Fix duplicate functions in help.py"""
    
    with open('cogs/help.py', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Find duplicate command_list functions
    first_command_line = None
    second_command_line = None
    
    for i, line in enumerate(lines):
        if 'async def command_list(self, ctx):' in line:
            if first_command_line is None:
                first_command_line = i
            else:
                second_command_line = i
                break
    
    if second_command_line is not None:
        print(f"Found duplicate command_list at line {second_command_line + 1}")
        
        # Find the end of the second function
        end_line = len(lines)
        for i in range(second_command_line + 1, len(lines)):
            if (lines[i].strip().startswith('async def ') or 
                lines[i].strip().startswith('def ') or
                lines[i].strip() == 'async def setup(bot):'):
                end_line = i
                break
        
        # Remove the duplicate function
        new_lines = lines[:second_command_line] + lines[end_line:]
        new_content = '\n'.join(new_lines)
        
        with open('cogs/help.py', 'w') as f:
            f.write(new_content)
        
        print(f"Removed duplicate command_list function (lines {second_command_line + 1} to {end_line})")
        return True
    
    return False

def fix_pinguser_duplicates():
    """Fix duplicate functions in ping_user.py"""
    
    with open('cogs/ping_user.py', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Find duplicate ping_user_help functions
    first_help_line = None
    second_help_line = None
    
    for i, line in enumerate(lines):
        if 'async def ping_user_help(self, ctx):' in line:
            if first_help_line is None:
                first_help_line = i
            else:
                second_help_line = i
                break
    
    if second_help_line is not None:
        print(f"Found duplicate ping_user_help at line {second_help_line + 1}")
        
        # Find the end of the second function
        end_line = len(lines)
        for i in range(second_help_line + 1, len(lines)):
            if (lines[i].strip().startswith('async def ') or 
                lines[i].strip().startswith('def ') or
                lines[i].strip() == 'async def setup(bot):'):
                end_line = i
                break
        
        # Remove the duplicate function
        new_lines = lines[:second_help_line] + lines[end_line:]
        new_content = '\n'.join(new_lines)
        
        with open('cogs/ping_user.py', 'w') as f:
            f.write(new_content)
        
        print(f"Removed duplicate ping_user_help function (lines {second_help_line + 1} to {end_line})")
        return True
    
    return False

def fix_tickets_setup_duplicates():
    """Fix duplicate ticket_setup_guide functions in tickets.py"""
    
    with open('cogs/tickets.py', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Find duplicate ticket_setup_guide functions
    first_setup_line = None
    second_setup_line = None
    
    for i, line in enumerate(lines):
        if 'async def ticket_setup_guide(self, ctx):' in line:
            if first_setup_line is None:
                first_setup_line = i
            else:
                second_setup_line = i
                break
    
    if second_setup_line is not None:
        print(f"Found duplicate ticket_setup_guide at line {second_setup_line + 1}")
        
        # Find the end of the second function
        end_line = len(lines)
        for i in range(second_setup_line + 1, len(lines)):
            if (lines[i].strip().startswith('async def ') or 
                lines[i].strip().startswith('def ') or
                lines[i].strip() == 'async def setup(bot):'):
                end_line = i
                break
        
        # Remove the duplicate function
        new_lines = lines[:second_setup_line] + lines[end_line:]
        new_content = '\n'.join(new_lines)
        
        with open('cogs/tickets.py', 'w') as f:
            f.write(new_content)
        
        print(f"Removed duplicate ticket_setup_guide function (lines {second_setup_line + 1} to {end_line})")
        return True
    
    return False

def main():
    """Main function to fix all duplicate functions"""
    
    print("=== Fixing Duplicate Function Definitions ===\n")
    
    fixes_made = 0
    
    if fix_starboard_duplicates():
        fixes_made += 1
    
    if fix_snipe_duplicates():
        fixes_made += 1
    
    if fix_tickets_duplicates():
        fixes_made += 1
    
    if fix_utility_duplicates():
        fixes_made += 1
    
    if fix_help_duplicates():
        fixes_made += 1
    
    if fix_pinguser_duplicates():
        fixes_made += 1
    
    if fix_tickets_setup_duplicates():
        fixes_made += 1
    
    print(f"\nCompleted! Made {fixes_made} fixes.")
    
    if fixes_made > 0:
        print("\nRunning verification scan...")
        os.system("python check_duplicate_execution.py")
    
    return fixes_made

if __name__ == "__main__":
    main()