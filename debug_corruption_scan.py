#!/usr/bin/env python3
"""
Comprehensive Code Corruption Scanner
Scans all Python files for syntax errors, duplicate functions, and corruption issues
"""

import ast
import os
import re
import json
from typing import Dict, List, Tuple, Any

def scan_syntax_errors(filepath: str) -> List[str]:
    """Check for Python syntax errors."""
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
    except SyntaxError as e:
        errors.append(f"Syntax Error: Line {e.lineno}: {e.msg}")
    except Exception as e:
        errors.append(f"Parse Error: {str(e)}")
    return errors

def find_duplicate_functions(filepath: str) -> List[str]:
    """Find duplicate function definitions."""
    duplicates = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all function definitions
        func_pattern = r'^\s*(async\s+)?def\s+(\w+)\s*\('
        functions = re.findall(func_pattern, content, re.MULTILINE)
        func_names = [func[1] for func in functions]
        
        # Check for duplicates
        seen = set()
        for name in func_names:
            if name in seen:
                duplicates.append(f"Duplicate function: {name}")
            seen.add(name)
                
    except Exception as e:
        duplicates.append(f"Error scanning {filepath}: {str(e)}")
    
    return duplicates

def find_duplicate_commands(filepath: str) -> List[str]:
    """Find duplicate command definitions."""
    duplicates = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find prefix commands
        prefix_pattern = r'@commands\.command\([^)]*name=[\'"]([^\'"]+)[\'"][^)]*\)'
        prefix_cmds = re.findall(prefix_pattern, content)
        
        # Find slash commands  
        slash_pattern = r'@app_commands\.command\([^)]*name=[\'"]([^\'"]+)[\'"][^)]*\)'
        slash_cmds = re.findall(slash_pattern, content)
        
        # Check for duplicates within each type
        prefix_seen = set()
        for cmd in prefix_cmds:
            if cmd in prefix_seen:
                duplicates.append(f"Duplicate prefix command: {cmd}")
            prefix_seen.add(cmd)
            
        slash_seen = set()
        for cmd in slash_cmds:
            if cmd in slash_seen:
                duplicates.append(f"Duplicate slash command: {cmd}")
            slash_seen.add(cmd)
                
    except Exception as e:
        duplicates.append(f"Error scanning commands in {filepath}: {str(e)}")
    
    return duplicates

def check_incomplete_code_blocks(filepath: str) -> List[str]:
    """Check for incomplete or corrupted code blocks."""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        in_function = False
        brace_count = 0
        paren_count = 0
        bracket_count = 0
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Track function definitions
            if re.match(r'^\s*(async\s+)?def\s+\w+', line):
                in_function = True
            
            # Count brackets
            brace_count += line.count('{') - line.count('}')
            paren_count += line.count('(') - line.count(')')
            bracket_count += line.count('[') - line.count(']')
            
            # Check for orphaned decorators
            if stripped.startswith('@') and i < len(lines):
                next_line = lines[i].strip() if i < len(lines) else ""
                if not (next_line.startswith('@') or next_line.startswith('def ') or next_line.startswith('async def')):
                    issues.append(f"Line {i}: Orphaned decorator: {stripped}")
            
            # Check for incomplete string literals
            if stripped.count('"') % 2 != 0 or stripped.count("'") % 2 != 0:
                if not stripped.endswith('\\'):  # Not an escaped quote
                    issues.append(f"Line {i}: Incomplete string literal")
        
        # Check final bracket counts
        if brace_count != 0:
            issues.append(f"Mismatched braces: {brace_count} unclosed")
        if paren_count != 0:
            issues.append(f"Mismatched parentheses: {paren_count} unclosed")
        if bracket_count != 0:
            issues.append(f"Mismatched brackets: {bracket_count} unclosed")
            
    except Exception as e:
        issues.append(f"Error checking code blocks: {str(e)}")
    
    return issues

def scan_import_issues(filepath: str) -> List[str]:
    """Check for import-related issues."""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for circular imports (basic check)
        imports = re.findall(r'from\s+(\S+)\s+import|import\s+(\S+)', content)
        
        # Check for unused imports (basic heuristic)
        import_pattern = r'(?:from\s+\S+\s+)?import\s+([^#\n]+)'
        imports_found = re.findall(import_pattern, content)
        
        for import_line in imports_found:
            modules = [m.strip() for m in import_line.split(',')]
            for module in modules:
                # Remove 'as alias' part
                module_name = module.split(' as ')[0].strip()
                if module_name and not re.search(rf'\b{re.escape(module_name)}\b', content.replace(import_line, '')):
                    issues.append(f"Potentially unused import: {module_name}")
                    
    except Exception as e:
        issues.append(f"Error checking imports: {str(e)}")
    
    return issues

def scan_file(filepath: str) -> Dict[str, List[str]]:
    """Comprehensive file scan."""
    results = {
        'syntax_errors': scan_syntax_errors(filepath),
        'duplicate_functions': find_duplicate_functions(filepath),
        'duplicate_commands': find_duplicate_commands(filepath),
        'code_block_issues': check_incomplete_code_blocks(filepath),
        'import_issues': scan_import_issues(filepath)
    }
    return results

def main():
    """Main scanning function."""
    print("=== COMPREHENSIVE CODE CORRUPTION SCAN ===\n")
    
    # Scan all Python files
    python_files = []
    for root, dirs, files in os.walk('.'):
        if 'site-packages' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Scanning {len(python_files)} Python files...\n")
    
    total_issues = 0
    critical_files = []
    
    for filepath in sorted(python_files):
        results = scan_file(filepath)
        
        # Count total issues
        file_issues = sum(len(issues) for issues in results.values())
        total_issues += file_issues
        
        if file_issues > 0:
            critical_files.append((filepath, file_issues))
            print(f"🔍 {filepath}:")
            
            for category, issues in results.items():
                if issues:
                    print(f"  ❌ {category.replace('_', ' ').title()}:")
                    for issue in issues:
                        print(f"    • {issue}")
            print()
    
    # Summary
    print("=== SCAN SUMMARY ===")
    print(f"Total files scanned: {len(python_files)}")
    print(f"Files with issues: {len(critical_files)}")
    print(f"Total issues found: {total_issues}")
    
    if critical_files:
        print("\n🚨 CRITICAL FILES (most issues first):")
        for filepath, issue_count in sorted(critical_files, key=lambda x: x[1], reverse=True):
            print(f"  {filepath}: {issue_count} issues")
    else:
        print("\n✅ NO CORRUPTION DETECTED - All files clean!")
    
    # Check specific bot files
    print("\n=== BOT-SPECIFIC CHECKS ===")
    
    # Check main.py
    if os.path.exists('main.py'):
        print("✓ main.py exists")
    else:
        print("❌ main.py missing")
    
    # Check run.py
    if os.path.exists('run.py'):
        print("✓ run.py exists")
    else:
        print("❌ run.py missing")
    
    # Check config.json
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r') as f:
                json.load(f)
            print("✓ config.json valid")
        except:
            print("❌ config.json corrupted")
    else:
        print("❌ config.json missing")
    
    # Check cogs directory
    cog_files = []
    if os.path.exists('cogs'):
        cog_files = [f for f in os.listdir('cogs') if f.endswith('.py') and not f.startswith('__')]
        print(f"✓ Found {len(cog_files)} cog files")
    else:
        print("❌ cogs directory missing")
    
    return total_issues == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)