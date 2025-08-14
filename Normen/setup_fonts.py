import os
import urllib.request
import tempfile
import zipfile

def download_fonts():
    # Create fonts directory if it doesn't exist
    fonts_dir = os.path.join(os.path.dirname(__file__), ".fonts")
    os.makedirs(fonts_dir, exist_ok=True)
    
    # Download DejaVu fonts
    font_url = "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip"
    
    print("Downloading DejaVu fonts...")
    with urllib.request.urlopen(font_url) as response:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            tmp_file.write(response.read())
    
    # Extract the fonts we need
    print("Extracting fonts...")
    with zipfile.ZipFile(tmp_file.name, 'r') as zip_ref:
        # Extract only the fonts we need
        for font_file in ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]:
            zip_ref.extract(f"dejavu-fonts-ttf-2.37/ttf/{font_file}", fonts_dir)
            # Rename to the expected filenames
            os.rename(
                os.path.join(fonts_dir, "dejavu-fonts-ttf-2.37", "ttf", font_file),
                os.path.join(fonts_dir, font_file)
            )
    
    # Clean up
    os.unlink(tmp_file.name)
    print(f"Fonts downloaded to: {fonts_dir}")

if __name__ == "__main__":
    download_fonts()
