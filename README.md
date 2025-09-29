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


## Quick start for a fresh virtual machine (explicit steps)

The project expects the PostgreSQL database and role to be provisioned by the administrator or during VM provisioning. The `setup_db.sh` in this repo is verify-only and will not create users/databases. Follow these exact steps when you log onto a clean Ubuntu/Debian VM.

1) Update the package list and install required system packages

```bash
sudo apt-get update
sudo apt-get install -y git python3 python3-venv python3-pip python3-tk postgresql postgresql-contrib
```

2) Create the PostgreSQL role and database (run as the postgres superuser)

Run these commands to provision the database and role that the app expects. If your environment already has a `student` user and `photon` database, skip this step.

```bash
sudo -u postgres psql -c "CREATE USER student WITH PASSWORD 'student';"
sudo -u postgres psql -c "CREATE DATABASE photon OWNER student;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE photon TO student;"
```

3) Verify PostgreSQL is running and reachable

```bash
sudo systemctl start postgresql
PGPASSWORD=student psql -U student -d photon -h localhost -c "SELECT current_database(), current_user();"
```

4) Clone repository, create and activate a Python virtualenv

```bash
git clone https://github.com/Dmarti29/Software-engineering--Laser-tag.git
cd Software-engineering--Laser-tag
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

5) (Optional) Make helper scripts executable

The repo contains `install.sh` and `setup_db.sh`. `setup_db.sh` currently only verifies connectivity (does not create DB/users). If you want to run them manually:

```bash
chmod +x install.sh setup_db.sh
```

6) Start the backend server

Run the backend as a module from the repository root so Python finds the `backend` package:

```bash
python3 -m backend.server
```

If port 5000 is already in use you'll see an error. To find and stop the process using the port:

```bash
# Find the process using port 5000
sudo lsof -i :5000

# Kill the process (replace <PID> with the process id from the previous command)
sudo kill <PID>
```

7) Start the frontend GUI (in a new terminal with the venv activated)

```bash
python3 main.py
```


### If this VM is already provisioned (no venv, no DB creation)

If the virtual machine you're logging into already has the required Python environment and the `photon` database/user provisioned by your admin (so you do NOT need to create a venv or run any DB setup), follow these minimal steps from the repository root:

1. Ensure you're in the project directory (skip clone if already present):

```bash
cd /path/to/Software-engineering--Laser-tag
```

2. Run the backend server (no venv required if Python and dependencies are already installed):

```bash
python3 -m backend.server
```

3. In another terminal, start the frontend GUI:

```bash
python3 main.py
```

Notes:
- `setup_db.sh` in this repo is verify-only and will not create the database/user. It can be used to check connectivity but is optional on a provisioned VM.
- If the backend is running on a different host than the frontend, update `base_url` in `frontend/api/client.py` to point to the backend host (e.g., `http://VM_IP:5000`).
- If you see port conflicts on 5000, either stop the conflicting process or change the Flask port (I can add an env var/CLI flag if you want).


## Notes & troubleshooting

- The repo intentionally avoids creating DB users/databases automatically. Use the explicit `psql` commands above when provisioning a new VM.
- If you see `ModuleNotFoundError: No module named 'backend'`, ensure you run the server with `python3 -m backend.server` from the project root or set `PYTHONPATH` to the repo root.
- If the backend cannot reach PostgreSQL, ensure the PostgreSQL service is running:

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
