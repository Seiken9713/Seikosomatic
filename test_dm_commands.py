#!/usr/bin/env python3
"""
DM Commands Testing Utility
Tests all DM-related commands to ensure proper functionality.
"""

import asyncio
import json
import os
from datetime import datetime

# Test data structure for DM commands
DM_COMMANDS = {
    "Basic Commands": [
        "!help",
        "!ping", 
        "!testdm",
        "!dmtest"
    ],
    "DM Gag System": [
        "!dmgag",
        "!dmgag Testing the gag system",
        "!dmgagstatus",
        "!dmungag",
        "!globaldmgag",
        "!globaldmgag Testing global gag"
    ],
    "Utility Commands": [
        "!purge 5",
        "!purgedm 3"
    ]
}

def test_dm_commands_list():
    """Generate a comprehensive test report for DM commands."""
    
    print("🔍 DM COMMANDS TESTING REPORT")
    print("=" * 50)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    total_commands = 0
    
    for category, commands in DM_COMMANDS.items():
        print(f"📂 {category}")
        print("-" * 30)
        
        for cmd in commands:
            print(f"   {cmd}")
            total_commands += 1
        
        print()
    
    print(f"📊 Summary: {total_commands} DM commands available for testing")
    print()
    
    print("🧪 TESTING INSTRUCTIONS:")
    print("1. Send these commands as DMs to the bot")
    print("2. Verify each command responds correctly")
    print("3. Check for any error messages or timeouts")
    print("4. Test both successful and error scenarios")
    print()
    
    print("🔧 EXPECTED BEHAVIORS:")
    print("✅ Basic commands should respond with helpful information")
    print("✅ DM gag commands should work in DMs only")
    print("✅ Purge commands should delete specified number of messages")
    print("✅ Help command should show DM-specific help")
    print("✅ Status commands should show current bot status")
    print()
    
    print("⚠️  KNOWN LIMITATIONS:")
    print("• Slash commands don't work in DMs (Discord limitation)")
    print("• Some commands may require specific permissions")
    print("• Rate limiting may apply to rapid command usage")
    
    return True

def check_dm_configuration():
    """Check if DM commands are properly configured."""
    
    print("\n🔧 DM CONFIGURATION CHECK")
    print("=" * 40)
    
    # Check if config has proper DM settings
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        print("✅ Configuration file loaded successfully")
        print(f"✅ Bot prefix: {config.get('prefix', 'Not set')}")
        
        # Check for any DM-specific settings
        if 'dm_settings' in config:
            print(f"✅ DM settings found: {config['dm_settings']}")
        else:
            print("ℹ️  No specific DM settings (using defaults)")
            
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
    
    # Check if data directory exists for DM gag storage
    if os.path.exists('data'):
        print("✅ Data directory exists for DM gag storage")
        
        # Check for DM gag files
        dm_gag_file = 'data/dm_gagged_users.json'
        if os.path.exists(dm_gag_file):
            print("✅ DM gag data file exists")
            try:
                with open(dm_gag_file, 'r') as f:
                    gag_data = json.load(f)
                print(f"ℹ️  Current DM gags: {len(gag_data)} users")
            except:
                print("⚠️  DM gag file exists but couldn't read it")
        else:
            print("ℹ️  No DM gag data file (will be created when needed)")
    else:
        print("⚠️  Data directory doesn't exist")
    
    print()

def generate_dm_test_script():
    """Generate a test script for manual DM testing."""
    
    test_script = """
DM TESTING SCRIPT
================

Copy and paste these commands one by one as DMs to the bot:

1. Basic Functionality Test:
   !dmtest
   !testdm
   !help
   !ping

2. DM Gag System Test:
   !dmgagstatus
   !dmgag Testing DM gag functionality
   Hello world (should be scrambled if contains R)
   Test message without the forbidden letter (should work normally)
   !dmgagstatus
   !dmungag
   !dmgagstatus

3. Utility Commands Test:
   !purge 2
   !purgedm 1

4. Error Handling Test:
   !nonexistentcommand
   !dmgag
   !purge 999

Expected Results:
- All valid commands should respond
- Invalid commands should be ignored
- DM gag should scramble messages with R
- Purge should delete specified messages
- Status commands should show current state
"""
    
    print(test_script)

if __name__ == "__main__":
    print("🤖 Discord Bot DM Commands Testing Utility")
    print("=" * 60)
    
    # Run all tests
    test_dm_commands_list()
    check_dm_configuration()
    generate_dm_test_script()
    
    print("\n✨ Testing utility complete!")
    print("Now test the commands manually by DMing the bot.")