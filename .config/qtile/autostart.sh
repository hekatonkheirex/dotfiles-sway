#! /bin/sh

export EDITOR=nvim
export QT_QPA_PLATFORMTHEME="qt5ct"
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export SSH_AUTH_SOCK

fcitx5 &
xinput --set-prop "ELAN1300:00 04F3:3087 Touchpad" "libinput Natural Scrolling Enabled" 1 &
xsetroot --cursor_name left_ptr &
nitrogen --restore &
dunst &
picom -f -b
$HOME/.config/scripts/thunar.sh &
thunar --daemon &
xss-lock -l $HOME/.config/scripts/lock.sh & 
blueman-applet &
firewall-applet &
xfce4-power-manager --daemon &
nm-applet --no-agent &
gnome-keyring-daemon --start --components=pkcs11,secrets,ssh &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
# $HOME/.config/scripts/welcome.sh
