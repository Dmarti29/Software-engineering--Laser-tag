# Backend Friendly Fire Implementation Summary

## Implemented Features

### 1. Game Start/End Broadcasts
- ✅ **Code 202**: Broadcasted when game starts (after countdown timer finishes)
- ✅ **Code 221**: Broadcasted 3 times when game ends

### 2. Hit Processing & Broadcasting
- ✅ **Normal Hit**: Broadcasts equipment ID of player that was hit
- ✅ **Friendly Fire**: Broadcasts BOTH equipment IDs (attacker first, then victim) - two separate transmissions

### 3. Base Scoring
- ✅ **Code 53 (Red Base)**: 
  - If GREEN team player hits it → +100 points
  - Base hit status tracked with `hit_base` flag
  - Broadcasts the base code (53)
  
- ✅ **Code 43 (Green Base)**:
  - If RED team player hits it → +100 points  
  - Base hit status tracked with `hit_base` flag
  - Broadcasts the base code (43)

### 4. Individual Scoring System
- ✅ **Enemy Hit**: +10 points to attacker
- ✅ **Friendly Fire**: -10 points to BOTH attacker and victim
- ✅ **Scores Sorted**: Players displayed highest to lowest on each team

## Files Modified

### 1. `backend/game_state.py` (NEW)
- GameState class for tracking players, teams, and scores
- Thread-safe operations
- Methods:
  - `add_player()` - Add player with equipment ID and team
  - `update_score()` - Add/subtract points
  - `is_friendly_fire()` - Check if same team
  - `mark_base_hit()` - Track base hits
  - `get_team_score()` - Calculate total team score

### 2. `backend/server.py` (MODIFIED)
- Integrated GameState
- Enhanced `process_received_udp_data()` with:
  - Base scoring logic (53/43 codes)
  - Friendly fire detection
  - Proper broadcasting for all scenarios
  - Score updates
- Updated `add_player()` to track team assignment
- Added `/game/state` endpoint - returns all scores sorted by highest first

## UDP Message Handling

### Format: `transmitting_id:hit_id`
```
Examples:
- "101:102" → Player 101 hit player 102
- "105:53" → Player 105 hit red base  
- "203:43" → Player 203 hit green base
```

### Processing Logic:
1. Check if `hit_id` is 53 or 43 (base codes)
2. If base: Verify correct team and award 100 points
3. If player: Check for friendly fire
   - Same team → Both lose 10 points, broadcast both IDs
   - Different team → Attacker gets 10 points, broadcast victim ID

## API Endpoints for Frontend

### GET `/game/state`
Returns real-time game state:
```json
{
  "is_active": true,
  "red_team": {
    "players": [
      {
        "equipment_id": 101,
        "player_id": 1,
        "codename": "Shadow",
        "score": 100,
        "hit_base": true
      }
    ],
    "total_score": 150
  },
  "green_team": { ... }
}
```
- Players sorted by score (highest first)
- Includes `hit_base` flag for base icon display

### POST `/game/start`
- Starts game
- Broadcasts code 202

### POST `/game/end`
- Ends game  
- Broadcasts code 221 three times

### POST `/game/reset`
- Resets all scores to 0
- Clears base hit flags
- Game remains in same state (active/inactive)

## Testing the Implementation

To test friendly fire:
1. Add players with equipment IDs to both teams
2. Start game
3. Send UDP message: `<red_equipment_id>:<red_equipment_id>` (same team)
4. Check logs for "FRIENDLY FIRE" message
5. Verify both players lost 10 points via `/game/state`

To test base scoring:
1. Send UDP message: `<green_equipment_id>:53` 
2. Check logs for "+100 points" message
3. Verify score via `/game/state` shows +100 and `hit_base: true`
