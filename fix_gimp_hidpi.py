import os
import shutil

def fix_huge_theme(target_font_size=12):
    """
    Overwrites 'Dark-HiDPI' with moderate font settings to fix the 'huge' UI.
    """
    # Define paths
    system_theme_path = "/usr/share/gimp/2.0/themes/Dark"
    user_config_dir = os.path.expanduser("~/.config/GIMP/2.10")
    user_theme_dir = os.path.join(user_config_dir, "themes")
    theme_name = "Dark-HiDPI"
    theme_path = os.path.join(user_theme_dir, theme_name)

    # 1. Clean up the previous "Huge" attempt
    if os.path.exists(theme_path):
        print(f"Removing previous '{theme_name}'...")
        shutil.rmtree(theme_path)

    # 2. Copy system theme again for a fresh start
    if not os.path.exists(system_theme_path):
        print(f"Error: System theme not found at {system_theme_path}")
        return

    try:
        shutil.copytree(system_theme_path, theme_path)
        print(f"Re-created '{theme_name}' from base system theme.")
    except Exception as e:
        print(f"Error creating theme: {e}")
        return

    # 3. Write the "Moderate" configuration
    # We use size 12 and scale 1.0 (no extra multiplication)
    gtkrc_path = os.path.join(theme_path, "gtkrc")
    
    moderate_config = f"""
# --- Fixed by Python Script (Moderate Size) ---
# Force the font to a specific size (12 is good for 4K with Mint scaling)
style "user-font"
{{
    font_name = "Sans {target_font_size}"
}}
widget_class "*" style "user-font"

# Reset dock scaling to 1.0 (removes the "huge" multiplier)
style "gimp-dock-style"
{{
    GimpDock::font-scale = 1.0
}}
class "GimpDock" style "gimp-dock-style"
# ----------------------------------------------
"""
    try:
        with open(gtkrc_path, 'a') as file:
            file.write(moderate_config)
        print(f"\nSUCCESS: Theme fixed with font size {target_font_size}.")
        print("Action Required: Restart GIMP. If it's still wrong, go to Edit > Preferences > Theme and click 'Reload Current Theme'.")
    except Exception as e:
        print(f"Error writing config: {e}")

if __name__ == "__main__":
    fix_huge_theme()
