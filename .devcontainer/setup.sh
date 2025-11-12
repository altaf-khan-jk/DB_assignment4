#!/bin/bash

echo "=== Setting up Database Automation Environment ==="

# Update and install system dependencies
sudo apt-get update
sudo apt-get install -y \
    mysql-client \
    default-jre \
    wget \
    ansible

# Install Flyway
echo "Installing Flyway..."
wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/9.22.0/flyway-commandline-9.22.0-linux-x64.tar.gz | tar xvz
sudo ln -sf $PWD/flyway-9.22.0/flyway /usr/local/bin/flyway

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Ansible collections (optional)
ansible-galaxy collection install community.docker 2>/dev/null || echo "Ansible collections optional"

# Make scripts executable
chmod +x *.sh 2>/dev/null || true

echo "=== Setup complete ==="
echo "Run './start_workflow.sh' to begin the assignment"