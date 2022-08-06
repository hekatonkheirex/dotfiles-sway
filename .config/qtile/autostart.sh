#! /bin/sh

export EDITOR=nvim
export QT_QPA_PLATFORMTHEME="qt5ct"
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export SSH_AUTH_SOCK

fcitx5 &
xinput --set-prop "ELAN1300:00 04F3:3087 Touchpad" "libinput Natural Scrolling Enabled" 1 &
xsetroot -cursor_name left_ptr &
nitrogen --restore &
# feh --bg-fill /mnt/windows/Walls/wallhaven-z8ewmo.jpg
picom -f -b --config /home/mura/.config/picom/picom_not_rounded.conf
$HOME/.config/scripts/thunar.sh &
thunar --daemon &
xss-lock -l $HOME/.config/scripts/lock.sh & 
blueman-applet &
xfce4-power-manager &
nm-applet &
gnome-keyring-daemon --start --components=pkcs11,secrets,ssh &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
# $HOME/.config/scripts/welcome.sh
