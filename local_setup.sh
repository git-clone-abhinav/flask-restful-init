#! /bin/sh

echo "================================================"
echo "Local setup script for flask-project"
echo "This will install all the dependencies"
echo "You can rerun this without any issues."
echo "================================================"

if [ -d ".env"];
then
    echo ".env folder exists. Installing using poetry..."
else
    echo ".env folder does not exist. Creating..."
    python3.7 -m venv .env
fi

# Activate virtual env
. .env/bin/Activate

# Upgrade the PIP
pip install --upgrade pip
pip install -r requirements.txt
# Work DOne, So deactive the virtual env
deactivate