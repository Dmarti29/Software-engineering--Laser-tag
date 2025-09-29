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

### Get the code
run this to ensure you have git
sudo apt update
sudo apt install -y git
git --version


Clone the repository (choose one):

**HTTPS**
```bash
git clone https://github.com/dmarti29/Software-engineering--Laser-tag.git
cd Software-engineering--Laser-tag

## Quick Start Guide
This guide assumes you're using a pre-provisioned virtual machine that already has Python and the PostgreSQL database set up.

### Running the Application

1. Navigate to the project directory:

```bash
cd /path/to/Software-engineering--Laser-tag
```

2. Start the backend server:

```bash
python3 -m backend.server
```

3. Open a new terminal and cd back into the same directory Software-engineering-Laser-tag

```bash
python3 main.py
```



## Notes & troubleshooting


```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```

- If you want to run the frontend from another machine, change the backend base URL in `frontend/api/client.py` (`base_url`) to point to the VM's IP address and open firewall rules accordingly.


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
