#!/usr/bin/env python3
"""
Command Audit Script
Scans all cogs to identify available commands and their implementation types
"""

import os
import re
import ast

def extract_commands_from_file(filepath):
    """Extract command information from a Python file."""
    commands = {
        'prefix': [],
        'slash': [],
        'both': []
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find prefix commands
        prefix_pattern = r'@commands\.command\([^)]*name=[\'"]([^\'"]+)[\'"]'
        prefix_matches = re.findall(prefix_pattern, content)
        
        # Find prefix commands without explicit name
        prefix_default_pattern = r'@commands\.command\(\)\s*async\s+def\s+(\w+)'
        prefix_default_matches = re.findall(prefix_default_pattern, content)
        
        # Find slash commands
        slash_pattern = r'@app_commands\.command\([^)]*name=[\'"]([^\'"]+)[\'"]'
        slash_matches = re.findall(slash_pattern, content)
        
        # Find slash commands without explicit name
        slash_default_pattern = r'@app_commands\.command\(\)\s*async\s+def\s+(\w+)'
        slash_default_matches = re.findall(slash_default_pattern, content)
        
        # Combine all commands
        all_prefix = set(prefix_matches + prefix_default_matches)
        all_slash = set(slash_matches + slash_default_matches)
        
        # Find commands that exist in both
        both_commands = all_prefix & all_slash
        prefix_only = all_prefix - both_commands
        slash_only = all_slash - both_commands
        
        commands['prefix'] = sorted(list(prefix_only))
        commands['slash'] = sorted(list(slash_only))
        commands['both'] = sorted(list(both_commands))
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    
    return commands

def main():
    """Main audit function."""
    cog_dir = 'cogs'
    all_commands = {}
    
    # Process each cog file
    for filename in os.listdir(cog_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            filepath = os.path.join(cog_dir, filename)
            cog_name = filename[:-3]  # Remove .py extension
            
            commands = extract_commands_from_file(filepath)
            if any(commands.values()):  # Only include cogs with commands
                all_commands[cog_name] = commands
    
    # Generate comprehensive report
    print("=" * 80)
    print("DISCORD BOT COMMAND AUDIT REPORT")
    print("=" * 80)
    
    total_prefix = 0
    total_slash = 0
    total_both = 0
    
    for cog_name, commands in all_commands.items():
        print(f"\n📁 {cog_name.upper()}")
        print("-" * 40)
        
        if commands['prefix']:
            print(f"  🔸 Prefix Only ({len(commands['prefix'])}): {', '.join(commands['prefix'])}")
            total_prefix += len(commands['prefix'])
        
        if commands['slash']:
            print(f"  🔹 Slash Only ({len(commands['slash'])}): {', '.join(commands['slash'])}")
            total_slash += len(commands['slash'])
        
        if commands['both']:
            print(f"  🔶 Both Available ({len(commands['both'])}): {', '.join(commands['both'])}")
            total_both += len(commands['both'])
        
        if not any(commands.values()):
            print("  ⚪ No commands found")
    
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"🔸 Prefix Only Commands: {total_prefix}")
    print(f"🔹 Slash Only Commands: {total_slash}")
    print(f"🔶 Available as Both: {total_both}")
    print(f"📊 Total Unique Commands: {total_prefix + total_slash + total_both}")
    
    # Generate help system recommendations
    print("\n" + "=" * 80)
    print("HELP SYSTEM RECOMMENDATIONS")
    print("=" * 80)
    
    for cog_name, commands in all_commands.items():
        if any(commands.values()):
            print(f"\n{cog_name}:")
            for cmd in commands['prefix']:
                print(f"  !{cmd} - Prefix command")
            for cmd in commands['slash']:
                print(f"  /{cmd} - Slash command")
            for cmd in commands['both']:
                print(f"  !{cmd} or /{cmd} - Available as both")

if __name__ == "__main__":
    main()