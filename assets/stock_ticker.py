#!/usr/bin/env python3
"""
Nikolas' Portfolio + EUR/USD
VWCE.DE, VWRA.L, VAGF.DE, GC=F, EURUSD=X
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
import yfinance as yf
from datetime import datetime

SYMBOLS = {
    "BELA.AT":  "Jumbo   ",  # Jumbo
    "VWCE.DE":  "VWCE    ",  # Vanguard FTSE All-World
    "VWRA.L":   "VWRA    ",  # Vanguard FTSE All-World  
    "VAGF.DE":  "VAGF    ",  # Global Aggregate Bond
    "GC=F":     "Gold    ",  # Gold Futures
    "EURUSD=X": "EUR/USD ",  # Euro vs USD (live 24/5)
    }

REFRESH_SECONDS = 180  # Every 3 min

def fetch_prices():
    data = []
    for symbol, label in SYMBOLS.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            if len(hist) >= 2:
                price = hist["Close"].iloc[-1]
                prev = hist["Close"].iloc[-2]
                change_pct = ((price - prev) / prev) * 100
            else:
                price = hist["Close"].iloc[-1] if len(hist) == 1 else None
                change_pct = 0.0 if price else None
            data.append((label, symbol, price, change_pct))
        except Exception:
            data.append((label, symbol, None, None))
    return data

class TickerWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="ETFs + EUR/USD")
        self.set_default_size(260, -1)
        self.set_keep_above(True)
        self.set_decorated(True)
        self.set_resizable(True)
        self.stick()

        css = b"""
        window { background: linear-gradient(145deg, #1e1e2e, #181825); border-radius: 12px; }
        label { color: #cdd6f4; font-family: 'JetBrains Mono', monospace; }
        .header { font-size: 15px; font-weight: 700; color: #89b4fa; margin-bottom: 8px; }
        .price { font-size: 14px; padding: 2px 0; }
        .positive { color: #a6e3a1; }
        .negative { color: #f38ba8; }
        .neutral  { color: #cdd6f4; }
        .timestamp { font-size: 11px; color: #6c7086; }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.box.set_margin_top(12)
        self.box.set_margin_bottom(12)
        self.box.set_margin_start(14)
        self.box.set_margin_end(14)
        self.add(self.box)

        self.update_prices()
        GLib.timeout_add_seconds(REFRESH_SECONDS, self.update_prices)

    def update_prices(self):
        for child in self.box.get_children():
            self.box.remove(child)

        header = Gtk.Label(label="📈 ETFs + EUR/USD")
        header.get_style_context().add_class("header")
        header.set_xalign(0)
        self.box.pack_start(header, False, False, 0)

        sep = Gtk.Separator()
        self.box.pack_start(sep, False, False, 4)

        prices = fetch_prices()
        for label, symbol, price, change_pct in prices:
            if price is not None:
                arrow = "▲" if change_pct >= 0 else "▼"
                sign = "+" if change_pct >= 0 else ""
                css_class = "positive" if change_pct > 0 else ("negative" if change_pct < 0 else "neutral")
                if "EUR" in label:
                    text = f"{label} {price:>7.4f} {arrow} {sign}{change_pct:>5.2f}%"
                else:
                    text = f"{label} €{price:>8.2f} {arrow} {sign}{change_pct:>5.2f}%"
            else:
                css_class = "neutral"
                text = f"{label} {'N/A':>8}"
            
            lbl = Gtk.Label(label=text)
            lbl.get_style_context().add_class("price")
            lbl.get_style_context().add_class(css_class)
            lbl.set_xalign(0)
            self.box.pack_start(lbl, False, False, 0)

        ts = Gtk.Label(label=f"Updated: {datetime.now().strftime('%H:%M:%S EET')}")
        ts.get_style_context().add_class("timestamp")
        ts.set_xalign(1)
        self.box.pack_start(ts, False, False, 6)

        self.box.show_all()
        return True

if __name__ == "__main__":
    win = TickerWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()