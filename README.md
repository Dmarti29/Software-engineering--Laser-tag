# Photon Laser Tag System
````markdown
# Photon Laser Tag System

| GitHub Username | Real Name       |
|-----------------|-----------------|
| dmarti29        | Daniel Martinez |
| carloszamora0822| Carlos Zamora   |
| imjustruby      | Ruby Lopez      |
| dorivas03       | Daniel Rivas    |
| bsaenz          | Brian Saenz     |

## Setup and steps to run on Virtual Machine. Installation steps.

**IMPORTANT: You must run the installation script before running the application!**

### Prerequisites
- Ubuntu/Debian-based Linux system
- sudo access

### Installation Steps

1. **Get the code**
   ```bash
   sudo apt update
   sudo apt install -y git
   git clone https://github.com/dmarti29/Software-engineering--Laser-tag.git
   cd Software-engineering--Laser-tag

Then install the dependencies with this command
sudo ./install.sh

### Running the Application
navigate to    cd Software-engineering--Laser-tag


2. Start the backend server:

python3 -m backend.server


3. Open a new terminal and cd back into the same directory Software-engineering-Laser-tag
   cd Software-engineering--Laser-tag

Then run


python3 main.py


So at this point you should have 2 different terminals open and they should be running both programs


## Notes & troubleshooting





## Features

- Splash screen with company logo
- Player entry system for red and green teams with customizable player IDs
- Database integration for player tracking and ID management
- UDP socket communication for equipment IDs
- Network configuration for UDP broadcasting
- Game start/stop controls


## Architecture

### Frontend

- `frontend/splashscreen.py`: Initial splash screen
- `frontend/player_entry/`: Player registration components
   - `player_entry_component.py`: Main UI component
   - `player_teams/`: Team-specific implementations

### Backend

- `backend/server.py`: Flask server with API endpoints
- `backend/database.py`: Database interaction layer
- `backend/config.py`: Configuration settings

````

## Running the Application

The application consists of a backend server and a frontend GUI. You need to run both in separate terminals:

1. Start the backend server:
```bash
PYTHONPATH=/home/student/Software-engineering--Laser-tag python3 backend/server.py
```

2. In a new terminal, start the frontend:
```bash
PYTHONPATH=/home/student/Software-engineering--Laser-tag python3 main.py
```

The frontend should open with:
- A splash screen showing the company logo
- Then the main interface with red and green team sections
- Network settings at the bottom
- Game control buttons

## Network Configuration

### Monitoring UDP Traffic

To monitor UDP broadcasts on port 7500:

```bash
sudo tcpdump -i lo -n udp port 7500 -X
```

To check open ports:

```bash
ss -tulpn
```

## Architecture

### Frontend

- `frontend/splashscreen.py`: Initial splash screen
- `frontend/player_entry/`: Player registration components
  - `player_entry_component.py`: Main UI component
  - `player_teams/`: Team-specific implementations

### Backend

- `backend/server.py`: Flask server with API endpoints
- `backend/database.py`: Database interaction layer
- `backend/config.py`: Configuration settings

student@photon:~/Software-engineering--Laser-tag$ python3 test_friendly_fire.py

╔════════════════════════════════════════════════════════╗
║        PHOTON LASER TAG - FRIENDLY FIRE TESTER        ║
╔════════════════════════════════════════════════════════╗

============================================================
FRIENDLY FIRE TEST SUITE
============================================================
Target: 127.0.0.1:7501
Make sure the backend server is running!
============================================================

Press ENTER to start tests (make sure backend is running)...

Running test scenarios...

Test 1/8: Red player (ID 2) hits Red player (ID 4)
  Message: '2:4'
  Expected: FRIENDLY FIRE
  ✓ Message sent successfully

Test 2/8: Green player (ID 1) hits Green player (ID 3)
  Message: '1:3'
  Expected: FRIENDLY FIRE
  ✓ Message sent successfully

Test 3/8: Red player (ID 2) hits Green player (ID 1)
  Message: '2:1'
  Expected: VALID HIT
  ✓ Message sent successfully

Test 4/8: Green player (ID 1) hits Red player (ID 2)
  Message: '1:2'
  Expected: VALID HIT
  ✓ Message sent successfully

Test 5/8: Red player (ID 6) hits Red player (ID 8)
  Message: '6:8'
  Expected: FRIENDLY FIRE
  ✓ Message sent successfully

Test 6/8: Green player (ID 5) hits Green player (ID 7)
  Message: '5:7'
  Expected: FRIENDLY FIRE
  ✓ Message sent successfully

Test 7/8: Red player (ID 10) hits Green player (ID 11)
  Message: '10:11'
  Expected: VALID HIT
  ✓ Message sent successfully

Test 8/8: Green player (ID 11) hits Red player (ID 10)
  Message: '11:10'
  Expected: VALID HIT
  ✓ Message sent successfully

============================================================
TESTS COMPLETE
============================================================


============================================================
CURRENT PLAYER SCORES
============================================================

🔴 RED TEAM:
   Player 2: +0 points
   Player 4: -10 points
   Player 6: -10 points
   Player 8: -10 points
   Player 10: +10 points

🟢 GREEN TEAM:
   Player 1: +0 points
   Player 3: -10 points
   Player 5: -10 points
   Player 7: -10 points
   Player 11: +10 points

============================================================

Check the backend server logs to verify:
  - FRIENDLY FIRE warnings for same-team hits (both players -10)
  - Normal info logs for enemy hits (+10 to shooter)
  - Score updates after each hit

Backend log location: server.log or terminal output
Run base scoring tests? (y/n): y

============================================================
BONUS: BASE SCORING TEST
============================================================

Press ENTER to test base scoring...

Test: Red base scored (ID 53)
  Message: '53'
  ✓ Message sent successfully



