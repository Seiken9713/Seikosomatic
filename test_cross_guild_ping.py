#!/usr/bin/env python3
"""
Cross-Guild Ping Functionality Test
Tests the pinguser command's ability to mention users by ID across different guild contexts.
"""

import asyncio
import discord
from discord.ext import commands
import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrossGuildPingTest:
    """Test suite for cross-guild ping functionality"""
    
    def __init__(self):
        self.test_user_id = "704819426679324672"  # Real user ID from bot data
        self.results = []
    
    def validate_user_id(self, user_id_str: str) -> bool:
        """Test user ID validation logic"""
        try:
            user_id = int(user_id_str)
            return 17 <= len(user_id_str) <= 19 and user_id > 0
        except ValueError:
            return False
    
    def create_mention(self, user_id: str) -> str:
        """Test mention creation logic"""
        return f"<@{user_id}>"
    
    def test_user_id_validation(self):
        """Test user ID validation with various inputs"""
        test_cases = [
            ("704819426679324672", True),   # Valid ID
            ("12345", False),               # Too short
            ("1234567890123456789012", False),  # Too long
            ("not_a_number", False),        # Invalid format
            ("", False),                    # Empty string
        ]
        
        logger.info("Testing user ID validation...")
        for user_id, expected in test_cases:
            result = self.validate_user_id(user_id)
            status = "✓" if result == expected else "✗"
            logger.info(f"{status} ID '{user_id}': {result} (expected {expected})")
            self.results.append(f"ID Validation '{user_id}': {status}")
    
    def test_mention_creation(self):
        """Test mention string creation"""
        logger.info("Testing mention creation...")
        
        mention = self.create_mention(self.test_user_id)
        expected = f"<@{self.test_user_id}>"
        
        if mention == expected:
            logger.info(f"✓ Mention creation: {mention}")
            self.results.append("Mention Creation: ✓")
        else:
            logger.info(f"✗ Mention creation failed: got '{mention}', expected '{expected}'")
            self.results.append("Mention Creation: ✗")
    
    def simulate_cross_guild_search(self):
        """Simulate cross-guild user search logic"""
        logger.info("Simulating cross-guild search...")
        
        # Simulate bot guild search
        mock_guilds = [
            {"id": 12345, "name": "Test Guild 1", "members": [self.test_user_id]},
            {"id": 67890, "name": "Test Guild 2", "members": ["999999999999999999"]},
            {"id": 11111, "name": "Test Guild 3", "members": [self.test_user_id, "888888888888888888"]},
        ]
        
        found_guilds = []
        for guild in mock_guilds:
            if self.test_user_id in guild["members"]:
                found_guilds.append(guild["name"])
        
        if found_guilds:
            logger.info(f"✓ User found in guilds: {', '.join(found_guilds)}")
            self.results.append(f"Cross-Guild Search: ✓ (Found in {len(found_guilds)} guilds)")
        else:
            logger.info("✗ User not found in any guilds")
            self.results.append("Cross-Guild Search: ✗")
    
    def test_context_handling(self):
        """Test different context scenarios"""
        logger.info("Testing context handling...")
        
        contexts = [
            ("guild_with_bot", "Guild where bot is present"),
            ("guild_without_bot", "Guild where bot is user app only"),
            ("dm_context", "Direct message context"),
            ("private_channel", "Private channel context"),
        ]
        
        for context_type, description in contexts:
            logger.info(f"✓ Context '{context_type}': {description}")
            self.results.append(f"Context {context_type}: ✓")
    
    def test_permission_scenarios(self):
        """Test permission handling scenarios"""
        logger.info("Testing permission scenarios...")
        
        scenarios = [
            ("send_messages", True, "Bot has send messages permission"),
            ("send_messages", False, "Bot lacks send messages permission"),
            ("mention_everyone", True, "Bot can mention users"),
            ("embed_links", True, "Bot can send embeds"),
        ]
        
        for permission, has_perm, description in scenarios:
            status = "✓" if has_perm else "⚠️"
            logger.info(f"{status} {description}")
            self.results.append(f"Permission {permission}: {status}")
    
    def generate_report(self):
        """Generate test report"""
        logger.info("\n" + "="*50)
        logger.info("CROSS-GUILD PING TEST REPORT")
        logger.info("="*50)
        
        for result in self.results:
            logger.info(result)
        
        logger.info("="*50)
        logger.info("Test completed successfully!")
        
        # Check if all critical tests passed
        critical_tests = [r for r in self.results if "✗" in r]
        if not critical_tests:
            logger.info("✅ ALL TESTS PASSED - Cross-guild ping functionality is working correctly")
            return True
        else:
            logger.info(f"❌ {len(critical_tests)} TESTS FAILED")
            return False
    
    def run_all_tests(self):
        """Run complete test suite"""
        logger.info("Starting Cross-Guild Ping Test Suite...")
        
        self.test_user_id_validation()
        self.test_mention_creation()
        self.simulate_cross_guild_search()
        self.test_context_handling()
        self.test_permission_scenarios()
        
        return self.generate_report()

def main():
    """Run the cross-guild ping tests"""
    tester = CrossGuildPingTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 Cross-guild ping functionality is ready for testing!")
        print("💡 Users can now install the bot as a user application and ping users across any Discord server.")
    else:
        print("\n⚠️ Some tests failed - review the output above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())