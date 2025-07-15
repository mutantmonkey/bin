#!/bin/sh

export GTK_USE_PORTAL=1
export QT_QPA_PLATFORM=wayland
export QT_QPA_PLATFORMTHEME=flatpak
export SDL_VIDEODRIVER=wayland
export XDG_CURRENT_DESKTOP=sway

export GTK_THEME=Adwaita:dark
export SWAY_CURSOR_THEME=Adwaita

exec sway $@
