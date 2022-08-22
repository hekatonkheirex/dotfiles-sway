local awful = require("awful")
local filesystem = require("gears.filesystem")
local config_dir = filesystem.get_configuration_dir()
local helpers = require("helpers")

local function autostart_apps()
	--- Compositor
	helpers.run.check_if_running("picom --experimental-backends", nil, function()
		awful.spawn("picom --experimental-backends --config " .. config_dir .. "configuration/picom.conf", false)
	end)
	--- Music Server
	-- helpers.run.run_once_pgrep("mpd")
	-- helpers.run.run_once_pgrep("mpDris2")
	--- Polkit Agent
	helpers.run.run_once_ps(
		"polkit-gnome-authentication-agent-1",
		"/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1"
	)
	--- Other stuff
	helpers.run.run_once_grep("blueman-applet")
	helpers.run.run_once_grep("nm-applet")
  helpers.run.run_once_grep("firewall-applet")
  helpers.run.run_once_grep("thunar --daemon")
  helpers.run.run_once_grep("fcitx5")
  helpers.run.run_once_grep("killall dunst")
  helpers.run.run_once_grep("killall xfce4-power-manager")
end

autostart_apps()
