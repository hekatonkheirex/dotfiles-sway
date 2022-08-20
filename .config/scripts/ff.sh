#!/bin/sh

if [ $XDG_SESSION_TYPE == "wayland" ]; then
export MOZ_DBUS_REMOTE=1
export MOZ_ENABLE_WAYLAND=1
fi
