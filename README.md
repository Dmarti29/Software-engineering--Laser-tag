# Photon Laser Tag System

| GitHub Username | Real Name       |
|-----------------|-----------------|
| dmarti29        | Daniel Martinez |
| carloszamora0822| Carlos Zamora   |
| imjustruby      | Ruby Lopez      |
| dorivas03       | Daniel Rivas    |
| bsaenz          | Brian Saenz     |


## Complete Installation Guide (Step by Step)

### Step 1: Clone the Repository
```bash
# Install git if you don't have it
sudo apt-get update
sudo apt-get install -y git

# Clone the repository
git clone https://github.com/Dmarti29/Software-engineering--Laser-tag.git
cd Software-engineering--Laser-tag
```

### Step 2: Run Installation Script
```bash
# Make the install script executable
chmod +x install.sh

# Run the install script (this will install all required packages)
sudo ./install.sh
```

### Step 3: Set Up Database
```bash
# Make the database setup script executable
chmod +x setup_db.sh

# Run the database setup
./setup_db.sh
```

### Step 4: Run the Application
You need two terminal windows open:

Terminal 1 (Backend Server):
```bash
PYTHONPATH=/home/student/Software-engineering--Laser-tag python3 backend/server.py
```

Terminal 2 (Frontend GUI):
```bash
PYTHONPATH=/home/student/Software-engineering--Laser-tag python3 main.py
```

### Troubleshooting

1. If you see "Address already in use" error:
   - Just ignore it, the server will still work

2. If you see database connection errors:
   - Make sure PostgreSQL is running:
   ```bash
   sudo systemctl start postgresql
   ```

3. If you see "No module found" errors:
   - Make sure you ran the install script with sudo
   - Make sure you're using PYTHONPATH as shown above

4. If the GUI doesn't show:
   - Make sure you installed python3-tk (the install script should have done this)
   - Try running: `sudo apt-get install python3-tk`

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
