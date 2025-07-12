#!/usr/bin/env python3
"""
Setup script for Discord Bot CI/CD pipeline
Helps configure GitHub Actions and automated deployments
"""

import json
import os
import subprocess
import sys

def check_git_repo():
    """Check if we're in a git repository"""
    try:
        subprocess.run(['git', 'status'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_git_remote():
    """Get the GitHub repository URL"""
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def create_readme():
    """Create a basic README if it doesn't exist"""
    if not os.path.exists('README.md'):
        readme_content = """# Discord Moderation Bot

A comprehensive Discord moderation and community management bot with advanced features.

## Features

- 🛡️ **Moderation**: Kick, ban, timeout, and warning system
- 🤖 **AutoMod**: Automated spam detection and content filtering
- 🎭 **Reaction Roles**: Automatic role assignment via reactions
- 📝 **Logging**: Comprehensive server event logging
- 🎮 **Interactive**: Custom buttons and engagement features
- 📢 **Welcome System**: Animated welcome messages and auto-roles
- ⭐ **Starboard**: Highlight popular messages
- 🔕 **AFK System**: Away status with automatic responses
- 📰 **RSS Feeds**: Automated news and update feeds
- ⏰ **Reminders**: Personal and server reminders
- 🔧 **Utility**: Server info, ping, and management tools

## Setup

1. Create a Discord application and bot at https://discord.com/developers/applications
2. Get your bot token and add it to `config.json`
3. Invite the bot to your server with appropriate permissions
4. Configure the bot settings in `config.json`
5. Run the bot with `python run.py`

## Deployment

This bot includes automated CI/CD with GitHub Actions. See `deployment-guide.md` for setup instructions.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python debug_corruption_scan.py`
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
"""
        with open('README.md', 'w') as f:
            f.write(readme_content)
        print("✅ Created README.md")

def create_license():
    """Create an MIT license file"""
    if not os.path.exists('LICENSE'):
        license_content = """MIT License

Copyright (c) 2025 Discord Bot Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        with open('LICENSE', 'w') as f:
            f.write(license_content)
        print("✅ Created LICENSE file")

def check_config():
    """Check if config.json exists and has required structure"""
    if not os.path.exists('config.json'):
        print("❌ config.json not found")
        return False
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        required_keys = ['bot_token', 'guild_id', 'admin_role_id', 'moderator_role_id']
        missing = [key for key in required_keys if key not in config]
        
        if missing:
            print(f"❌ Missing config keys: {missing}")
            return False
        
        print("✅ Configuration file is valid")
        return True
    except Exception as e:
        print(f"❌ Error reading config.json: {e}")
        return False

def create_data_gitkeep():
    """Create .gitkeep file in data directory"""
    os.makedirs('data', exist_ok=True)
    gitkeep_path = 'data/.gitkeep'
    if not os.path.exists(gitkeep_path):
        with open(gitkeep_path, 'w') as f:
            f.write("# This file ensures the data directory is tracked by git\n")
        print("✅ Created data/.gitkeep")

def install_dev_dependencies():
    """Install development dependencies for code quality"""
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 
                       'black', 'isort', 'flake8', 'bandit'], check=True)
        print("✅ Installed development dependencies")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install development dependencies")
        return False

def format_code():
    """Format code with black and isort"""
    try:
        print("🔧 Formatting code with black...")
        subprocess.run([sys.executable, '-m', 'black', '.'], check=True)
        
        print("🔧 Sorting imports with isort...")
        subprocess.run([sys.executable, '-m', 'isort', '.'], check=True)
        
        print("✅ Code formatting completed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Code formatting failed")
        return False

def run_quality_checks():
    """Run code quality checks"""
    print("🔍 Running code quality checks...")
    
    # Syntax check
    try:
        subprocess.run([sys.executable, '-m', 'py_compile', 'main.py'], check=True)
        subprocess.run([sys.executable, '-m', 'py_compile', 'run.py'], check=True)
        print("✅ Syntax check passed")
    except subprocess.CalledProcessError:
        print("❌ Syntax check failed")
        return False
    
    # Corruption scan
    if os.path.exists('debug_corruption_scan.py'):
        try:
            subprocess.run([sys.executable, 'debug_corruption_scan.py'], check=True)
            print("✅ Corruption scan passed")
        except subprocess.CalledProcessError:
            print("❌ Corruption scan found issues")
            return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Discord Bot CI/CD Setup")
    print("=" * 40)
    
    # Check if git repository
    if not check_git_repo():
        print("❌ This is not a git repository. Please run 'git init' first.")
        return
    
    # Get repository info
    remote_url = get_git_remote()
    if remote_url:
        print(f"📂 Repository: {remote_url}")
    
    # Create necessary files
    create_readme()
    create_license()
    create_data_gitkeep()
    
    # Check configuration
    config_valid = check_config()
    
    # Install and run development tools
    if install_dev_dependencies():
        format_code()
        run_quality_checks()
    
    # Final instructions
    print("\n" + "=" * 40)
    print("🎉 CI/CD Setup Complete!")
    print("\nNext steps:")
    print("1. Push your code to GitHub")
    print("2. Go to repository Settings > Secrets and variables > Actions")
    print("3. Add these secrets:")
    print("   - REPLIT_TOKEN (get from https://replit.com/account)")
    print("   - REPLIT_REPL_ID (your @username/repl-name)")
    print("   - DISCORD_WEBHOOK (optional, for notifications)")
    print("4. Read deployment-guide.md for detailed instructions")
    
    if not config_valid:
        print("\n⚠️ Warning: Fix config.json before deploying")

if __name__ == "__main__":
    main()