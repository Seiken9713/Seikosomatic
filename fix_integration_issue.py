#!/usr/bin/env python3
"""
Discord Bot Integration Fix
Generates a proper invite link with all required permissions to fix "unknown integration" errors.
"""

import json

def generate_invite_link():
    """Generate a proper invite link with all required permissions."""
    
    # Load bot client ID from config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    client_id = config['client_id']
    
    # Calculate permissions value for all required bot permissions
    permissions = (
        0x0000000000000001 |  # Create Instant Invite
        0x0000000000000002 |  # Kick Members
        0x0000000000000004 |  # Ban Members
        0x0000000000000008 |  # Administrator (optional, but useful)
        0x0000000000000010 |  # Manage Channels
        0x0000000000000020 |  # Manage Guild
        0x0000000000000040 |  # Add Reactions
        0x0000000000000400 |  # View Channels
        0x0000000000000800 |  # Send Messages
        0x0000000000001000 |  # Send TTS Messages
        0x0000000000002000 |  # Manage Messages
        0x0000000000004000 |  # Embed Links
        0x0000000000008000 |  # Attach Files
        0x0000000000010000 |  # Read Message History
        0x0000000000020000 |  # Mention Everyone
        0x0000000000040000 |  # Use External Emojis
        0x0000000000080000 |  # View Guild Insights
        0x0000000000100000 |  # Connect (Voice)
        0x0000000000200000 |  # Speak (Voice)
        0x0000000000400000 |  # Mute Members (Voice)
        0x0000000000800000 |  # Deafen Members (Voice)
        0x0000000001000000 |  # Move Members (Voice)
        0x0000000002000000 |  # Use Voice Activity
        0x0000000004000000 |  # Change Nickname
        0x0000000008000000 |  # Manage Nicknames
        0x0000000010000000 |  # Manage Roles
        0x0000000020000000 |  # Manage Webhooks
        0x0000000040000000 |  # Manage Guild Expressions
        0x0000000080000000 |  # Use Application Commands (CRITICAL for slash commands)
        0x0000000100000000 |  # Request to Speak
        0x0000000200000000 |  # Manage Events
        0x0000000400000000 |  # Manage Threads
        0x0000000800000000 |  # Create Public Threads
        0x0000001000000000 |  # Create Private Threads
        0x0000002000000000 |  # Use External Stickers
        0x0000004000000000 |  # Send Messages in Threads
        0x0000008000000000 |  # Use Embedded Activities
        0x0000010000000000    # Moderate Members (Timeout)
    )
    
    # Generate the invite URL with proper scopes and permissions
    invite_url = (
        f"https://discord.com/api/oauth2/authorize?"
        f"client_id={client_id}&"
        f"permissions={permissions}&"
        f"scope=bot%20applications.commands"
    )
    
    print("=" * 60)
    print("DISCORD BOT INTEGRATION FIX")
    print("=" * 60)
    print(f"Bot Client ID: {client_id}")
    print(f"Permissions Value: {permissions}")
    print()
    print("IMPORTANT: Use this invite link to re-invite the bot:")
    print(invite_url)
    print()
    print("This link includes:")
    print("- bot scope (for basic bot functionality)")
    print("- applications.commands scope (for slash commands)")
    print("- All necessary permissions including 'Use Application Commands'")
    print()
    print("After re-inviting, slash commands should work without 'unknown integration' errors.")
    print("=" * 60)
    
    return invite_url

if __name__ == "__main__":
    generate_invite_link()