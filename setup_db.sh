#!/bin/bash

# Photon Laser Tag System - Database Setup Script

echo "==== Setting up PostgreSQL Database for Photon Laser Tag ===="
echo ""

# Make sure PostgreSQL is running
echo "Making sure PostgreSQL is running..."
sudo systemctl start postgresql || {
    echo "Failed to start PostgreSQL"
    exit 1
}

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if pg_isready &>/dev/null; then
        break
    fi
    echo "Waiting... ($i/30)"
    sleep 1
done

if ! pg_isready &>/dev/null; then
    echo "PostgreSQL failed to start"
    exit 1
fi

# Check if PostgreSQL service is running
pg_isready &> /dev/null
if [ $? -ne 0 ]; then
    echo "PostgreSQL service is not running. Please start it first."
    echo "On macOS: brew services start postgresql"
    echo "On Ubuntu: sudo systemctl start postgresql"
    exit 1
fi

echo "Checking for existing database 'photon'..."
if sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='photon';" | grep -q 1; then
    echo "Database 'photon' exists."
else
    echo "Database 'photon' does NOT exist on this host. This script will not create databases or users." 
    echo "If you want to create it, run the original setup that creates users/databases or contact your admin."
    exit 1
fi

echo "Checking for role/user 'student'..."
if sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='student';" | grep -q 1; then
    echo "Role 'student' exists."
else
    echo "Role 'student' does NOT exist on this host. This script will not create users." 
    echo "If you expect to connect as a different user, set the PSQL_USER environment variable before running this script, e.g.:"
    echo "  PSQL_USER=otheruser ./setup_db.sh"
    exit 1
fi

PSQL_USER=${PSQL_USER:-student}

echo "Attempting to connect to database 'photon' as user '$PSQL_USER' to verify access only." 
echo "Note: you may be prompted for a password unless you have .pgpass or PGPASSWORD set."

# Run a simple verification query; do NOT create or modify database objects.
VERIFY_SQL="SELECT current_database(), current_user();"

if [ -n "$PGPASSWORD" ]; then
    PGPASSWORD="$PGPASSWORD" psql -U "$PSQL_USER" -d photon -h localhost -c "$VERIFY_SQL" >/dev/null 2>&1 || {
        echo "Failed to connect to 'photon' as '$PSQL_USER'. Check credentials and that the user has CONNECT privileges."
        exit 1
    }
else
    psql -U "$PSQL_USER" -d photon -h localhost -c "$VERIFY_SQL" >/dev/null 2>&1 || {
        echo "Failed to connect to 'photon' as '$PSQL_USER'. You may need to set PGPASSWORD or ensure the user can connect."
        exit 1
    }
fi

echo ""
echo "==== Connection Verified ===="
echo "Successfully connected to database 'photon' as user '$PSQL_USER'."
echo "This script did not create or modify users/databases; it only verified connectivity."
echo ""
