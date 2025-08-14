import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# Set page config with theme first
st.set_page_config(
    page_title="Normen App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set theme using CSS
st.markdown(
    """
    <style>
    /* Main app background */
    .stApp {
        background-color: #B6DDE8;
    }
    
    /* Header */
    .stApp > header {
        background-color: #B6DDE8;
    }
    
    /* Main content area */
    .stApp > div > div > div > div > div > section > div {
        background-color: #B6DDE8;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #D1E9F0;  /* Lighter blue for sidebar */
    }
    
    /* Sidebar header */
    .st-emotion-cache-1cyp6b1 {
        background-color: #D1E9F0 ;
    }
    
    /* Sidebar content */
    .st-emotion-cache-1cyp6b1 > div > div > div > div > div > div {
        background-color: #D1E9F0 ;
    }
    
    /* Sidebar text - more specific selectors */
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
    
    /* Filter boxes in sidebar - more specific */
    .st-emotion-cache-1cyp6b1 [data-baseweb="input"],
    .st-emotion-cache-1cyp6b1 [data-baseweb="select"],
    .st-emotion-cache-1cyp6b1 [role="combobox"],
    .st-emotion-cache-1cyp6b1 input,
    .st-emotion-cache-1cyp6b1 select,
    .st-emotion-cache-1cyp6b1 .st-bd,
    .st-emotion-cache-1cyp6b1 .st-bc,
    .st-emotion-cache-1cyp6b1 .st-bb,
    .st-emotion-cache-1cyp6b1 .st-ba,
    .st-emotion-cache-1cyp6b1 .stSelectbox > div,
    .st-emotion-cache-1cyp6b1 .stTextInput > div > div > input,
    .st-emotion-cache-1cyp6b1 .stNumberInput > div > div > input,
    .st-emotion-cache-1cyp6b1 .stSlider > div > div > div > div,
    .st-emotion-cache-1cyp6b1 .stCheckbox > div,
    .st-emotion-cache-1cyp6b1 .stRadio > div {
        background-color: #D1E9F0 !important;
        color: #000000 !important;
    }
    
    /* Table header and index */
    thead tr th,
    .stDataFrame th,
    .dataframe thead th,
    .stDataFrame thead th,
    .dataframe th,
    .stDataFrame th[data-testid="stTd"] {
        background-color: #B6DDE8 !important;
        color: #000000 !important;
    }
    
    /* Table index */
    .stDataFrame th.row_heading,
    .dataframe th.index_name,
    .stDataFrame th.index_name,
    .dataframe th.blank,
    .stDataFrame th.blank {
        background-color: #B6DDE8 !important;
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Try to import fpdf, but make it optional
PDF_AVAILABLE = False
FPDF = None
try:
    import importlib.util
    import sys
    import subprocess
    
    # Check if fpdf is installed
    fpdf_spec = importlib.util.find_spec('fpdf')
    if fpdf_spec is not None:
        from fpdf import FPDF
        PDF_AVAILABLE = True
        st.sidebar.success("PDF-Export ist verfügbar")
    else:
        st.warning("PDF-Export ist nicht verfügbar. Bitte installieren Sie das 'fpdf' Paket mit 'pip install fpdf'")
except Exception as e:
    st.warning(f"PDF-Export ist nicht verfügbar: {str(e)}")
    st.warning("Bitte installieren Sie das 'fpdf' Paket mit 'pip install fpdf' in der Python-Umgebung, die von Streamlit verwendet wird.")
    st.warning(f"Aktueller Python-Pfad: {sys.executable}")

# Vollständigen Pfad zur Excel-Datei erstellen
current_dir = os.path.dirname(os.path.abspath(__file__))
file_name = "tabellarische_Darstellung_Kategorien.xlsx"
file_path = os.path.join(current_dir, file_name)

try:
    #Datei lesen
    df = pd.read_excel(file_path)
    st.sidebar.success("Datei erfolgreich geladen!")
    
except PermissionError as pe:
    st.error(f"Zugriffsfehler: {str(pe)}")
    st.error("Bitte stellen Sie sicher, dass die Datei nicht von einem anderen Programm geöffnet ist.")
    st.stop()
    
except Exception as e:
    st.error(f"Fehler beim Laden der Datei: {str(e)}")
    st.error("Bitte überprüfen Sie, ob die Datei korrekt ist und nicht beschädigt.")
    st.stop()

# Vorverarbeitung: Leere Werte auffüllen und Spalten standardisieren
for col in ['Kategorie 1', 'Kategorie 2', 'Kategorie 3']:
    if col in df.columns:
        df[col] = df[col].fillna("").astype(str)
        df[col] = df[col].apply(lambda x: [c.strip() for c in str(x).split(',') if c.strip()])
    else:
        st.warning(f"Warnung: Spalte '{col}' nicht im DataFrame gefunden.")
        df[col] = ""  # Füge leere Spalte hinzu, falls nicht vorhanden

# Hilfsfunktion: alle Kategorien sammeln
def extract_all_categories(df):
    all_cats = set()
    for col in ['Kategorie 1', 'Kategorie 2', 'Kategorie 3']:
        all_cats.update(cat for sublist in df[col] for cat in sublist)
    return sorted(all_cats)

# Sidebar-Filter
st.sidebar.header("Filter")

# Kategorie Filter
st.sidebar.subheader("Kategorien Filter")

# Kategorie 1 Filter
if 'Kategorie 1' in df.columns:
    k1_options = sorted(set([item for sublist in df['Kategorie 1'] for item in sublist if item]))
    k1_selected = st.sidebar.multiselect("Wählen Sie Kategorie 1:", k1_options)
else:
    st.sidebar.warning("Spalte 'Kategorie 1' nicht gefunden")
    k1_selected = []

# Kategorie 2 Filter
if 'Kategorie 2' in df.columns:
    k2_options = sorted(set([item for sublist in df['Kategorie 2'] for item in sublist if item]))
    k2_selected = st.sidebar.multiselect("Wählen Sie Kategorie 2:", k2_options)
else:
    st.sidebar.warning("Spalte 'Kategorie 2' nicht gefunden")
    k2_selected = []

# Kategorie 3 Filter
if 'Kategorie 3' in df.columns:
    k3_options = sorted(set([item for sublist in df['Kategorie 3'] for item in sublist if item]))
    k3_selected = st.sidebar.multiselect("Wählen Sie Kategorie 3:", k3_options)
else:
    st.sidebar.warning("Spalte 'Kategorie 3' nicht gefunden")
    k3_selected = []

st.sidebar.subheader("Weitere Filter")
# Art
alle_arten = sorted(df['Art'].dropna().unique())
auswahl_art = st.sidebar.multiselect("Art auswählen:", alle_arten)

# Herausgabejahr
alle_jahre = sorted(df['Herausgabejahr'].dropna().unique())
auswahl_jahr = st.sidebar.multiselect("Herausgabejahr auswählen:", alle_jahre)

# Trägerorganisation
alle_traeger = sorted(df['Trägerorganisation'].dropna().unique())
auswahl_traeger = st.sidebar.multiselect("Trägerorganisation auswählen:", alle_traeger)

# Daten filtern
def filter_data(df):
    # Filter für Kategorie 1
    if k1_selected and 'Kategorie 1' in df.columns:
        mask = df['Kategorie 1'].apply(lambda x: any(cat in x for cat in k1_selected))
        df = df[mask]
    
    # Filter für Kategorie 2
    if k2_selected and 'Kategorie 2' in df.columns:
        mask = df['Kategorie 2'].apply(lambda x: any(cat in x for cat in k2_selected))
        df = df[mask]
    
    # Filter für Kategorie 3
    if k3_selected and 'Kategorie 3' in df.columns:
        mask = df['Kategorie 3'].apply(lambda x: any(cat in x for cat in k3_selected))
        df = df[mask]
    
    # Filter für Art
    if 'Art' in df.columns and auswahl_art:
        df = df[df['Art'].isin(auswahl_art)]
    
    # Filter für Herausgabejahr
    if 'Herausgabejahr' in df.columns and auswahl_jahr:
        df = df[df['Herausgabejahr'].astype(str).isin([str(j) for j in auswahl_jahr])]
    
    # Filter für Trägerorganisation
    if 'Trägerorganisation' in df.columns and auswahl_traeger:
        df = df[df['Trägerorganisation'].isin(auswahl_traeger)]
    
    return df

# Daten filtern
gefiltert = filter_data(df)

# Funktion zum Erstellen des PDFs
def create_pdf(dataframe):
    # Create PDF with UTF-8 support
    pdf = FPDF()
    pdf.add_page()
    
    # Enable UTF-8 encoding
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Use DejaVu font which has good Unicode support
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fonts_dir = os.path.normpath(os.path.join(current_dir, 'fonts'))
    
    # No debug information shown to user
    
    # Check if fonts directory exists
    if not os.path.exists(fonts_dir):
        st.error(f"Schriftarten-Verzeichnis nicht gefunden: {fonts_dir}")
        st.warning("Bitte führen Sie zuerst das setup_fonts.py Skript aus.")
        return
    
    # Define font paths - try multiple possible locations
    possible_font_dirs = [
        fonts_dir,
        os.path.join(fonts_dir, 'dejavu-fonts-ttf-2.37', 'ttf')
    ]
    
    normal_font = None
    bold_font = None
    
    # Search for font files in possible locations
    for font_dir in possible_font_dirs:
        if not os.path.exists(font_dir):
            continue
            
        normal_path = os.path.normpath(os.path.join(font_dir, 'DejaVuSans.ttf'))
        bold_path = os.path.normpath(os.path.join(font_dir, 'DejaVuSans-Bold.ttf'))
        
        if os.path.exists(normal_path) and os.path.exists(bold_path):
            normal_font = normal_path
            bold_font = bold_path
            break
    
    if not normal_font or not bold_font:
        st.error("Konnte die erforderlichen Schriftdateien nicht finden.")
        st.error("Bitte stellen Sie sicher, dass die folgenden Dateien vorhanden sind:")
        st.error(f"- {os.path.join(fonts_dir, 'DejaVuSans.ttf')}")
        st.error(f"- {os.path.join(fonts_dir, 'DejaVuSans-Bold.ttf')}")
        st.warning("Führen Sie das setup_fonts.py Skript aus, um die Schriftarten zu installieren.")
        return
    
    
    # Clear any existing font cache
    if hasattr(pdf, 'font_family_cache'):
        pdf.font_family_cache.clear()
    
    # Set font paths
    try:
        # Add fonts with explicit paths
        pdf.add_font('DejaVu', '', normal_font, uni=True)
        pdf.add_font('DejaVu', 'B', bold_font, uni=True)
        # Fonts loaded successfully
    except Exception as e:
        st.error(f"Fehler beim Laden der Schriftarten: {str(e)}")
        st.error(f"Stelle sicher, dass die Schriftdateien lesbar sind:")
        st.error(f"- {normal_font}")
        st.error(f"- {bold_font}")
        st.warning("Versuche mit Standardschriftart fortzufahren...")
        pdf.set_font('Arial', '', 10)
        return
    except RuntimeError as e:
        st.error(f"Fehler beim Laden der Schriftarten: {str(e)}")
        st.error(f"Überprüfen Sie, ob die Schriftdateien vorhanden sind:")
        st.error(f"- {normal_font}")
        st.error(f"- {bold_font}")
        st.warning("Falls die Dateien fehlen, führen Sie bitte setup_fonts.py aus.")
        return
    
    # Header mit Autoren und Datum
    pdf.set_font('DejaVu', 'B', 16)
    pdf.cell(0, 10, 'Normen und Standards Übersicht', 0, 1, 'C')
    
    pdf.set_font('DejaVu', '', 10)
    authors = 'Autoren: Prof. Dr. Michael Klotz, Prof. Dr. Susanne Marx, Benjamin Birkmann'
    pdf.cell(0, 10, authors, 0, 1, 'C')
    pdf.cell(0, 10, f'Erstellt am: {datetime.now().strftime("%d.%m.%Y %H:%M")}', 0, 1, 'C')
    
    # Filterinformationen
    pdf.ln(10)
    pdf.set_font('DejaVu', 'B', 12)
    pdf.cell(0, 10, 'Angewendete Filter:', 0, 1)
    
    def safe_str(value):
        if isinstance(value, (list, tuple)):
            return ', '.join(map(str, value)) if value else 'Keine'
        return str(value) if value is not None else 'Keine'
    
    pdf.set_font('DejaVu', '', 10)
    pdf.cell(0, 10, f'Kategorie 1: {safe_str(k1_selected)}', 0, 1)
    pdf.cell(0, 10, f'Kategorie 2: {safe_str(k2_selected)}', 0, 1)
    pdf.cell(0, 10, f'Kategorie 3: {safe_str(k3_selected)}', 0, 1)
    pdf.cell(0, 10, f'Art: {safe_str(auswahl_art)}', 0, 1)
    pdf.cell(0, 10, f'Jahr: {safe_str(auswahl_jahr)}', 0, 1)
    pdf.cell(0, 10, f'Trägerorganisation: {safe_str(auswahl_traeger)}', 0, 1)
    
    # Tabelle
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Gefundene Einträge: {len(gefiltert)}', 0, 1)
    
    if len(dataframe) > 0:
        # Spaltenbreiten anpassen
        col_width = 190  # Breite der Tabelle in mm
        
        # Tabellenkopf
        pdf.set_font('DejaVu', 'B', 10)
        first_column = dataframe.columns[0]
        pdf.cell(col_width, 10, 'Titel', 1, 1, 'C', fill=True)
        
        # Tabelleninhalt
        pdf.set_font('DejaVu', '', 10)
        for index, row in dataframe.iterrows():
            # Text umbrechen, falls zu lang
            text = str(row[first_column])
            # Ensure text is properly encoded for PDF
            if not isinstance(text, str):
                text = str(text)
            pdf.multi_cell(col_width, 10, text, 1, 'L')
    
    # Return the PDF as bytes with proper encoding
    return pdf.output(dest='S').encode('latin-1', errors='replace')
    # Note: If you still see issues, you might need to install the DejaVu fonts
    # They can be downloaded from: https://dejavu-fonts.github.io/

# Ergebnis anzeigen
st.write(f"Gefundene Einträge: {len(gefiltert)}")

if len(gefiltert.columns) > 0:
    # Tabelle anzeigen
    first_column = gefiltert.columns[0]
    styled_df = gefiltert[[first_column]].rename(columns={first_column: 'Titel'}).style.set_properties(
        **{'background-color': '#E1F4F9', 'color': 'black'}
    )
    st.write(styled_df)
    
    # PDF Download Button
    if len(gefiltert) > 0 and PDF_AVAILABLE:
        try:
            pdf_data = create_pdf(gefiltert)
            b64 = base64.b64encode(pdf_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="normen_uebersicht.pdf">Ergebnis als PDF herunterladen</a>'
            st.markdown(href, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Fehler beim Erstellen der PDF: {str(e)}")
    elif len(gefiltert) > 0:
        # Show CSV download as fallback
        csv = gefiltert.to_csv(index=False).encode('utf-8')
        b64 = base64.b64encode(csv).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="normen_uebersicht.csv">Ergebnis als CSV herunterladen</a>'
        st.markdown(href, unsafe_allow_html=True)
else:
    st.error("Keine Spalten im DataFrame gefunden.")
