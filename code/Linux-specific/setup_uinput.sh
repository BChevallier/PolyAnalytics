#!/bin/bash
# Setup script for uinput permissions

echo "Setting up uinput access for hardware-level input simulation..."

# Load uinput kernel module
echo "Loading uinput module..."
sudo modprobe uinput

# Make it load on boot
if ! grep -q "uinput" /etc/modules 2>/dev/null; then
    echo "Adding uinput to /etc/modules..."
    echo "uinput" | sudo tee -a /etc/modules
fi

# Create udev rule for non-root access
UDEV_RULE="/etc/udev/rules.d/99-uinput.rules"
if [ ! -f "$UDEV_RULE" ]; then
    echo "Creating udev rule..."
    echo 'KERNEL=="uinput", MODE="0660", GROUP="input", OPTIONS+="static_node=uinput"' | sudo tee "$UDEV_RULE"
    sudo udevadm control --reload-rules
    sudo udevadm trigger
fi

# Add user to input group
echo "Adding current user to 'input' group..."
sudo usermod -a -G input $USER

echo ""
echo "Setup complete! Please:"
echo "1. Log out and log back in for group changes to take effect"
echo "2. Or run: newgrp input"
echo ""
echo "Test with: python3 linuxInputs_evdev.py"
