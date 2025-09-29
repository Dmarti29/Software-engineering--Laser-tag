# Photon Laser Tag System

## Project Overview

This project implements a laser tag management system with player entry, game control, and team management features. The system is designed for a laser tag arena where players can register, join teams, and participate in matches.

## Features

- Splash screen with company logo
- Player entry system for red and green teams with customizable player IDs
- Database integration for player tracking and ID management
- UDP socket communication for equipment IDs
- Network configuration for UDP broadcasting
- Game start/stop controls

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database (for production use)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Software-engineering--Laser-tag.git
   cd Software-engineering--Laser-tag
   ```

2. Run the install script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   During installation, you'll be asked if you want to set up the PostgreSQL database.
   If you choose 'yes', the script will automatically run the database setup script.

   Or manually install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Database Setup (Production Only)

For production usage with a real database, you can run the setup script directly:

```bash
chmod +x setup_db.sh
./setup_db.sh
```

This script will create the required PostgreSQL user and database:  
- Username: `student`
- Password: `student`
- Database: `photon`

## Running the Application

### Development Mode

Run the application in development mode (no database required):

```bash
python main.py
```

### Production Mode

When running on a VM with a configured database:

```bash
python main.py
```

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