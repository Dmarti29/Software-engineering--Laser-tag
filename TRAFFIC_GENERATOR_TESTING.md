# Traffic Generator Testing Guide

## Overview
This guide explains how to test the laser tag system using the traffic generator provided by the instructor.

## Setup

### Prerequisites
1. Backend server must be running
2. Players must be added to the game with equipment IDs
3. At least 2 red team players and 2 green team players configured

## Running the Traffic Generator

### Step 1: Start Backend Server
```bash
python3 -m backend.server
```

The backend will:
- Set up UDP sockets (broadcast on 7500, receive on 7501)
- Connect to PostgreSQL database
- Wait for player registrations

### Step 2: Add Players via Frontend
You need to add exactly 4 players (2 red, 2 green) with specific equipment IDs.

**Example Equipment IDs:**
- Red Player 1: Equipment ID `101`
- Red Player 2: Equipment ID `102`
- Green Player 1: Equipment ID `201`
- Green Player 2: Equipment ID `202`

Make sure to assign these equipment IDs when adding players through the frontend.

### Step 3: Start the Game
Click "Start Game" button in the frontend. This will:
- Broadcast code `202` via UDP
- Signal the traffic generator to begin

### Step 4: Run Traffic Generator
In a separate terminal:
```bash
python3 traffic_generator.py
```

When prompted, enter the equipment IDs:
```
Enter equipment id of red player 1 ==> 101
Enter equipment id of red player 2 ==> 102
Enter equipment id of green player 1 ==> 201
Enter equipment id of green player 2 ==> 202
```

The traffic generator will wait for code `202` from the game software.

## What the Traffic Generator Tests

### 1. Normal Hits (Iterations 0-4, 6-9, 11-19, 21+)
Random hits between red and green players:
- Format: `equipment_id:equipment_id`
- Expected: Attacker gets +10 points
- Backend broadcasts the victim's equipment ID

### 2. Friendly Fire (Iteration 5)
Red player 1 hits red player 2:
- Format: `101:102`
- Expected: Both players lose 10 points
- Backend broadcasts BOTH equipment IDs (101, then 102)
- Traffic generator waits for 2 broadcasts

### 3. Base Hit - Green Base (Iteration 10)
Random red player hits green base:
- Format: `<red_equipment_id>:43`
- Expected: Red player gets +100 points
- Backend broadcasts code `43`
- `hit_base` flag set to true for that player

### 4. Base Hit - Red Base (Iteration 20)
Random green player hits red base:
- Format: `<green_equipment_id>:53`
- Expected: Green player gets +100 points
- Backend broadcasts code `53`
- `hit_base` flag set to true for that player

## Monitoring the Test

### Backend Logs
Watch the backend terminal for:
```
INFO:Received UDP message: 101:201 from ...
INFO:Valid hit: Player 101 hit enemy 201
INFO:Broadcasted equipment ID: 201

WARNING:FRIENDLY FIRE: Player 101 hit teammate 102
INFO:Broadcasted equipment ID: 101
INFO:Broadcasted equipment ID: 102

INFO:RED team player 101 hit GREEN base! +100 points
INFO:Broadcasted equipment ID: 43
```

### Checking Game State
While traffic generator is running, query game state in another terminal:
```bash
curl http://localhost:5000/game/state
```

You should see:
- Players sorted by score (highest first)
- Correct team totals
- `hit_base: true` for players who hit bases
- Negative scores for players involved in friendly fire

## Expected Results

After the traffic generator completes:

**Red Team:**
- Individual scores updated based on hits/friendly fire
- One player should have +100 from base hit
- Both players lose 10 from friendly fire incident

**Green Team:**
- Individual scores updated based on hits
- One player should have +100 from base hit

## Stopping the Test

### Option 1: Let Traffic Generator Run
Traffic generator will continue until it receives code `221` (game end)

### Option 2: End Game Manually
Click "Stop Game" in frontend, which broadcasts code `221` three times.

## Troubleshooting

### Traffic Generator Won't Start
- **Problem:** Waiting for code 202
- **Solution:** Click "Start Game" in frontend

### No Response from Backend
- **Problem:** UDP ports not set up
- **Solution:** Restart backend server

### Equipment IDs Not Found
- **Problem:** Players not in game state
- **Solution:** Make sure to add players with equipment IDs through frontend before starting game

### Friendly Fire Not Detected
- **Problem:** Players not assigned to same team
- **Solution:** Check team assignment when adding players

## Full Test Flow Example

```bash
# Terminal 1: Start backend
python3 -m backend.server

# Terminal 2: Start frontend (add players, then start game)
python3 main.py

# Terminal 3: Run traffic generator
python3 traffic_generator.py
# Enter equipment IDs: 101, 102, 201, 202

# Terminal 4: Monitor game state
watch -n 1 curl -s http://localhost:5000/game/state | jq

# When done, click "Stop Game" in frontend
```

## Verifying Friendly Fire Implementation

The traffic generator specifically tests friendly fire at iteration 5:
1. Watch backend logs for "FRIENDLY FIRE" warning
2. Confirm TWO broadcasts (attacker ID, then victim ID)
3. Check game state - both players should show -10 points
4. Traffic generator should receive 2 messages before continuing

This confirms the friendly fire backend logic is working correctly!
