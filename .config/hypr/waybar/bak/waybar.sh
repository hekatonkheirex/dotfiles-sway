#!/usr/bin/env sh
# Terminate already running bar instances
killall -q "waybar"

# Wait until the processes have been shut down
while pgrep -x waybar >/dev/null; do sleep 1; done

# Launch main
$HOME/.local/bin/waybar -c $HOME/.config/hypr/waybar/config -s $HOME/.config/hypr/waybar/style.css
