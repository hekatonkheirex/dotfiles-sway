import os
import socket
import subprocess
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from typing import List  # noqa: F401


# Defaults
mod = "mod4"
myTerm = "wezterm"


# Autostart programs
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])



def focus_previous_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)
    previous_group = group.get_previous_group(skip_empty=True)
    previous_group_index = qtile.groups.index(previous_group)
    if previous_group_index < group_index:
        qtile.current_screen.set_group(previous_group)


def focus_next_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)
    next_group = group.get_next_group(skip_empty=True)
    next_group_index = qtile.groups.index(next_group)
    if next_group_index > group_index:
        qtile.current_screen.set_group(next_group)


def window_to_prev_group(qtile):
    i = qtile.groups.index(qtile.current_group)
    if qtile.current_window is not None and i != 0:
        qtile.current_window.togroup(qtile.groups[i - 1].name)


def window_to_next_group(qtile):
    i = qtile.groups.index(qtile.current_group)
    if qtile.current_window is not None and i != 6:
        qtile.current_window.togroup(qtile.groups[i + 1].name)


def toggle_minimize_all(qtile):
    group = qtile.current_screen.group
    for win in group.windows:
        win.minimized = not win.minimized
        if win.minimized is False:
            group.layout_all()


keys = [
    # The essentials
    Key(
        [mod], "Return",
        lazy.spawn(myTerm),
        desc="Launch terminal"
    ),
    Key(
        [mod, "shift"], "r",
        lazy.restart(),
        desc="Restart Qtile"
    ),
    Key(
        [mod, "shift"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"
    ),
    Key(
        [mod], "w",
        lazy.window.kill(),
        desc="Kill focused window"
    ),
    Key(
        [mod], "Tab",
        lazy.next_layout(),
        desc="Toggle between layouts"
    ),

    # Windows management
    Key(
        [mod], "h",
        lazy.layout.left(),
        desc="Move focus to left"
    ),
    Key(
        [mod], "l",
        lazy.layout.right(),
        desc="Move focus to right"
    ),
    Key(
        [mod], "j",
        lazy.layout.down(),
        desc="Move focus down"
    ),
    Key(
        [mod], "k",
        lazy.layout.up(),
        desc="Move focus up"
    ),
    Key(
        [mod], "space",
        lazy.layout.next(),
        desc="Move window focus to other window"
    ),
    Key(
        [mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        desc="Move window to the left"
    ),
    Key(
        [mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right"
    ),
    Key(
        [mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        desc="Move window down"
    ),
    Key(
        [mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        desc="Move window up"
    ),
    Key(
        [mod, "control"], "h",
        lazy.layout.grow_left(),
        desc="Grow window to the left"
    ),
    Key(
        [mod, "control"], "l",
        lazy.layout.grow_right(),
        desc="Grow window to the right"
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.grow_down(),
        desc="Grow window down"
    ),
    Key(
        [mod, "control"], "k",
        lazy.layout.grow_up(),
        desc="Grow window up"
    ),
    Key(
        [mod], "n",
        lazy.layout.normalize(),
        desc="Reset all window sizes"
    ),
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"
    ),
    Key(
        [mod], "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen"
    ),

    # Custom keybinds
    Key(
        ["control", "mod1"], "l",
        lazy.spawn('betterlockscreen -l dimblur'),
        desc="Lock the screen"
    ),
    Key(
        [mod], "b",
        lazy.spawn('firefox'),
        desc="Launch Firefox"
    ),
    Key(
        [mod], "t",
        lazy.spawn('Thunar'),
        desc="Launch Thunar"
    ),
    Key(
        [mod], "d",
        lazy.spawn('rofi -show drun'),
        desc="Spawn rofi"
    ),
    Key(
        [mod], "p",
        lazy.spawn('sh /home/mura/.config/rofi/scripts/powermenu.sh'),
        desc="Spawn powermenu"
    ),

    # Audio keybindings
    Key(
        [], "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute 0 toggle"),
        lazy.spawn("dunstify -i ~/.config/dunst/vmute.png 'Audio muted'"),
        desc="Mute audio"
    ),
    Key(
        [], "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume 0 -5%"),
        lazy.spawn("dunstify -i ~/.config/dunst/vdown.png 'Volume down'"),
        desc="Lower audio"
    ),
    Key(
        [], "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume 0 +5%"),
        lazy.spawn("dunstify -i ~/.config/dunst/vup.png 'Volume up'"),
        desc="Raise audio"
    ),

    # Screenshots
    Key(
        [], "Print",
        lazy.spawn("scrot 'screenshot_%Y%m%d_%H%M%S.png' -e \
                'mkdir -p ~/Pictures/Screenshots && mv $f \
                ~/Pictures/Screenshots && xclip -selection clipboard \
                -t image/png -i ~/Pictures/Screenshots/`ls \
                -1 -t ~/Pictures/Screenshots | head -1`'"),
        lazy.spawn("dunstify -i ~/.config/dunst/screenshot.png \
                'Screenshot captured'"),
    ),

    # Touchpad
    Key(
        [], "XF86TouchpadToggle",
        lazy.spawn("/home/mura/.config/scripts/touchpad.sh toggle"),
        desc="Enable/disable touchpad"
    ),
]

groups = []

group_names = 'www term file doc bit chat share vid mus'.split()
group_labels = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
group_layouts = [
        "monadtall", "tile", "max", "max", "max", "max", "floating",
        "floating", "max"
    ]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i]
        ))


@hook.subscribe.client_new
def assign_app_group(client):
    d = {}
    d[group_names[0]] = [
        "firefox",
        "Firefox",
        "Navigator",
        "google-chrome",
        "Google-chrome",
        ]
    d[group_names[1]] = [
        "Alacritty",
        "kitty",
        "org.wezfurlong.wezterm",
        ]
    d[group_names[2]] = [
        "thunar",
        ]
    d[group_names[3]] = [
        "Soffice",
        "libreoffice",
        ]
    d[group_names[4]] = [
        "qBittorrent",
        ]
    d[group_names[5]] = [
        "discord",
        ]
    d[group_names[6]] = [
        "TeamViewer",
        "Anydesk",
        ]
    d[group_names[7]] = [
        "mpv",
        ]
    d[group_names[8]] = [
        "Spotify",
        ]

    wm_class = client.window.get_wm_class()[0]

    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen(toggle=False)


for i, name in enumerate(group_names, 1):
    keys.extend([
        Key([mod], str(i), lazy.group[name].toscreen()),
        Key([mod, 'shift'], str(i), lazy.window.togroup(name))])

# layouts
# Gruvbox dark
# layout_theme = {
#        "border_width": 2,
#        "margin": 15,
#        "border_focus": "98971a",
#        "border_normal": "282828"
#    }

# Nord dark
# layout_theme = {
#   "border_width": 4,
#   "margin": 15,
#   "border_focus": "88c0d0",
#   "border_normal": "2e3440"
# }

# Outrun Dark
# layout_theme = {
#    "border_width": 2,
#    "margin": 15,
#    "border_focus": "f10596",
#    "border_normal": "00002a"
# }

# Dracula
# layout_theme = {
#    "border_width": 4,
#    "margin": 15,
#    "border_focus": "bd93f9",
#    "border_normal": "282a36"
# }

# Everforest
# layout_theme = {
#    "border_width": 2,
#    "margin": 15,
#    "border_focus": "a7c080",
#    "border_normal": "2b3339"
# }

# Tokyo Night
# layout_theme = {
#        "border_width": 2,
#        "margin": 15,
#        "border_focus": "9ece6a",
#        "border_normal": "1a1b26"
#    }

# Horizon
# layout_theme = {
#     "border_width": 4,
#     "margin": 15,
#     "border_focus": "09f7a0",
#     "border_normal": "1c1e26"
#  }

# Onedark
# layout_theme = {
#        "border_width": 4,
#        "margin": 15,
#        "border_focus": "98c379",
#        "border_normal": "282c34"
#    }

# Catppuccin
# layout_theme = {
#         "border_width": 2,
#         "margin": 15,
#         "border_focus": "cba6f7",
#         "border_normal": "1e1e2e"
#     }

# Rose Pine
layout_theme = {
        "border_width": 4,
        "margin": 15,
        "border_focus": "c4a7e7",
        "border_normal": "191724"
    }

# Rose Pine Dawn
# layout_theme = {
#        "border_width": 4,
#        "margin": 15,
#        "border_focus": "c4a7e7",
#        "border_normal": "232136"
#    }

# Rose Pine Dawn
# layout_theme = {
#        "border_width": 4,
#        "margin": 15,
#        "border_focus": "907aa9",
#        "border_normal": "faf4ed"
#    }

# Hackthebox
# layout_theme = {
#        "border_width": 2,
#        "margin": 15,
#        "border_focus": "9fef00",
#        "border_normal": "161f2d"
#    }

layouts = [
    layout.MonadTall(
        border_focus='c4a7e7',
        border_normal='191724',
        border_width=4,
        margin=15,
        ratio=0.52,
    ),
    layout.Tile(
        **layout_theme
    ),
    layout.Max(
        **layout_theme
    ),
    layout.Floating(
        border_focus='ebbcba',
        border_normal='191724',
        border_width=4,
        fullscreen_border_width=0,
    ),
    # layout.Columns(**layout_theme),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme)
]

# Colors definitions
# Gruvbox
# colors = [
#        ["#282828", "#282828"],  # 0 Background 0
#        ["#3c3836", "#3c3836"],  # 1 Background 1
#        ["#fbf1c7", "#fbf1c7"],  # 2 Foreground 0
#        ["#ebdbb2", "#ebdbb2"],  # 3 Foreground 1
#        ["#cc241d", "#cc241d"],  # 4 Red
#        ["#98971a", "#98971a"],  # 5 Green
#        ["#d79921", "#d79921"],  # 6 Yellow
#        ["#458588", "#458588"],  # 7 Blue
#        ["#b16286", "#b16286"],  # 8 Magenta
#        ["#689d6a", "#689d6a"],  # 9 Cyan
#        ["#d65d0e", "#d65d0e"],  # 10 Orange
#        ["#8f3f71", "#8f3f71"],  # 11 Violet
#    ]

# Nord
# colors = [
#        ["#2e3440", "#2e3440"],  # 0 Background 0
#        ["#3b4252", "#3b4252"],  # 1 Background 1
#        ["#eceff4", "#eceff4"],  # 2 Foreground 0
#        ["#e5e9f0", "#e5e9f0"],  # 3 Foreground 1
#        ["#bf616a", "#bf616a"],  # 4 Red
#        ["#a3be8c", "#a3be8c"],  # 5 Green
#        ["#ebcb8b", "#ebcb8b"],  # 6 Yellow
#        ["#5e81ac", "#5e81ac"],  # 7 Blue
#        ["#b48ead", "#b48ead"],  # 8 Magenta
#        ["#88c0d0", "#88c0d0"],  # 9 Cyan
#        ["#d08770", "#d08770"],  # 10 Orange
#        ["#81a1c1", "#81a1c1"],  # 11 Violet
#    ]

# Outrun Dark
# colors = [["#00002a", "#00002a"],  # 0 Background 0
#           ["#19193f", "#19193f"],  # 1 Background 1
#           ["#d0d0fa", "#d0d0fa"],  # 2 Foreground 0
#           ["#bbbbe1", "#bbbbe1"],  # 3 Foreground 1
#           ["#ff4242", "#ff4242"],  # 4 Red
#           ["#59f176", "#59f176"],  # 5 Green
#           ["#f3e877", "#f3e877"],  # 6 Yellow
#           ["#66b0ff", "#66b0ff"],  # 7 Blue
#           ["#f10596", "#f10596"],  # 8 Magenta
#           ["#0ef0f0", "#0ef0f0"],  # 9 Cyan
#           ["#faa613", "#faa613"],  # 10 Orange
#           ["#aa7dce", "#aa7dce"],  # 11 Violet
#         ]

# Dracula
# colors = [["#282a36", "#282a36"],  # 0 Background 0
#           ["#44475a", "#44475a"],  # 1 Background 1
#           ["#f8f8f2", "#f8f8f2"],  # 2 Foreground 0
#           ["#bfbfbf", "#bfbfbf"],  # 3 Foreground 1
#           ["#ff5555", "#ff5555"],  # 4 Red
#           ["#50fa7b", "#50fa7b"],  # 5 Green
#           ["#f1fa8c", "#f1fa8c"],  # 6 Yellow
#           ["#1098f7", "#1098f7"],  # 7 Blue
#           ["#ff79c6", "#ff79c6"],  # 8 Magenta
#           ["#8be9fd", "#8be9fd"],  # 9 Cyan
#           ["#ffb86c", "#ffb86c"],  # 10 Orange
#           ["#bd93f9", "#bd93f9"],  # 11 Violet
#         ]

# Everforest
# colors = [["#2b3339", "#2b3339"],  # 0 Background 0
#           ["#40474c", "#40474c"],  # 1 Background 1
#           ["#d3c6aa", "#d3c6aa"],  # 2 Foreground 0
#           ["#d7cbb2", "#d7cbb2"],  # 3 Foreground 1
#           ["#e67e80", "#e67e80"],  # 4 Red
#           ["#a7c080", "#a7c080"],  # 5 Green
#           ["#dbbc7f", "#dbbc7f"],  # 6 Yellow
#           ["#7fbbb3", "#7fbbb3"],  # 7 Blue
#           ["#d699b6", "#d699b6"],  # 8 Magenta
#           ["#83c092", "#83c092"],  # 9 Cyan
#           ["#ff9f1c", "#ff9f1c"],  # 10 Orange
#           ["#e3dfff", "#e3dfff"],  # 11 Violet
#         ]

# Tokyo Night
# colors = [
#        ["#1a1b26", "#1a1b26"],  # 0 Background 0
#        ["#30313b", "#30313b"],  # 1 Background 1
#        ["#a9b1d6", "#a9b1d6"],  # 2 Foreground 0
#        ["#b1b8da", "#b1b8da"],  # 3 Foreground 1
#        ["#f7768e", "#f7768e"],  # 4 Red
#        ["#9ece6a", "#9ece6a"],  # 5 Green
#        ["#e0af68", "#e0af68"],  # 6 Yellow
#        ["#7aa2f7", "#7aa2f7"],  # 7 Blue
#        ["#9a7ecc", "#9a7ecc"],  # 8 Magenta
#        ["#4abaaf", "#4abaaf"],  # 9 Cyan
#        ["#fea520", "#fea520"],  # 10 Orange
#        ["#7c7be0", "#7c7be0"],  # 11 Violet
#    ]

# Horizon
# colors = [["#1c1e26", "#1c1e26"],  # 0 Background 0
#            ["#32343b", "#32343b"],  # 1 Background 1
#            ["#d2d4de", "#d2d4de"],  # 2 Foreground 0
#            ["#d6d8e1", "#d6d8e1"],  # 3 Foreground 1
#            ["#e95678", "#e95678"],  # 4 Red
#            ["#09f7a0", "#09f7a0"],  # 5 Green
#            ["#fab795", "#fab795"],  # 6 Yellow
#            ["#25b0bc", "#25b0bc"],  # 7 Blue
#            ["#ee64ac", "#ee64ac"],  # 8 Magenta
#            ["#6bdfe6", "#6bdfe6"],  # 9 Cyan
#            ["#f09483", "#f09483"],  # 10 Orange
#            ["#b877db", "#b877db"],  # 11 Violet
#          ]

# Onedark
# colors = [
#         ["#282c34", "#282c34"],  # 0 Background 0
#         ["#302D41", "#302D41"],  # 1 Background 1
#         ["#abb2bf", "#abb2bf"],  # 2 Foreground 0
#         ["#99a0ab", "#99a0ab"],  # 3 Foreground 1
#         ["#e06c75", "#e06c75"],  # 4 Red
#         ["#98c379", "#98c379"],  # 5 Green
#         ["#e5c97b", "#e5c97b"],  # 6 Yellow
#         ["#61afef", "#61afef"],  # 7 Blue
#         ["#c678dd", "#c678dd"],  # 8 Magenta
#         ["#56b6c2", "#56b6c2"],  # 9 Cyan
#         ["#eea243", "#eea243"],  # 10 Orange
#         ["#ab87ff", "#ab87ff"],  # 11 Violet
#     ]

# Catppuccin
# colors = [
#         ["#1e1e2e", "#1e1e2e"],  # 0 Background 0
#         ["#313244", "#313244"],  # 1 Background 1
#         ["#cdd6f4", "#cdd6f4"],  # 2 Foreground 0
#         ["#bac2de", "#bac2de"],  # 3 Foreground 1
#         ["#f38ba8", "#f38ba8"],  # 4 Red
#         ["#a6e3a1", "#a6e3a1"],  # 5 Green
#         ["#f9e2af", "#f9e2af"],  # 6 Yellow
#         ["#89b4fa", "#89b4fa"],  # 7 Blue
#         ["#f5c2e7", "#f5c2e7"],  # 8 Magenta
#         ["#89dceb", "#89dceb"],  # 9 Cyan
#         ["#fab387", "#fab387"],  # 10 Orange
#         ["#cba6f7", "#cba6f7"],  # 11 Violet
#     ]

# Rose Pine
colors = [
         ["#191724", "#191724"],  # 0 Background 0
         ["#26233a", "#26233a"],  # 1 Background 1
         ["#e0def4", "#e0def4"],  # 2 Foreground 0
         ["#908caa", "#908caa"],  # 3 Foreground 1
         ["#eb6f92", "#eb6f92"],  # 4 Red
         ["#569f86", "#569f86"],  # 5 Green
         ["#f6c177", "#f6c177"],  # 6 Yellow
         ["#5a8fa5", "#5a8fa5"],  # 7 Blue
         ["#ebbcba", "#ebbcba"],  # 8 Magenta
         ["#9ccfd8", "#9ccfd8"],  # 9 Cyan
         ["#ea9d34", "#ea9d34"],  # 10 Orange
         ["#c4a7e7", "#c4a7e7"],  # 11 Violet
     ]

# Rose Pine Moon
# colors = [
#         ["#232136", "#232136"],  # 0 Background 0
#         ["#393552", "#393552"],  # 1 Background 1
#         ["#e0def4", "#e0def4"],  # 2 Foreground 0
#         ["#908caa", "#908caa"],  # 3 Foreground 1
#         ["#eb6f92", "#eb6f92"],  # 4 Red
#         ["#56949f", "#56949f"],  # 5 Green
#         ["#f6c177", "#f6c177"],  # 6 Yellow
#         ["#3e8fb0", "#3e8fb0"],  # 7 Blue
#         ["#ea9a97", "#ea9a97"],  # 8 Magenta
#         ["#9ccfd8", "#9ccfd8"],  # 9 Cyan
#         ["#ea9d34", "#ea9d34"],  # 10 Orange
#         ["#c4a7e7", "#c4a7e7"],  # 11 Violet
#     ]

# Rose Pine Dawn
# colors = [
#        ["#faf4ed", "#faf4ed"],  # 0 Background 0
#        ["#e4dfde", "#e4dfde"],  # 1 Background 1
#        ["#575279", "#575279"],  # 2 Foreground 0
#        ["#6e6a86", "#6e6a86"],  # 3 Foreground 1
#        ["#b4637a", "#b4637a"],  # 4 Red
#        ["#56949f", "#56949f"],  # 5 Green
#        ["#f6c177", "#f6c177"],  # 6 Yellow
#        ["#286983", "#286983"],  # 7 Blue
#        ["#d7827e", "#d7827e"],  # 8 Magenta
#        ["#9ccfd8", "#9ccfd8"],  # 9 Cyan
#        ["#ea9d34", "#ea9d34"],  # 10 Orange
#        ["#907aa9", "#907aa9"],  # 11 Violet
#    ]

# Hackthebox
# colors = [
#         ["#161f2d", "#161f2d"],  # 0 Background 0
#         ["#2d3542", "#2d3542"],  # 1 Background 1
#         ["#a4b1cd", "#a4b1cd"],  # 2 Foreground 0
#         ["#c5d1eb", "#c5d1eb"],  # 3 Foreground 1
#         ["#ff3e3e", "#ff3e3e"],  # 4 Red
#         ["#9fef00", "#9fef00"],  # 5 Green
#         ["#ffaf00", "#ffaf00"],  # 6 Yellow
#         ["#2e6cff", "#2e6cff"],  # 7 Blue
#         ["#9f00ff", "#9f00ff"],  # 8 Magenta
#         ["#2ee7b6", "#2ee7b6"],  # 9 Cyan
#         ["#d5a021", "#d5a021"],  # 10 Orange
#         ["#a09be7", "#a09be7"],  # 11 Violet
#     ]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

# Widgets definitions
widget_defaults = dict(
    font='Product Sans',
    fontsize=18,
    padding=4,
    background='#191724',
    foreground='#e0def4',
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    padding=8,
                    foreground=colors[5],
                    background=colors[5],
                ),
                widget.TextBox(
                    font='Material Design Icons',
                    fontsize=26,
                    foreground=colors[0],
                    background=colors[5],
                    mouse_callbacks={
                        "Button1": lazy.spawn("rofi -show drun"),
                        },
                    text=' 󰣇',
                    padding=-1,
                ),
                widget.TextBox(
                    text=' \ue0b6',
                    font='Iosevka Nerd Font',
                    fontsize=34,
                    padding=-1,
                    foreground=colors[0],
                    background=colors[5],
                ),
                widget.GroupBox(
                    active=colors[2],
                    block_highlight_text_color=colors[0],
                    borderwidth=2,
                    disable_drag=True,
                    font='Stick',
                    fontsize=18,
                    hide_unused=True,
                    highlight_color='00000000',
                    # highlight_color=colors[11],
                    # highlight_method='text',
                    highlight_method='block',
                    inactive=colors[1],
                    padding=2,
                    rounded=True,
                    spacing=4,
                    this_current_screen_border=colors[11],
                    urgent_alert_method='block',
                    urgent_border=colors[4],
                    urgent_text=colors[0],
                ),
                widget.TextBox(
                    text=' \ue0b6',
                    font='Iosevka Nerd Font',
                    fontsize=34,
                    padding=-1,
                    foreground=colors[7],
                    background=colors[0],
                ),
                widget.CurrentLayoutIcon(
                    custom_icon_paths=[
                        os.path.expanduser("~/.config/qtile/icons")
                    ],
                    padding=1,
                    scale=0.5,
                    background=colors[7],
                ),
                # widget.CurrentLayout(
                #     padding=1,
                #     foreground=colors[0],
                #     background=colors[7],
                # ),
                widget.TextBox(
                    text=' \ue0b6',
                    font='Iosevka Nerd Font',
                    fontsize=34,
                    padding=-1,
                    foreground=colors[1],
                    background=colors[7],
                ),
                # widget.TextBox(
                #     text='',
                #     font='Font Awesome 6 Brands',
                #     fontsize=16,
                #     padding=1,
                #     foreground=colors[5],
                # ),
                # widget.Mpris2(
                #     name='spotify',
                #     objname="org.mpris.MediaPlayer2.spotify",
                #     display_metadata=['xesam:title', 'xesam:artist'],
                #     scroll_chars=None,
                #     stop_pause_text='',
                #     padding=4,
                #     foreground=colors[2],
                # ),
                widget.WindowName(
                    max_chars=400,
                    padding=8,
                    foreground=colors[11],
                    background=colors[1],
                ),
                widget.Spacer(
                        background=colors[1],
                        length=5,
                ),
                widget.TextBox(
                    text=' \ue0b6',
                    font='Iosevka Nerd Font',
                    fontsize=34,
                    padding=-1,
                    foreground=colors[11],
                    background=colors[1],
                ),
                widget.Systray(
                    padding=4,
                    background=colors[11],
                ),
                widget.TextBox(
                    text=' \ue0b6',
                    font='Iosevka Nerd Font',
                    fontsize=34,
                    padding=-1,
                    foreground=colors[8],
                    background=colors[11],
                ),
                widget.TextBox(
                    text='',
                    font='Font Awesome 6 Pro',
                    fontsize=18,
                    padding=3,
                    foreground=colors[0],
                    background=colors[8],
                ),
                widget.Backlight(
                    backlight_name='amdgpu_bl0',
                    padding=1,
                    foreground=colors[0],
                    background=colors[8],
                ),
                widget.TextBox(
                    text=' \ue0b6',
                    font='Iosevka Nerd Font',
                    fontsize=34,
                    padding=-1,
                    foreground=colors[4],
                    background=colors[8],
                ),
                widget.TextBox(
                    text='',
                    font='Font Awesome 6 Pro',
                    fontsize=18,
                    padding=1,
                    foreground=colors[0],
                    background=colors[4],
                ),
                widget.PulseVolume(
                    padding=4,
                    foreground=colors[0],
                    background=colors[4],
                ),
                widget.TextBox(
                    text=' \ue0b6',
                    font='Iosevka Nerd Font',
                    fontsize=34,
                    padding=-1,
                    foreground=colors[10],
                    background=colors[4],
                ),
                widget.Wttr(
                    location={'Asuncion': 'Asuncion'},
                    padding=4,
                    format=1,
                    foreground=colors[0],
                    background=colors[10],
                ),
                widget.TextBox(
                    text=' \ue0b6',
                    font='Iosevka Nerd Font',
                    fontsize=34,
                    padding=-1,
                    foreground=colors[6],
                    background=colors[10],
                ),
                widget.TextBox(
                    text='',
                    font='Font Awesome 6 Pro',
                    fontsize=18,
                    padding=1,
                    foreground=colors[0],
                    background=colors[6],
                ),
                widget.Clock(
                    format='%a %d %b %H:%M',
                    padding=4,
                    foreground=colors[0],
                    background=colors[6],
                ),
                widget.Sep(
                    padding=4,
                    foreground=colors[6],
                    background=colors[6],
                ),
            ],
            34,
            margin=[5, 5, 0, 5],
            # border_width=[2, 2, 2, 2],
            # border_color=["1e1e2e", "1e1e2e", "1e1e2e", "1e1e2e"],
        ),
    ),
]

# Drag floating layouts
mouse = [
        Drag(
            [mod], "Button1",
            lazy.window.set_position_floating(),
            start=lazy.window.get_position()
            ),
        Drag(
            [mod], "Button3",
            lazy.window.set_size_floating(),
            start=lazy.window.get_size()
            ),
        Click(
            [mod], "Button2",
            lazy.window.bring_to_front()
            )
]

# General configurations
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus='ebbcba',
    border_normal='191724',
    border_width=4,
    fullscreen_border_width=0,
    float_rules=[
        # Run the utility `xprop` to see the wm class and name of an X client
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),  # gitk
        Match(wm_class='makebranch'),  # gitk
        Match(wm_class='maketag'),  # gitk
        Match(wm_class='ssh-askpass'),  # ssh-askpass
        Match(title='branchdialog'),  # gitk
        Match(title='pinentry'),  # GPG key password entry
        Match(wm_class='Galculator'),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"

wmname = "LG3D"
