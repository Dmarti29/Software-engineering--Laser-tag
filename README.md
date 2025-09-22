# Laser Tag System - Sprint 2

## Team Members
| GitHub Username | Real Name |
|----------------|-----------|
| [danielmartinez] | Daniel Martinez |
| [carlos] | Carlos |
| [ruby] | Ruby |
| [rivas] | Rivas |
| [brian] | Brian |

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Update database settings in config.py
3. Run: `python backend.py`

## Files

### database.py
Handles all database operations for the laser tag system. Connects to PostgreSQL database and manages player data.
- Connects to "photon" database
- Adds new players with ID and codename
- Looks up existing players by ID
- Deletes all players when needed

### backend.py
REST API server that connects the database to the frontend. Also handles UDP networking for game communication.
- Provides web endpoints for adding/getting players
- Sets up UDP sockets on ports 7500 and 7501
- Broadcasts equipment IDs when players are added
- Handles game start/end signals

### config.py
Configuration settings for database connection and game parameters.
- Database connection details
- UDP port numbers
- Game codes and settings

### requirements.txt
List of Python packages needed to run the application.

## Sprint 2 Completed Tasks
- Database connection to PostgreSQL
- Player add/get/delete functionality
- REST API endpoints
- UDP socket setup for networking
- Equipment ID broadcasting
