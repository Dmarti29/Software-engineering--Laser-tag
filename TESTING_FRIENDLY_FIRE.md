# Friendly Fire Testing Guide

This branch (`test-friendly-fire`) contains friendly fire detection logic that needs to be tested on both Mac and VM.

## What's New

### Backend Changes
- **File**: `backend/server.py`
- **Feature**: Friendly fire detection in `process_received_udp_data()`
- **Logic**: 
  - Even player IDs = Red Team
  - Odd player IDs = Green Team
  - If shooter and target have same parity (both even or both odd) = FRIENDLY FIRE

## Testing Workflow

### On Mac (Local Development)

1. **Pull the branch** (if not already on it):
   ```bash
   git checkout test-friendly-fire
   git pull origin test-friendly-fire
   ```

2. **Start the backend server**:
   ```bash
   # Terminal 1
   python3 -m backend.server
   ```

3. **Run the friendly fire test**:
   ```bash
   # Terminal 2
   python3 test_friendly_fire.py
   ```

4. **Watch the backend logs** for:
   - `WARNING` messages for friendly fire
   - `INFO` messages for valid enemy hits

### On VM (Testing Environment)

1. **SSH into your VM**

2. **Navigate to project**:
   ```bash
   cd Software-engineering--Laser-tag
   ```

3. **Pull the test branch**:
   ```bash
   git fetch origin
   git checkout test-friendly-fire
   git pull origin test-friendly-fire
   ```

4. **Start backend** (Terminal 1):
   ```bash
   python3 -m backend.server
   ```

5. **Run tests** (Terminal 2):
   ```bash
   python3 test_friendly_fire.py
   ```

## Expected Test Results

The test script sends these scenarios:

| Test | Shooter | Target | Expected Result |
|------|---------|--------|----------------|
| 1 | Red (ID 2) | Red (ID 4) | ⚠️ FRIENDLY FIRE |
| 2 | Green (ID 1) | Green (ID 3) | ⚠️ FRIENDLY FIRE |
| 3 | Red (ID 2) | Green (ID 1) | ✓ VALID HIT |
| 4 | Green (ID 1) | Red (ID 2) | ✓ VALID HIT |
| 5 | Red (ID 6) | Red (ID 8) | ⚠️ FRIENDLY FIRE |
| 6 | Green (ID 5) | Green (ID 7) | ⚠️ FRIENDLY FIRE |
| 7 | Red (ID 10) | Green (ID 11) | ✓ VALID HIT |
| 8 | Green (ID 11) | Red (ID 10) | ✓ VALID HIT |

### Backend Log Examples

**Friendly Fire:**
```
WARNING:__main__:FRIENDLY FIRE! Player 2 hit teammate 4
```

**Valid Hit:**
```
INFO:__main__:Player 2 hit enemy player 1
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000
# Kill it
kill -9 <PID>
```

### Connection Refused
- Make sure backend server is running first
- Check firewall settings on VM
- Verify PostgreSQL is running

### No Output in Logs
- Check `server.log` file
- Backend might not have started correctly
- Database connection might have failed

## Pushing Changes

When you make code changes on Mac and want to test on VM:

```bash
# On Mac
git add .
git commit -m "Update friendly fire logic"
git push origin test-friendly-fire

# On VM
git pull origin test-friendly-fire
```

## Next Steps

After testing:
1. ✅ Verify friendly fire is detected correctly
2. ✅ Verify normal hits still work
3. 📝 Document any issues
4. 🔀 Merge to main when ready

## Quick Command Reference

### Mac
```bash
# Terminal 1: Backend
python3 -m backend.server

# Terminal 2: Tests
python3 test_friendly_fire.py
```

### VM
```bash
# Terminal 1: Backend
python3 -m backend.server

# Terminal 2: Tests  
python3 test_friendly_fire.py
```

## Making Changes

To modify the friendly fire logic:
1. Edit `backend/server.py` - function `process_received_udp_data()`
2. Save changes
3. Restart backend server
4. Re-run tests
5. Commit and push to branch
