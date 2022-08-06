# if [ -n "$DESKTOP_SESSION" ];then
#     eval $(gnome-keyring-daemon --start --components=okcs11,secrets,ssh)
#     export SSH_AUTH_SOCK
# fi

## LANGUAGE
export LANG=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8

## PATHS
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/scripts:$PATH"
export PATH="$PYENV_ROOT/bin:$PATH"
export PYENV_ROOT="$HOME/.pyenv"

## EDITOR
export EDITOR=nvim

## JAVA
export _JAVA_AWT_WM_NONREPARENTING=1

## FIREFOX
export BROWSER="/usr/bin/firefox"
export MOZ_ENABLE_WAYLAND=1

## GTK environment
export TDESKTOP_DISABLE_GTK_INTEGRATION=1
# export CLUTTER_BACKEND="wayland"
# export BEMENU_BACKEND="wayland"

## QT environment
export QT_QPA_PLATFORM="wayland-egl"
export QT_QPA_PLATFORMTHEME="qt5ct"
# export QT_WAYLAND_FORCE_DPI="physical"
# export QT_WAYLAND_DISABLE_WINDOWDECORATION=1

## SDL environment
# export SDL_VIDEODRIVER="wayland"

## Elementary environment
# export ELM_DISPLAY="wl"
# export ECORE_EVAS_ENGINE="wayland-egl"
# export ELM_ENGINE="wayland-egl"
export ELM_ACCEL="opengl"

## General
export NO_AT_BRIDGE=1
# export WINIT_UNIX_BACKEND="wayland"
export DBUS_SESSION_BUS_ADDRESS
export DBUS_SESSION_BUS_PID
