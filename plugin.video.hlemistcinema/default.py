# -*- coding: utf-8 -*-
"""Hlemist Cinema - initial Kodi entry point."""
import sys
import urllib.parse
import xbmcaddon
import xbmcgui
import xbmcplugin

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])

def make_url(action):
    return sys.argv[0] + "?" + urllib.parse.urlencode({"action": action})

def root():
    items = [
        ("Vyhledat film nebo seriál", "search"),
        ("Přehled zdrojů", "sources"),
        ("Nastavení", "settings"),
    ]
    for label, action in items:
        li = xbmcgui.ListItem(label=label)
        xbmcplugin.addDirectoryItem(HANDLE, make_url(action), li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)

def search():
    keyboard = xbmc.Keyboard("", "Zadej název filmu nebo seriálu")
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText().strip():
        xbmcgui.Dialog().ok(
            "Hlemist Cinema",
            "Vyhledávání zatím není připojeno ke zdrojům. Toto je vývojová kostra doplňku."
        )

def sources():
    names = [
        ("FastShare", "source_fastshare"),
        ("WebShare", "source_webshare"),
        ("Kra.sk", "source_kra"),
        ("CZtor", "source_cztor"),
        ("Přehraj.to", "source_prehrajto"),
        ("Sosáč", "source_sosac"),
        ("HellSpy", "source_hellspy"),
        ("Sleduj.to", "source_sledujto"),
        ("Luna", "source_luna"),
    ]
    lines = []
    for label, key in names:
        state = "zapnuto" if ADDON.getSettingBool(key) else "vypnuto"
        lines.append("%s: %s" % (label, state))
    xbmcgui.Dialog().textviewer("Zdroje (stav integrace)", "\n".join(lines))

def main():
    params = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(sys.argv[2]).query))
    action = params.get("action")
    if action == "search":
        search()
    elif action == "sources":
        sources()
    elif action == "settings":
        ADDON.openSettings()
    else:
        root()

if __name__ == "__main__":
    main()
