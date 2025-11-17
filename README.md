# Photon Laser Tag System

| GitHub Username | Real Name       |
|-----------------|-----------------|
| dmarti29        | Daniel Martinez |
| carloszamora0822| Carlos Zamora   |
| imjustruby      | Ruby Lopez      |
| dorivas03       | Daniel Rivas    |
| bsaenz          | Brian Saenz     |

## Installation Instructions

**IMPORTANT: You must run the installation script before running the application!**

### Prerequisites
- Ubuntu/Debian-based Linux system
- sudo access

### Installation Steps

1. **Update system and install git:**
   ```bash
   sudo apt update
   sudo apt install -y git
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/dmarti29/Software-engineering--Laser-tag.git
   cd Software-engineering--Laser-tag
   ```

3. **Run the installation script:**
   ```bash
   sudo ./install.sh
   ```

### Running the Application

1. **Start the backend server (in one terminal):**
   ```bash
   cd Software-engineering--Laser-tag
   python3 -m backend.server
   ```

2. **Start the frontend (in another terminal):**
   ```bash
   cd Software-engineering--Laser-tag
   python3 main.py
   ```

You should now have 2 terminals open running both programs.





## Features

- Splash screen with company logo
- Player entry system for red and green teams
- Database integration for player tracking and ID management  
- Real-time scoring with friendly fire detection
- Base scoring (+100 points)
- 30-second pregame countdown with music
- 6-minute gameplay timer
- Team totals and winning team display
- UDP socket communication for equipment IDs
- Network configuration for UDP broadcasting

## Architecture

### Frontend
- `frontend/splashscreen.py`: Initial splash screen
- `frontend/player_entry/`: Player registration components
- `frontend/play_action_screen.py`: Main gameplay display
- `frontend/countdowntimer.py`: Pregame countdown
- `main.py`: Application entry point

### Backend
- `backend/server.py`: Flask server with API endpoints
- `backend/database.py`: Database interaction layer  
- `backend/game_state.py`: Game state management
- `backend/udp_server.py`: UDP communication for equipment

## Project Structure
```
Software-engineering--Laser-tag/
├── backend/               # Backend server code
├── frontend/             # Frontend UI components
├── photon_tracks/        # Game music files
├── install.sh            # Installation script
├── main.py              # Application entry point
└── README.md            # This file
```
