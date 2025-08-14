import os
import urllib.request
import tempfile
import zipfile
import shutil

def download_fonts():
    # Create fonts directory if it doesn't exist
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fonts_dir = os.path.join(current_dir, "fonts")
    os.makedirs(fonts_dir, exist_ok=True)
    
    # Check if fonts already exist
    required_fonts = ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]
    all_fonts_exist = all(os.path.exists(os.path.join(fonts_dir, font)) for font in required_fonts)
    
    if all_fonts_exist:
        print("Alle erforderlichen Schriftarten sind bereits vorhanden.")
        return True
    
    print("Einige Schriftarten fehlen. Starte Download...")
    
    try:
        # Download DejaVu fonts
        font_url = "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip"
        
        print("Lade DejaVu-Schriftarten herunter...")
        with urllib.request.urlopen(font_url) as response:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                tmp_file.write(response.read())
        
        # Create a temporary directory for extraction
        temp_extract_dir = os.path.join(current_dir, "temp_fonts")
        os.makedirs(temp_extract_dir, exist_ok=True)
        
        try:
            # Extract the zip file
            print("Extrahiere Schriftarten...")
            with zipfile.ZipFile(tmp_file.name, 'r') as zip_ref:
                # Extract only the fonts we need
                for font_file in required_fonts:
                    zip_ref.extract(f"dejavu-fonts-ttf-2.37/ttf/{font_file}", temp_extract_dir)
                    # Copy to fonts directory
                    src = os.path.join(temp_extract_dir, "dejavu-fonts-ttf-2.37", "ttf", font_file)
                    dst = os.path.join(fonts_dir, font_file)
                    shutil.copy2(src, dst)
                    print(f"Kopiere {font_file} nach {dst}")
            
            print("\nSchriftarten wurden erfolgreich installiert in:", fonts_dir)
            return True
            
        finally:
            # Clean up temporary files
            if os.path.exists(tmp_file.name):
                os.remove(tmp_file.name)
            if os.path.exists(temp_extract_dir):
                shutil.rmtree(temp_extract_dir, ignore_errors=True)
                
    except Exception as e:
        print(f"Fehler beim Installieren der Schriftarten: {str(e)}")
        return False

if __name__ == "__main__":
    if download_fonts():
        print("\nDie Schriftarten wurden erfolgreich eingerichtet.")
    else:
        print("\nEs gab ein Problem beim Einrichten der Schriftarten.")
        print("Bitte stellen Sie sicher, dass Sie über eine Internetverbindung verfügen")
        print("und die erforderlichen Berechtigungen haben, um Dateien zu schreiben.")
