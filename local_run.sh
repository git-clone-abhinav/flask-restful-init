#! /bin/sh

echo "================================================"
echo "Local setup script for flask-project"
echo "This will setup the local virtual environment"
echo "You can rerun this without any issues."
echo "================================================"

if [ -d ".env"];
then
    echo "Enabling virtual env"
else
    echo "No virtual env found. Please sun setup.sh first."
    exit N
fi

# Activate virtual env
. .env/bin/Activate
export ENV=development
python main.py
deactivate