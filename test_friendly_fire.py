#!/usr/bin/env python3
"""
Friendly Fire Test Script
Tests the friendly fire detection logic in the backend server.

Usage:
    python test_friendly_fire.py

This script simulates UDP messages to test:
1. Red team hitting Red team (FRIENDLY FIRE)
2. Green team hitting Green team (FRIENDLY FIRE)
3. Red team hitting Green team (VALID HIT)
4. Green team hitting Red team (VALID HIT)
"""

import socket
import time
import sys

# Configuration
UDP_PORT = 7501  # Backend receive port
HOST = '127.0.0.1'

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
    print("Check the backend server logs to verify:")
    print("  - FRIENDLY FIRE warnings for same-team hits")
    print("  - Normal info logs for enemy hits")
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
