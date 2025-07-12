#!/usr/bin/env python3
"""
Script to find and remove duplicate commands causing double messaging
"""

import os
import re
import json
from collections import defaultdict

def analyze_cog_commands(filepath):
    """Analyze a cog file to find duplicate commands."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find all command definitions
    prefix_commands = []
    slash_commands = []
    
    # Patterns to match command definitions
    prefix_pattern = r'@commands\.command\([^)]*name=[\'"]([^\'"]+)[\'"]'
    prefix_def_pattern = r'@commands\.command\(\)\s*\n\s*async def (\w+)'
    slash_pattern = r'@app_commands\.command\([^)]*name=[\'"]([^\'"]+)[\'"]'
    slash_def_pattern = r'@app_commands\.command\(\)\s*\n\s*async def (\w+)'
    
    # Find prefix commands
    prefix_matches = re.findall(prefix_pattern, content)
    prefix_def_matches = re.findall(prefix_def_pattern, content, re.MULTILINE)
    
    # Find slash commands  
    slash_matches = re.findall(slash_pattern, content)
    slash_def_matches = re.findall(slash_def_pattern, content, re.MULTILINE)
    
    all_prefix = set(prefix_matches + prefix_def_matches)
    all_slash = set(slash_matches + slash_def_matches)
    
    # Find duplicates
    duplicates = all_prefix & all_slash
    
    return {
        'file': filepath,
        'prefix_only': all_prefix - duplicates,
        'slash_only': all_slash - duplicates,
        'duplicates': duplicates
    }

def main():
    """Main analysis function."""
    print("=== Discord Bot Double Messaging Analysis ===\n")
    
    cogs_dir = "cogs"
    total_duplicates = 0
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(cogs_dir, filename)
            analysis = analyze_cog_commands(filepath)
            
            if analysis['duplicates']:
                total_duplicates += len(analysis['duplicates'])
                print(f"🔍 {filename}:")
                print(f"   Duplicate commands: {list(analysis['duplicates'])}")
                print(f"   Prefix only: {list(analysis['prefix_only'])}")
                print(f"   Slash only: {list(analysis['slash_only'])}")
                print()
    
    print(f"📊 Total duplicate commands found: {total_duplicates}")
    
    if total_duplicates > 0:
        print("\n⚠️  These duplicate commands are likely causing double messaging!")
        print("💡 Recommendation: Remove prefix commands that have slash equivalents")

if __name__ == "__main__":
    main()