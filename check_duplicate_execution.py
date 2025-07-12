#!/usr/bin/env python3
"""
Duplicate Execution Detection Script
Adds debug logging to all commands to detect duplicate execution issues
"""

import os
import re
import ast

def add_debug_logging_to_commands():
    """Add debug logging to all command functions in all cogs"""
    
    cog_files = []
    for file in os.listdir('cogs'):
        if file.endswith('.py') and not file.startswith('__'):
            cog_files.append(os.path.join('cogs', file))
    
    results = {}
    
    for filepath in cog_files:
        print(f"\nProcessing {filepath}...")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if logger is imported
            has_logger_import = 'import logging' in content
            has_logger_instance = 'logger = logging.getLogger(__name__)' in content
            
            # Find all command functions
            command_pattern = r'@commands\.command\([^)]*\)\s*(?:@[^\n]*\s*)*async def (\w+)\(self, ctx'
            commands_found = re.findall(command_pattern, content, re.MULTILINE)
            
            # Find all slash commands
            slash_pattern = r'@app_commands\.command\([^)]*\)\s*(?:@[^\n]*\s*)*async def (\w+)\(self, interaction'
            slash_commands_found = re.findall(slash_pattern, content, re.MULTILINE)
            
            results[filepath] = {
                'has_logger_import': has_logger_import,
                'has_logger_instance': has_logger_instance,
                'prefix_commands': commands_found,
                'slash_commands': slash_commands_found,
                'total_commands': len(commands_found) + len(slash_commands_found)
            }
            
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            results[filepath] = {'error': str(e)}
    
    return results

def generate_logging_patches():
    """Generate patches to add logging to commands that don't have it"""
    
    # Files that already have debug logging added
    files_with_logging = ['cogs/auto_role.py']
    
    patches = []
    results = add_debug_logging_to_commands()
    
    for filepath, data in results.items():
        if 'error' in data:
            continue
            
        if filepath in files_with_logging:
            print(f"Skipping {filepath} - already has logging")
            continue
            
        if data['total_commands'] > 0:
            patches.append({
                'file': filepath,
                'needs_logger_import': not data['has_logger_import'],
                'needs_logger_instance': not data['has_logger_instance'],
                'commands': data['prefix_commands'] + data['slash_commands']
            })
    
    return patches

def main():
    """Main function to analyze and report on duplicate execution potential"""
    
    print("=== Duplicate Execution Detection Analysis ===\n")
    
    results = add_debug_logging_to_commands()
    
    # Summary report
    total_files = len(results)
    total_commands = sum(data.get('total_commands', 0) for data in results.values() if 'error' not in data)
    
    print(f"Analyzed {total_files} cog files")
    print(f"Found {total_commands} total commands")
    
    # Detailed breakdown
    print("\n=== Per-File Breakdown ===")
    for filepath, data in results.items():
        if 'error' in data:
            print(f"{filepath}: ERROR - {data['error']}")
            continue
            
        print(f"\n{filepath}:")
        print(f"  - Logger imported: {data['has_logger_import']}")
        print(f"  - Logger instance: {data['has_logger_instance']}")
        print(f"  - Prefix commands ({len(data['prefix_commands'])}): {', '.join(data['prefix_commands'])}")
        print(f"  - Slash commands ({len(data['slash_commands'])}): {', '.join(data['slash_commands'])}")
    
    # Generate patches for missing logging
    patches = generate_logging_patches()
    
    print(f"\n=== Files Needing Debug Logging ({len(patches)} files) ===")
    for patch in patches:
        print(f"\n{patch['file']}:")
        print(f"  - Needs logger import: {patch['needs_logger_import']}")
        print(f"  - Needs logger instance: {patch['needs_logger_instance']}")
        print(f"  - Commands to patch: {', '.join(patch['commands'])}")
    
    return patches

if __name__ == "__main__":
    patches = main()