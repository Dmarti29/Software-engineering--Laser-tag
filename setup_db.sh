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

echo "Creating database user 'student'..."
psql postgres -c "CREATE USER student WITH PASSWORD 'student';" || echo "User might already exist"

echo "Creating database 'photon'..."
psql postgres -c "CREATE DATABASE photon WITH OWNER student;" || echo "Database might already exist"

echo "Granting privileges..."
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE photon TO student;"

echo "Creating players table..."
psql -U student -d photon -c "CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, codename VARCHAR(30) NOT NULL);"

echo ""
echo "==== Database Setup Complete ===="
echo "Database: photon"
echo "User: student"
echo "Password: student"
echo ""
echo "To test the connection:"
echo "psql -U student -d photon -h localhost"
echo ""
