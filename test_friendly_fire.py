#!/usr/bin/env python3
"""
Friendly Fire Test Script
Tests the friendly fire detection logic in the backend server.

Usage:
    python test_friendly_fire.py

This script simulates UDP messages to test:
1. Red team hitting Red team (FRIENDLY FIRE) - Both players lose 10 points
2. Green team hitting Green team (FRIENDLY FIRE) - Both players lose 10 points
3. Red team hitting Green team (VALID HIT) - Shooter gains 10 points
4. Green team hitting Red team (VALID HIT) - Shooter gains 10 points
"""

import socket
import time
import sys
import requests

# Configuration
UDP_PORT = 7501  # Backend receive port
API_PORT = 5000  # Backend API port
HOST = '127.0.0.1'
API_URL = f'http://{HOST}:{API_PORT}'

def send_udp_message(message):
    """Send a UDP message to the backend server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode(), (HOST, UDP_PORT))
        sock.close()
        return True
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def get_all_scores():
    """Fetch all player scores from the backend API"""
    try:
        response = requests.get(f'{API_URL}/scores', timeout=2)
        if response.status_code == 200:
            return response.json().get('scores', {})
        else:
            print(f"⚠️  Failed to get scores: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️  Could not fetch scores: {e}")
        return None

def display_scores():
    """Display current player scores"""
    scores = get_all_scores()
    if scores:
        print("\n" + "="*60)
        print("CURRENT PLAYER SCORES")
        print("="*60)
        
        # Separate by team
        red_scores = {pid: score for pid, score in scores.items() if int(pid) % 2 == 0}
        green_scores = {pid: score for pid, score in scores.items() if int(pid) % 2 == 1}
        
        print("\n🔴 RED TEAM:")
        if red_scores:
            for pid, score in sorted(red_scores.items(), key=lambda x: int(x[0])):
                print(f"   Player {pid}: {score:+d} points")
        else:
            print("   No players scored yet")
        
        print("\n🟢 GREEN TEAM:")
        if green_scores:
            for pid, score in sorted(green_scores.items(), key=lambda x: int(x[0])):
                print(f"   Player {pid}: {score:+d} points")
        else:
            print("   No players scored yet")
        
        print("\n" + "="*60 + "\n")
    else:
        print("\n⚠️  Unable to retrieve scores (backend may not be running)\n")

def run_tests():
    """Run friendly fire test scenarios"""
    
    print("=" * 60)
    print("FRIENDLY FIRE TEST SUITE")
    print("=" * 60)
    print(f"Target: {HOST}:{UDP_PORT}")
    print("Make sure the backend server is running!")
    print("=" * 60)
    print()
    
    # Wait for user confirmation
    input("Press ENTER to start tests (make sure backend is running)...")
    print()
    
    test_cases = [
        # Format: (message, description, expected_result)
        ("2:4", "Red player (ID 2) hits Red player (ID 4)", "FRIENDLY FIRE"),
        ("1:3", "Green player (ID 1) hits Green player (ID 3)", "FRIENDLY FIRE"),
        ("2:1", "Red player (ID 2) hits Green player (ID 1)", "VALID HIT"),
        ("1:2", "Green player (ID 1) hits Red player (ID 2)", "VALID HIT"),
        ("6:8", "Red player (ID 6) hits Red player (ID 8)", "FRIENDLY FIRE"),
        ("5:7", "Green player (ID 5) hits Green player (ID 7)", "FRIENDLY FIRE"),
        ("10:11", "Red player (ID 10) hits Green player (ID 11)", "VALID HIT"),
        ("11:10", "Green player (ID 11) hits Red player (ID 10)", "VALID HIT"),
    ]
    
    print("Running test scenarios...")
    print()
    
    for i, (message, description, expected) in enumerate(test_cases, 1):
        print(f"Test {i}/{len(test_cases)}: {description}")
        print(f"  Message: '{message}'")
        print(f"  Expected: {expected}")
        
        if send_udp_message(message):
            print(f"  ✓ Message sent successfully")
        else:
            print(f"  ✗ Failed to send message")
        
        print()
        time.sleep(0.5)  # Small delay between tests
    
    print("=" * 60)
    print("TESTS COMPLETE")
    print("=" * 60)
    print()
    
    # Wait a moment for backend to process
    time.sleep(1)
    
    # Display final scores
    display_scores()
    
    print("Check the backend server logs to verify:")
    print("  - FRIENDLY FIRE warnings for same-team hits (both players -10)")
    print("  - Normal info logs for enemy hits (+10 to shooter)")
    print("  - Score updates after each hit")
    print()
    print("Backend log location: server.log or terminal output")

def test_base_scoring():
    """Test base scoring (bonus test)"""
    print()
    print("=" * 60)
    print("BONUS: BASE SCORING TEST")
    print("=" * 60)
    print()
    
    input("Press ENTER to test base scoring...")
    print()
    
    base_tests = [
        ("53", "Red base scored (ID 53)"),
        ("43", "Green base scored (ID 43)"),
    ]
    
    for message, description in base_tests:
        print(f"Test: {description}")
        print(f"  Message: '{message}'")
        
        if send_udp_message(message):
            print(f"  ✓ Message sent successfully")
        else:
            print(f"  ✗ Failed to send message")
        
        print()
        time.sleep(0.5)
    
    print("Check backend logs for base scoring messages")
    print()

if __name__ == "__main__":
    print()
    print("╔════════════════════════════════════════════════════════╗")
    print("║        PHOTON LASER TAG - FRIENDLY FIRE TESTER        ║")
    print("╔════════════════════════════════════════════════════════╗")
    print()
    
    try:
        run_tests()
        
        # Ask if user wants to test base scoring too
        response = input("Run base scoring tests? (y/n): ").strip().lower()
        if response == 'y':
            test_base_scoring()
        
        print()
        print("✓ All tests completed successfully!")
        print()
        
    except KeyboardInterrupt:
        print()
        print("Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ Test error: {e}")
        sys.exit(1)
