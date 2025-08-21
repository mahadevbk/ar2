# dev's scratch pad
# tab[0] 1455
#tab [1] 1912
#tab [2] 2155
#tab [3] 2244
#tab [4] 2308
#tab [5] 2684
# court names 1367
# profile image line 55
#
#
#
#
import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, timedelta
from collections import defaultdict
from supabase import create_client, Client
import re
import urllib.parse
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io  # Added to fix 'name io is not defined' error
from itertools import combinations
from dateutil import parser
import plotly.graph_objects as go # Added for the new chart
import random
from fpdf import FPDF
import zipfile
import io
from datetime import datetime
import urllib.parse
import requests



# Set the page title
st.set_page_config(page_title="AR Tennis")

# Custom CSS for a scenic background
st.markdown("""
<style>
.stApp {
  background: linear-gradient(to bottom, #07314f, #031827);
  background-size: cover;
  background-repeat: repeat;
  background-position: center;
  background-attachment: fixed;
  background-color: #031827;
}

[data-testid="stHeader"] {
  background: linear-gradient(to top, #07314f, #035996) !important;
}

.profile-image {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border: 1px solid #fff500;
    border-radius: 20%;
    margin-right: 10px;
    vertical-align: middle;
    transition: transform 0.2s;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4), 0 0 10px rgba(255, 245, 0, 0.6);
}
.profile-image:hover {
    transform: scale(1.1);
}

/* Birthday Banner Styling */
.birthday-banner {
    background: linear-gradient(45deg, #FFFF00, #EEE8AA);
    color: #950606;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    display: flex;
    justify-content: center;
    align-items: center;
}
.whatsapp-share img {
    width: 24px;
    vertical-align: middle;
    margin-right: 5px;
}
.whatsapp-share {
    background-color: #25D366;
    color: white !important;
    padding: 5px 10px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: bold;
    margin-left: 15px;
    display: inline-flex;
    align-items: center;
    font-size: 0.8em;
    border: none;
}
.whatsapp-share:hover {
    opacity: 0.9;
}

/* Card styling for court locations */
.court-card {
    background: linear-gradient(to bottom, #031827, #07314f);
    border: 1px solid #fff500;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s, box-shadow 0.2s;
    text-align: center;
}
.court-card:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 12px rgba(255, 245, 0, 0.3);
}
.court-card h4 {
    color: #fff500;
    margin-bottom: 10px;
}
.court-card a {
    background-color: #fff500;
    color: #031827;
    padding: 8px 16px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: bold;
    display: inline-block;
    margin-top: 10px;
    transition: background-color 0.2s;
}
.court-card a:hover {
    background-color: #ffd700;
}
.court-icon {
    width: 50px;
    height: 50px;
    margin-bottom: 10px;
}

@import url('https://fonts.googleapis.com/css2?family=Offside&display=swap');
html, body, [class*="st-"], h1, h2, h3, h4, h5, h6 {
    font-family: 'Offside', sans-serif !important;
}

/* ✅ Header & subheader resize to ~125% of tab font size (14px → 17–18px) */
h1 {
    font-size: 24px !important;
}
h2 {
    font-size: 22px !important;
}
h3 {
    font-size: 16px !important;
}

/* Rankings table container */
.rankings-table-container {
    width: 100%;
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-top: 0px !important;
    padding: 10px;
}
.rankings-table-scroll {
    max-height: 500px;
    overflow-y: auto;
}

.ranking-header-row {
    display: none;
}
.ranking-row {
    display: block;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #696969;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    background-color: rgba(255, 255, 255, 0.05);
    overflow: visible;
}
.ranking-row:last-child {
    margin-bottom: 0;
}

.rank-col, .profile-col, .player-col, .points-col, .win-percent-col, .matches-col, .wins-col, .losses-col, .games-won-col, .game-diff-avg-col, .cumulative-game-diff-col, .trend-col, .birthday-col, .partners-col, .best-partner-col {
    width: 100%;
    text-align: left;
    padding: 2px 0;
    font-size: 1em;
    margin-bottom: 5px;
    word-break: break-word;
}
.rank-col {
    display: inline-block;
    white-space: nowrap;
    font-size: 1.3em;
    font-weight: bold;
    margin-right: 5px;
    color: #fff500;
}
.profile-col {
    text-align: left;
    margin-bottom: 10px;
    display: inline-block;
    vertical-align: middle;
}
.player-col {
    font-size: 1.3em;
    font-weight: bold;
    display: inline-block;
    flex-grow: 1;
    vertical-align: middle;
}

.rank-profile-player-group {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}
.rank-profile-player-group .rank-col {
    width: auto;
    margin-right: 10px;
}
.rank-profile-player-group .profile-col {
     width: auto;
     margin-right: 10px;
}

.points-col::before { content: "Points: "; font-weight: bold; color: #bbbbbb; }
.win-percent-col::before { content: "Win %: "; font-weight: bold; color: #bbbbbb; }
.matches-col::before { content: "Matches: "; font-weight: bold; color: #bbbbbb; }
.wins-col::before { content: "Wins: "; font-weight: bold; color: #bbbbbb; }
.losses-col::before { content: "Losses: "; font-weight: bold; color: #bbbbbb; }
.games-won-col::before { content: "Games Won: "; font-weight: bold; color: #bbbbbb; }
.game-diff-avg-col::before { content: "Game Diff Avg: "; font-weight: bold; color: #bbbbbb; }
.cumulative-game-diff-col::before { content: "Cumulative Game Diff.: "; font-weight: bold; color: #bbbbbb; }
.trend-col::before { content: "Recent Trend: "; font-weight: bold; color: #bbbbbb; }
.birthday-col::before { content: "Birthday: "; font-weight: bold; color: #bbbbbb; }

.points-col, .win-percent-col, .matches-col, .wins-col, .losses-col, .games-won-col, .game-diff-avg-col, .cumulative-game-diff-col, .trend-col, .birthday-col, .partners-col, .best-partner-col {
    color: #fff500;
}

div.st-emotion-cache-1jm692n {
    margin-bottom: 0px !important;
    padding-bottom: 0px !important;
}
div.st-emotion-cache-1jm692n h3 {
    margin-bottom: 0px !important;
    padding-bottom: 0px !important;
    line-height: 1 !important;
}

.rankings-table-container > div {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
.rankings-table-container > .rankings-table-scroll {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

.stTabs [data-baseweb="tab-list"] {
    flex-wrap: nowrap;
    overflow-x: auto;
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    flex: 1 0 auto;
    padding: 10px 0;
    font-size: 14px;
    text-align: center;
    margin: 2px;
}
</style>

""", unsafe_allow_html=True)

# Supabase setup
supabase_url = st.secrets["supabase"]["supabase_url"]
supabase_key = st.secrets["supabase"]["supabase_key"]
supabase: Client = create_client(supabase_url, supabase_key)

# Table names
players_table_name = "players"
matches_table_name = "matches"
bookings_table_name = "bookings"

# --- Session state initialization ---
if 'players_df' not in st.session_state:
    st.session_state.players_df = pd.DataFrame(columns=["name", "profile_image_url", "birthday"])
if 'matches_df' not in st.session_state:
    st.session_state.matches_df = pd.DataFrame(columns=["match_id", "date", "match_type", "team1_player1", "team1_player2", "team2_player1", "team2_player2", "set1", "set2", "set3", "winner", "match_image_url"])
if 'form_key_suffix' not in st.session_state:
    st.session_state.form_key_suffix = 0

if 'bookings_df' not in st.session_state:
    st.session_state.bookings_df = pd.DataFrame(columns=["booking_id", "date", "time", "match_type", "court_name", "player1", "player2", "player3", "player4", "screenshot_url"])

# --- Functions ---
def load_players():
    try:
        response = supabase.table(players_table_name).select("name, profile_image_url, birthday").execute()
        df = pd.DataFrame(response.data)
        expected_columns = ["name", "profile_image_url", "birthday"]
        for col in expected_columns:
            if col not in df.columns:
                df[col] = ""
        st.session_state.players_df = df
    except Exception as e:
        st.error(f"Error loading players: {str(e)}")

def save_players(players_df):
    try:
        expected_columns = ["name", "profile_image_url", "birthday"]
        players_df_to_save = players_df[expected_columns].copy()
        
        # Replace NaN with None for JSON compliance before saving
        players_df_to_save = players_df_to_save.where(pd.notna(players_df_to_save), None)

        supabase.table(players_table_name).upsert(players_df_to_save.to_dict("records")).execute()
    except Exception as e:
        st.error(f"Error saving players: {str(e)}")
      
def delete_player_from_db(player_name):
    try:
        supabase.table(players_table_name).delete().eq("name", player_name).execute()
    except Exception as e:
        st.error(f"Error deleting player from database: {str(e)}")

def generate_pdf_reportlab(rank_df_combined, rank_df_doubles, rank_df_singles):
    # Format the current date
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    # Buffer to store PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='Title',
        fontName='Helvetica-Bold',
        fontSize=24,
        alignment=1,  # Center
        spaceAfter=12
    )
    subtitle_style = ParagraphStyle(
        name='Subtitle',
        fontName='Helvetica-Bold',
        fontSize=14,
        alignment=1,  # Center
        spaceAfter=12
    )
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ])
    
    # Function to format DataFrame for table
    def df_to_table(df, ranking_type):
        if df.empty:
            return [Paragraph(f"{ranking_type} Rankings as of {current_date}", subtitle_style), Paragraph(f"No data available for {ranking_type.lower()} rankings.", styles['Normal'])]
        
        # Format the DataFrame
        display_df = df[["Rank", "Player", "Points", "Win %", "Matches", "Wins", "Losses", "Games Won", "Game Diff Avg", "Recent Trend"]].copy()
        display_df["Points"] = display_df["Points"].map("{:.1f}".format)
        display_df["Win %"] = display_df["Win %"].map("{:.1f}%".format)
        display_df["Game Diff Avg"] = display_df["Game Diff Avg"].map("{:.2f}".format)
        display_df["Matches"] = display_df["Matches"].astype(int)
        display_df["Wins"] = display_df["Wins"].astype(int)
        display_df["Losses"] = display_df["Losses"].astype(int)
        display_df["Games Won"] = display_df["Games Won"].astype(int)
        
        # Table data
        headers = ["Rank", "Player", "Points", "Win %", "Matches", "Wins", "Losses", "Games Won", "Game Diff Avg", "Recent Trend"]
        data = [headers] + display_df.values.tolist()
        
        # Create table
        col_widths = [0.6*inch, 1.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1*inch, 1.2*inch]
        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(table_style)
        
        return [Paragraph(f"{ranking_type} Rankings as of {current_date}", subtitle_style), table]
    
    # Add main heading
    elements.append(Paragraph("AR Tennis League", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Add tables
    elements.extend(df_to_table(rank_df_combined, "Combined"))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(PageBreak())
    
    elements.extend(df_to_table(rank_df_doubles, "Doubles"))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(PageBreak())
    
    elements.extend(df_to_table(rank_df_singles, "Singles"))
    
    # Build PDF
    doc.build(elements)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data
  

def load_matches():
    try:
        response = supabase.table(matches_table_name).select("*").execute()
        df = pd.DataFrame(response.data)
        expected_columns = ["match_id", "date", "match_type", "team1_player1", "team1_player2", "team2_player1", "team2_player2", "set1", "set2", "set3", "winner", "match_image_url"]
        for col in expected_columns:
            if col not in df.columns:
                df[col] = ""
        st.session_state.matches_df = df
    except Exception as e:
        st.error(f"Error loading matches: {str(e)}")

def save_matches(df):
    try:
        df_to_save = df.copy()
        if 'date' in df_to_save.columns:
            df_to_save['date'] = pd.to_datetime(df_to_save['date'], errors='coerce')
            df_to_save = df_to_save.dropna(subset=['date'])
            df_to_save['date'] = df_to_save['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        duplicates = df_to_save[df_to_save.duplicated(subset=['match_id'], keep=False)]
        if not duplicates.empty:
            st.warning(f"Found duplicate match_id values: {duplicates['match_id'].tolist()}")
            df_to_save = df_to_save.drop_duplicates(subset=['match_id'], keep='last')

        # Replace NaN with None for JSON compliance before saving
        df_to_save = df_to_save.where(pd.notna(df_to_save), None)
            
        supabase.table(matches_table_name).upsert(df_to_save.to_dict("records")).execute()
    except Exception as e:
        st.error(f"Error saving matches: {str(e)}")

def delete_match_from_db(match_id):
    try:
        supabase.table(matches_table_name).delete().eq("match_id", match_id).execute()
        # Remove the match from session state
        st.session_state.matches_df = st.session_state.matches_df[st.session_state.matches_df["match_id"] != match_id].reset_index(drop=True)
        save_matches(st.session_state.matches_df)  # Save to ensure consistency
    except Exception as e:
        st.error(f"Error deleting match from database: {str(e)}")

def upload_image_to_supabase(file, file_name, image_type="match"):
    try:
        bucket = "profile" if image_type == "profile" else "ar"
        if image_type == "match":
            file_path = f"2ep_1/{file_name}"
        elif image_type == "booking":
            file_path = f"bookings/{file_name}"
        else:
            file_path = file_name
        response = supabase.storage.from_(bucket).upload(file_path, file.read(), {"content-type": file.type})
        if response is None or (isinstance(response, dict) and "error" in response):
            error_message = response.get("error", "Unknown error") if isinstance(response, dict) else "Upload failed"
            return ""
        public_url = supabase.storage.from_(bucket).get_public_url(file_path)
        if not public_url.startswith(f"https://vnolrqfkpptpljizzdvw.supabase.co/storage/v1/object/public/{bucket}/"):
            st.warning(f"Uploaded image URL does not match expected prefix. Got: {public_url}")
        return public_url
    except Exception as e:
        st.error(f"Error uploading image to bucket '{bucket}/{file_path}': {str(e)}")
        return ""
        
def tennis_scores():
    scores = ["6-0", "6-1", "6-2", "6-3", "6-4", "7-5", "7-6", "0-6", "1-6", "2-6", "3-6", "4-6", "5-7", "6-7"]
    
    # Add winning super tie-break scores (e.g., 10-0 to 10-9)
    for i in range(10):
        scores.append(f"Tie Break 10-{i}")
        
    # Add losing super tie-break scores (e.g., 0-10 to 9-10)
    for i in range(10):
        scores.append(f"Tie Break {i}-10")
        
    # Add winning standard tie-break scores (e.g., 7-0 to 7-5)
    for i in range(6): # Scores from 0 to 5
        scores.append(f"Tie Break 7-{i}")
        
    # Add losing standard tie-break scores (e.g., 0-7 to 5-7)
    for i in range(6): # Scores from 0 to 5
        scores.append(f"Tie Break {i}-7")
        
    return scores



def download_image(url):
    """Download image bytes from a public Supabase URL."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        st.error(f"Failed to download {url}: {e}")
    return None


def get_quarter(month):
    if 1 <= month <= 3:
        return "Q1"
    elif 4 <= month <= 6:
        return "Q2"
    elif 7 <= month <= 9:
        return "Q3"
    else:
        return "Q4"

def generate_match_id(matches_df, match_datetime):
    year = match_datetime.year
    quarter = get_quarter(match_datetime.month)
    if not matches_df.empty and 'date' in matches_df.columns:
        matches_df['date'] = pd.to_datetime(matches_df['date'], errors='coerce')
        filtered_matches = matches_df[
            (matches_df['date'].dt.year == year) &
            (matches_df['date'].apply(lambda d: get_quarter(d.month) == quarter))
        ]
        serial_number = len(filtered_matches) + 1
        new_id = f"AR{quarter}{year}-{serial_number:02d}"
        # Ensure the ID is unique
        while new_id in matches_df['match_id'].values:
            serial_number += 1
            new_id = f"AR{quarter}{year}-{serial_number:02d}"
    else:
        serial_number = 1
        new_id = f"AR{quarter}{year}-{serial_number:02d}"
    return new_id

def get_player_trend(player, matches, max_matches=5):
    player_matches = matches[
        (matches['team1_player1'] == player) |
        (matches['team1_player2'] == player) |
        (matches['team2_player1'] == player) |
        (matches['team2_player2'] == player)
    ].copy()
    player_matches['date'] = pd.to_datetime(player_matches['date'], errors='coerce')
    player_matches = player_matches.sort_values(by='date', ascending=False)
    trend = []
    for _, row in player_matches.head(max_matches).iterrows():
        if row['match_type'] == 'Doubles':
            team1 = [row['team1_player1'], row['team1_player2']]
            team2 = [row['team2_player1'], row['team2_player2']]
        else:
            team1 = [row['team1_player1']]
            team2 = [row['team2_player1']]
        if player in team1 and row['winner'] == 'Team 1':
            trend.append('W')
        elif player in team2 and row['winner'] == 'Team 2':
            trend.append('W')
        elif row['winner'] != 'Tie':
            trend.append('L')
    return ' '.join(trend) if trend else 'No recent matches'

def display_player_insights(selected_players, players_df, matches_df, rank_df, partner_stats, key_prefix=""):
    # If selected_players is a single string, convert to a list for uniform handling
    if isinstance(selected_players, str):
        selected_players = [selected_players] if selected_players else []

    # Exclude "Visitor" from selected players
    selected_players = [p for p in selected_players if p != "Visitor"]

    if not selected_players:
        st.info("No players selected or available for insights.")
        return

    # Radio buttons to toggle between Player Insights and Birthdays
    view_option = st.radio("Select View", ["Player Insights", "Birthdays"], horizontal=True, key=f"{key_prefix}view_selector")

    if view_option == "Birthdays":
        # ... (Birthday view code remains unchanged)
        birthday_data = []
        for player in selected_players:
            player_info = players_df[players_df["name"] == player].iloc[0] if player in players_df["name"].values else None
            if player_info is None:
                continue
            birthday = player_info.get("birthday", "")
            profile_image = player_info.get("profile_image_url", "")
            if birthday and re.match(r'^\d{2}-\d{2}$', birthday):
                try:
                    day, month = map(int, birthday.split("-"))
                    birthday_dt = datetime.strptime(f"{day:02d}-{month:02d}-2000", "%d-%m-%Y")
                    birthday_formatted = birthday_dt.strftime("%d %b")
                    birthday_data.append({
                        "Player": player,
                        "Birthday": birthday_formatted,
                        "SortDate": birthday_dt,
                        "Profile": profile_image
                    })
                except ValueError:
                    continue

        if not birthday_data:
            st.info("No valid birthday data available for selected players.")
            return

        birthday_df = pd.DataFrame(birthday_data)
        birthday_df = birthday_df.sort_values(by="SortDate").reset_index(drop=True)

        st.markdown('<div class="rankings-table-container">', unsafe_allow_html=True)
        st.markdown('<div class="rankings-table-scroll">', unsafe_allow_html=True)
        for _, row in birthday_df.iterrows():
            profile_html = f'<a href="{row["Profile"]}" target="_blank"><img src="{row["Profile"]}" class="profile-image" alt="Profile"></a>' if row["Profile"] else ''
            player_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['Player']}</span>"
            birthday_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['Birthday']}</span>"
            st.markdown(f"""
            <div class="ranking-row">
                <div class="rank-profile-player-group">
                    <div class="profile-col">{profile_html}</div>
                    <div class="player-col">{player_styled}</div>
                </div>
                <div class="birthday-col">{birthday_styled}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:  # Player Insights view
        active_players = []
        for player in selected_players:
            if player in rank_df["Player"].values and player != "Visitor":
                player_data = rank_df[rank_df["Player"] == player].iloc[0]
                if player_data["Matches"] > 0:
                    active_players.append(player)

        active_players = sorted(active_players)

        if not active_players:
            st.info("No players with matches played are available for insights.")
            return

        st.markdown('<div class="rankings-table-container">', unsafe_allow_html=True)
        st.markdown('<div class="rankings-table-scroll">', unsafe_allow_html=True)

        for selected_player in active_players:
            player_info = players_df[players_df["name"] == selected_player].iloc[0] if selected_player in players_df["name"].values else None
            if player_info is None:
                continue
            birthday = player_info.get("birthday", "Not set")
            profile_image = player_info.get("profile_image_url", "")
            trend = get_player_trend(selected_player, matches_df)

            profile_html = f'<a href="{profile_image}" target="_blank"><img src="{profile_image}" class="profile-image" alt="Profile"></a>' if profile_image else ''

            player_styled = f"<span style='font-weight:bold; color:#fff500;'>{selected_player}</span>"

            player_data = rank_df[rank_df["Player"] == selected_player].iloc[0]
            rank = player_data["Rank"]
            points = player_data["Points"]
            win_percent = player_data["Win %"]
            matches = int(player_data["Matches"])
            wins = int(player_data["Wins"])
            losses = int(player_data["Losses"])
            game_diff_avg = player_data["Game Diff Avg"]
            cumulative_game_diff = int(player_data["Cumulative Game Diff"])
            games_won = int(player_data["Games Won"])

            # --- START: New calculation for D/S matches ---
            player_matches_df = matches_df[
                (matches_df['team1_player1'] == selected_player) |
                (matches_df['team1_player2'] == selected_player) |
                (matches_df['team2_player1'] == selected_player) |
                (matches_df['team2_player2'] == selected_player)
            ]
            doubles_count = player_matches_df[player_matches_df['match_type'] == 'Doubles'].shape[0]
            singles_count = player_matches_df[player_matches_df['match_type'] == 'Singles'].shape[0]
            # --- END: New calculation for D/S matches ---

            # Partners and most effective partner, excluding "Visitor"
            partners_list = "None"
            best_partner = "None"
            if selected_player in partner_stats and partner_stats[selected_player]:
                partners_list = ', '.join([
                    f'{p} ({item["wins"]} wins, {item["losses"]} losses, {item["ties"]} ties, GD Sum: {item["game_diff_sum"]:.2f})'
                    for p, item in partner_stats[selected_player].items() if p != "Visitor"
                ])
                sorted_partners = sorted(
                    [(p, item) for p, item in partner_stats[selected_player].items() if p != "Visitor"],
                    key=lambda item: (
                        item[1]['wins'] / item[1]['matches'] if item[1]['matches'] > 0 else 0,
                        item[1]['game_diff_sum'] / item[1]['matches'] if item[1]['matches'] > 0 else 0,
                        item[1]['wins']
                    ),
                    reverse=True
                )
                if sorted_partners:
                    best_partner_name = sorted_partners[0][0]
                    best_stats = sorted_partners[0][1]
                    best_win_percent = (best_stats['wins'] / best_stats['matches'] * 100) if best_stats['matches'] > 0 else 0
                    best_partner = f"{best_partner_name} ({best_stats['wins']} {'win' if best_stats['wins'] == 1 else 'wins'}, {best_win_percent:.1f}% win rate)"

            points_styled = f"<span style='font-weight:bold; color:#fff500;'>{points:.1f}</span>"
            win_percent_styled = f"<span style='font-weight:bold; color:#fff500;'>{win_percent:.1f}%</span>"
            # --- MODIFIED: Updated matches_styled to include D/S count ---
            matches_styled = f"<span style='font-weight:bold; color:#fff500;'>{matches} (Doubles: {doubles_count}, Singles: {singles_count})</span>"
            wins_styled = f"<span style='font-weight:bold; color:#fff500;'>{wins}</span>"
            losses_styled = f"<span style='font-weight:bold; color:#fff500;'>{losses}</span>"
            game_diff_avg_styled = f"<span style='font-weight:bold; color:#fff500;'>{game_diff_avg:.2f}</span>"
            cumulative_game_diff_styled = f"<span style='font-weight:bold; color:#fff500;'>{cumulative_game_diff}</span>"
            games_won_styled = f"<span style='font-weight:bold; color:#fff500;'>{games_won}</span>"
            birthday_styled = f"<span style='font-weight:bold; color:#fff500;'>{birthday}</span>"
            partners_styled = f"<span style='font-weight:bold; color:#fff500;'>{partners_list}</span>"
            best_partner_styled = f"<span style='font-weight:bold; color:#fff500;'>{best_partner}</span>"
            trend_styled = f"<span style='font-weight:bold; color:#fff500;'>{trend}</span>"

            # Updated HTML markup to ensure labels are displayed
            st.markdown(f"""
            <div class="ranking-row">
                <div class="rank-profile-player-group">
                    <div class="rank-col">{rank}</div>
                    <div class="profile-col">{profile_html}</div>
                    <div class="player-col">{player_styled}</div>
                </div>
                <div class="points-col">{points_styled}</div>
                <div class="win-percent-col">{win_percent_styled}</div>
                <div class="matches-col">{matches_styled}</div>
                <div class="wins-col">{wins_styled}</div>
                <div class="losses-col">{losses_styled}</div>
                <div class="game-diff-avg-col">{game_diff_avg_styled}</div>
                <div class="cumulative-game-diff-col">{cumulative_game_diff_styled}</div>
                <div class="games-won-col">{games_won_styled}</div>
                <div class="birthday-col">{birthday_styled}</div>
                <div class="partners-col"><span style='font-weight:bold; color:#bbbbbb;'>Partners: </span>{partners_styled}</div>
                <div class="best-partner-col"><span style='font-weight:bold; color:#bbbbbb;'>Most Effective Partner: </span>{best_partner_styled}</div>
                <div class="trend-col">{trend_styled}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def calculate_rankings(matches_to_rank):
    scores = defaultdict(float)
    wins = defaultdict(int)
    losses = defaultdict(int)
    matches_played = defaultdict(int)
    singles_matches = defaultdict(int) # Added
    doubles_matches = defaultdict(int) # Added
    games_won = defaultdict(int)
    game_diff = defaultdict(float)
    cumulative_game_diff = defaultdict(int) # New: For cumulative game difference
    partner_stats = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'ties': 0, 'matches': 0, 'game_diff_sum': 0}))

    for _, row in matches_to_rank.iterrows():
        match_type = row['match_type'] # Added
        
        if match_type == 'Doubles':
            t1 = [row['team1_player1'], row['team1_player2']]
            t2 = [row['team2_player1'], row['team2_player2']]
        else:
            t1 = [row['team1_player1']]
            t2 = [row['team2_player1']]

        team1_total_games = 0
        team2_total_games = 0
        match_gd_sum = 0
        set_count = 0
        for set_score in [row['set1'], row['set2'], row['set3']]:
            if set_score and ('-' in set_score or 'Tie Break' in set_score):
                try:
                    team1_games, team2_games = 0, 0
                    is_tie_break = "Tie Break" in set_score
                    
                    if is_tie_break:
                        # For tie breaks, the game score is always 7-6 or 6-7
                        tie_break_scores = [int(s) for s in set_score.replace("Tie Break", "").strip().split('-')]
                        if tie_break_scores[0] > tie_break_scores[1]:
                            team1_games, team2_games = 7, 6
                        else:
                            team1_games, team2_games = 6, 7
                    else:
                        # Regular set scores
                        team1_games, team2_games = map(int, set_score.split('-'))

                    team1_total_games += team1_games
                    team2_total_games += team2_games
                    match_gd_sum += team1_games - team2_games
                    set_count += 1

                    # New: Calculate cumulative game difference for each player per set
                    set_difference = team1_games - team2_games
                    for p in t1:
                        if p != "Visitor":
                            games_won[p] += team1_games
                            cumulative_game_diff[p] += set_difference
                    for p in t2:
                        if p != "Visitor":
                            games_won[p] += team2_games
                            cumulative_game_diff[p] -= set_difference

                except ValueError:
                    continue
        match_gd_avg = match_gd_sum / set_count if set_count > 0 else 0

        # Update individual player stats for non-Visitor players
        if row["winner"] == "Team 1":
            for p in t1:
                if p != "Visitor":
                    scores[p] += 3
                    wins[p] += 1
                    matches_played[p] += 1
                    game_diff[p] += match_gd_avg
                    if match_type == 'Doubles': doubles_matches[p] += 1 # Added
                    else: singles_matches[p] += 1 # Added
            for p in t2:
                if p != "Visitor":
                    scores[p] += 1
                    losses[p] += 1
                    matches_played[p] += 1
                    game_diff[p] -= match_gd_avg
                    if match_type == 'Doubles': doubles_matches[p] += 1 # Added
                    else: singles_matches[p] += 1 # Added
        elif row["winner"] == "Team 2":
            for p in t2:
                if p != "Visitor":
                    scores[p] += 3
                    wins[p] += 1
                    matches_played[p] += 1
                    game_diff[p] -= match_gd_avg
                    if match_type == 'Doubles': doubles_matches[p] += 1 # Added
                    else: singles_matches[p] += 1 # Added
            for p in t1:
                if p != "Visitor":
                    scores[p] += 1
                    losses[p] += 1
                    matches_played[p] += 1
                    game_diff[p] += match_gd_avg
                    if match_type == 'Doubles': doubles_matches[p] += 1 # Added
                    else: singles_matches[p] += 1 # Added
        else:
            # Tie
            for p in t1 + t2:
                if p != "Visitor":
                    scores[p] += 1.5
                    matches_played[p] += 1
                    game_diff[p] += match_gd_avg if p in t1 else -match_gd_avg
                    if match_type == 'Doubles': doubles_matches[p] += 1 # Added
                    else: singles_matches[p] += 1 # Added

        # Update partner stats for doubles matches
        if row['match_type'] == 'Doubles':
            for p1 in t1:
                for p2 in t1:
                    if p1 != p2 and p1 != "Visitor" and p2 != "Visitor":
                        partner_stats[p1][p2]['matches'] += 1
                        partner_stats[p1][p2]['game_diff_sum'] += match_gd_sum
                        if row["winner"] == "Team 1":
                            partner_stats[p1][p2]['wins'] += 1
                        elif row["winner"] == "Team 2":
                            partner_stats[p1][p2]['losses'] += 1
                        else:
                            partner_stats[p1][p2]['ties'] += 1
            for p1 in t2:
                for p2 in t2:
                    if p1 != p2 and p1 != "Visitor" and p2 != "Visitor":
                        partner_stats[p1][p2]['matches'] += 1
                        partner_stats[p1][p2]['game_diff_sum'] -= match_gd_sum  # Reverse for losing team
                        if row["winner"] == "Team 2":
                            partner_stats[p1][p2]['wins'] += 1
                        elif row["winner"] == "Team 1":
                            partner_stats[p1][p2]['losses'] += 1
                        else:
                            partner_stats[p1][p2]['ties'] += 1

    rank_data = []
    players_df = st.session_state.players_df
    for player in scores:
        if player == "Visitor":
            continue # Skip Visitor in rankings
        win_percentage = (wins[player] / matches_played[player] * 100) if matches_played[player] > 0 else 0
        game_diff_avg = (game_diff[player] / matches_played[player]) if matches_played[player] > 0 else 0
        profile_image = players_df[players_df["name"] == player]["profile_image_url"].iloc[0] if player in players_df["name"].values else ""
        player_trend = get_player_trend(player, matches_to_rank)
        rank_data.append({
            "Rank": f"🏆 {len(rank_data) + 1}",
            "Profile": profile_image,
            "Player": player,
            "Points": scores[player],
            "Win %": round(win_percentage, 2),
            "Matches": matches_played[player],
            "Doubles Matches": doubles_matches[player], # Added
            "Singles Matches": singles_matches[player], # Added
            "Wins": wins[player],
            "Losses": losses[player],
            "Games Won": games_won[player],
            "Game Diff Avg": round(game_diff_avg, 2),
            "Cumulative Game Diff": cumulative_game_diff[player], # New: Add to rank data
            "Recent Trend": player_trend
        })

    rank_df = pd.DataFrame(rank_data)
    if not rank_df.empty:
        rank_df = rank_df.sort_values(
            by=["Points", "Win %", "Game Diff Avg", "Games Won", "Player"],
            ascending=[False, False, False, False, True]
        ).reset_index(drop=True)
        rank_df["Rank"] = [f"🏆 {i}" for i in range(1, len(rank_df) + 1)]
    return rank_df, partner_stats

def display_community_stats(matches_df):
    """
    Calculates and displays interesting community stats for the last 7 days.
    """
    #st.subheader("AR Tennis Community Interesting Facts (Last 7 Days)")

    # Ensure the 'date' column is in datetime format
    matches_df['date'] = pd.to_datetime(matches_df['date'], errors='coerce')

    # Get the date 7 days ago from today
    seven_days_ago = datetime.now() - pd.Timedelta(days=7)

    # Filter matches from the last 7 days
    recent_matches = matches_df[matches_df['date'] >= seven_days_ago]

    if recent_matches.empty:
        st.info("No matches played in the last 7 days.")
        return

    # 1. Number of matches played in the last 7 days
    num_matches = len(recent_matches)
    st.metric("Matches Played", num_matches)

    # 2. Number of active players in the last 7 days
    player_columns = ['team1_player1', 'team1_player2', 'team2_player1', 'team2_player2']
    active_players = pd.unique(recent_matches[player_columns].values.ravel('K'))
    # Remove any potential 'None' or empty values
    active_players = [player for player in active_players if pd.notna(player) and player != '']
    num_active_players = len(active_players)
    st.metric("Active Players", num_active_players)

    # 4. Other interesting item: Top 5 players with the most wins in the last 7 days
    st.markdown("##### Top 5 Winners (Last 7 Days)")
    winners = []
    for index, row in recent_matches.iterrows():
        if row['winner'] == 'Team 1':
            winners.extend([row['team1_player1'], row['team1_player2']])
        elif row['winner'] == 'Team 2':
            winners.extend([row['team2_player1'], row['team2_player2']])

    winners = [w for w in winners if pd.notna(w) and w != '']
    if winners:
        win_counts = pd.Series(winners).value_counts().nlargest(5)
        st.table(win_counts)
    else:
        st.info("No wins recorded in the last 7 days.")

# Chart --------------

def create_nerd_stats_chart(rank_df):
    """Creates a styled, stacked bar chart for player performance."""
    if rank_df is None or rank_df.empty:
        return None

    # Sort players from highest to lowest rank (which is the default order of rank_df)
    df = rank_df.copy()

    # Define colors
    optic_yellow = '#fff500'
    bright_orange = '#FFA500'
    # Updated color palette for higher contrast
    bar_colors = ['#1E90FF', '#FFD700', '#9A5BE2']  # Dodger Blue, Gold, and a vibrant Purple

    fig = go.Figure()

    # Add traces for the stacked bars as per the user's request
    fig.add_trace(go.Bar(
        x=df['Player'],
        y=df['Matches'],
        name='Matches Played',
        marker_color=bar_colors[0]
    ))
    fig.add_trace(go.Bar(
        x=df['Player'],
        y=df['Wins'],
        name='Matches Won',
        marker_color=bar_colors[1]
    ))
    fig.add_trace(go.Bar(
        x=df['Player'],
        y=df['Points'],
        name='Points',
        marker_color=bar_colors[2]
    ))

    # Update the layout for custom styling
    fig.update_layout(
        barmode='stack',
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot area
        font=dict(color=optic_yellow),  # Set default font color for the chart
        xaxis=dict(
            title=dict(
                text='Players (Ranked Highest to Lowest)',
                font=dict(color=optic_yellow)
            ),
            tickfont=dict(color=optic_yellow),
            showgrid=False,
            linecolor=bright_orange,
            linewidth=2,
            mirror=True
        ),
        yaxis=dict(
            title=dict(
                text='Stacked Value (Points + Wins + Matches)',
                font=dict(color=optic_yellow)
            ),
            tickfont=dict(color=optic_yellow),
            gridcolor='rgba(255, 165, 0, 0.2)',  # Faint orange grid lines
            linecolor=bright_orange,
            linewidth=2,
            mirror=True
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=optic_yellow)
        ),
        margin=dict(t=60, b=10, l=10, r=10)  # Adjust top margin for legend
    )

    return fig



# --------------------------------------

def create_partnership_chart(player_name, partner_stats, players_df):
    """Creates a horizontal bar chart showing a player's performance with different partners."""
    if player_name not in partner_stats or not partner_stats[player_name]:
        return None

    partners_data = partner_stats[player_name]
    
    # Exclude "Visitor" and prepare data for DataFrame
    chart_data = []
    for partner, stats in partners_data.items():
        if partner == "Visitor":
            continue
        win_percentage = (stats['wins'] / stats['matches'] * 100) if stats['matches'] > 0 else 0
        chart_data.append({
            'Partner': partner,
            'Win %': win_percentage,
            'Matches Played': stats['matches'],
            'Wins': stats['wins'],
            'Losses': stats['losses']
        })

    if not chart_data:
        return None

    df = pd.DataFrame(chart_data).sort_values(by='Win %', ascending=True)

    # Define colors
    optic_yellow = '#fff500'
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df['Partner'],
        x=df['Win %'],
        orientation='h',
        text=df.apply(lambda row: f"{row['Wins']}W - {row['Losses']}L ({row['Matches Played']} Matches)", axis=1),
        textposition='auto',
        marker=dict(
            color=df['Win %'],
            colorscale='Viridis',
            colorbar=dict(title='Win %')
        )
    ))

    # --- THIS SECTION IS CORRECTED ---
    fig.update_layout(
        title=f'Partnership Performance for: {player_name}',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=optic_yellow),
        xaxis=dict(
            title=dict(text='Win Percentage (%)', font=dict(color=optic_yellow)),
            tickfont=dict(color=optic_yellow),
            showgrid=True,
            gridcolor='rgba(255, 165, 0, 0.2)'
        ),
        yaxis=dict(
            title=dict(text='Partner', font=dict(color=optic_yellow)),
            tickfont=dict(color=optic_yellow),
            showgrid=False
        ),
        margin=dict(l=100, r=20, t=60, b=40)
    )

    return fig



  #-----------------------------------------------------------------------------------

def save_bookings(bookings_df):
    try:
        # Convert DataFrame to list of dicts
        data = bookings_df.to_dict('records')
        # Upsert to Supabase with explicit conflict handling
        response = supabase.table("bookings").upsert(
            data,
            on_conflict="booking_id",
            returning="representation"
        ).execute()
        st.write(f"Supabase save response: {response.data}")
        return response
    except Exception as e:
        raise Exception(f"Supabase save failed: {str(e)}")





def load_bookings():
    try:
        response = supabase.table("bookings").select("*").execute()
        df = pd.DataFrame(response.data)
        expected_columns = ['booking_id', 'date', 'time', 'match_type', 'court_name',
                            'player1', 'player2', 'player3', 'player4',
                            'standby_player', 'screenshot_url']
        for col in expected_columns:
            if col not in df:
                df[col] = None

        if not df.empty:
            # Convert `date` and `time` safely
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
            #df['time'] = pd.to_datetime(df['time'], format='%H:%M', errors='coerce').dt.time
            df['time'] = pd.to_datetime(df['time'], errors='coerce').dt.time

            # Build combined datetime column
            df['booking_datetime'] = df.apply(
                lambda row: datetime.combine(row['date'], row['time'])
                if pd.notnull(row['date']) and pd.notnull(row['time'])
                else None,
                axis=1
            )

            #cutoff = datetime.now() - timedelta(hours=4)
            cutoff = pd.Timestamp.now(tz='Asia/Dubai') - timedelta(hours=4)          

            # Expired bookings
            expired = df[df['booking_datetime'].notnull() & (df['booking_datetime'] < cutoff)]

            # Delete expired bookings from Supabase
            for _, row in expired.iterrows():
                try:
                    supabase.table("bookings").delete().eq("booking_id", row['booking_id']).execute()
                except Exception as e:
                    st.error(f"Failed to delete expired booking {row['booking_id']}: {e}")

            # Keep only valid ones
            df = df[df['booking_datetime'].isnull() | (df['booking_datetime'] >= cutoff)]

        # Final cleaning for display
        df['date'] = df['date'].fillna("").astype(str)
        df['time'] = df['time'].astype(str).fillna("")
        for col in ['player1', 'player2', 'player3', 'player4', 'standby_player', 'screenshot_url']:
            df[col] = df[col].fillna("")

        st.session_state.bookings_df = df[expected_columns]

    except Exception as e:
        st.error(f"Failed to load bookings: {str(e)}")
        st.session_state.bookings_df = pd.DataFrame(columns=expected_columns)




def save_bookings(bookings_df):
    try:
        data = bookings_df.to_dict('records')
        response = supabase.table("bookings").upsert(
            data,
            on_conflict="booking_id",
            returning="representation"
        ).execute()
        return response
    except Exception as e:
        raise Exception(f"Supabase save failed: {str(e)}")



      
def create_backup_zip(players_df, matches_df, bookings_df):
    """Create a zip file with CSV tables + images from Supabase URLs."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        # --- CSVs ---
        zf.writestr("players.csv", players_df.to_csv(index=False))
        zf.writestr("matches.csv", matches_df.to_csv(index=False))
        zf.writestr("bookings.csv", bookings_df.to_csv(index=False))

        # --- Profile images ---
        for _, row in players_df.iterrows():
            url = row.get("profile_image_url")
            if url:
                img_data = download_image(url)
                if img_data:
                    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', row["name"])  # sanitize filename
                    filename = f"profile_images/{safe_name}.jpg"
                    zf.writestr(filename, img_data)

        # --- Match images ---
        for _, row in matches_df.iterrows():
            url = row.get("match_image_url")
            if url:
                img_data = download_image(url)
                if img_data:
                    match_id = row.get("match_id", str(uuid.uuid4()))
                    filename = f"match_images/{match_id}.jpg"
                    zf.writestr(filename, img_data)

    buffer.seek(0)
    return buffer



def generate_booking_id(bookings_df, booking_date):
    year = booking_date.year
    quarter = get_quarter(booking_date.month)
    if not bookings_df.empty and 'date' in bookings_df.columns:
        bookings_df['date'] = pd.to_datetime(bookings_df['date'], errors='coerce')
        filtered_bookings = bookings_df[
            (bookings_df['date'].dt.year == year) &
            (bookings_df['date'].apply(lambda d: get_quarter(d.month) == quarter))
        ]
        serial_number = len(filtered_bookings) + 1
        new_id = f"BK{quarter}{year}-{serial_number:02d}"
        while new_id in bookings_df['booking_id'].values:
            serial_number += 1
            new_id = f"BK{quarter}{year}-{serial_number:02d}"
    else:
        serial_number = 1
        new_id = f"BK{quarter}{year}-{serial_number:02d}"
    return new_id


# ==============================================================================
# START: NEW COMPLEX ODDS CALCULATION FUNCTIONS
# ==============================================================================

def _calculate_performance_score(player_stats, full_dataset):
    """
    Calculates a weighted performance score for a player based on normalized stats.
    """
    # Define weights for each component
    w_wp = 0.50  # Win Percentage
    w_agd = 0.35 # Average Game Difference
    w_ef = 0.15  # Experience Factor (Matches Played)

    # --- 1. Normalize Win Percentage (WP) ---
    max_wp = full_dataset['Win %'].max()
    wp_norm = player_stats['Win %'] / max_wp if max_wp > 0 else 0

    # --- 2. Normalize Average Game Difference (AGD) ---
    max_agd = full_dataset['Game Diff Avg'].max()
    min_agd = full_dataset['Game Diff Avg'].min()
    if max_agd == min_agd:
        agd_norm = 0.5 # Avoid division by zero if all values are the same
    else:
        agd_norm = (player_stats['Game Diff Avg'] - min_agd) / (max_agd - min_agd)

    # --- 3. Normalize Experience Factor (EF) ---
    max_matches = full_dataset['Matches'].max()
    ef_norm = player_stats['Matches'] / max_matches if max_matches > 0 else 0

    # --- 4. Calculate Final Performance Score ---
    performance_score = (w_wp * wp_norm) + (w_agd * agd_norm) + (w_ef * ef_norm)
    
    return performance_score

def calculate_enhanced_doubles_odds(players, doubles_rank_df):
    """
    Calculates balanced teams and odds for a doubles match using a multi-factor Performance Score.
    """
    if len(players) != 4 or "" in players or doubles_rank_df.empty:
        return ("Please select four players with doubles match history.", None, None)

    player_scores = {}
    for player in players:
        player_data = doubles_rank_df[doubles_rank_df["Player"] == player]
        if not player_data.empty:
            # Calculate performance score for this player
            player_scores[player] = _calculate_performance_score(player_data.iloc[0], doubles_rank_df)
        else:
            # Player has no doubles history, assign a baseline score (e.g., 0)
            player_scores[player] = 0

    # Find the most balanced pairing based on the new Performance Score
    min_diff = float('inf')
    best_pairing = None
    
    for team1_combo in combinations(players, 2):
        team2_combo = tuple(p for p in players if p not in team1_combo)
        
        team1_score = sum(player_scores.get(p, 0) for p in team1_combo)
        team2_score = sum(player_scores.get(p, 0) for p in team2_combo)
        
        diff = abs(team1_score - team2_score)
        
        if diff < min_diff:
            min_diff = diff
            best_pairing = (team1_combo, team2_combo)

    if not best_pairing:
        return ("Could not determine a balanced pairing.", None, None)

    team1, team2 = best_pairing
    team1_total_score = sum(player_scores.get(p, 0) for p in team1)
    team2_total_score = sum(player_scores.get(p, 0) for p in team2)
    total_match_score = team1_total_score + team2_total_score

    team1_odds = (team1_total_score / total_match_score) * 100 if total_match_score > 0 else 50.0
    team2_odds = (team2_total_score / total_match_score) * 100 if total_match_score > 0 else 50.0

    # Styled output
    t1p1_styled = f"<span style='font-weight:bold; color:#fff500;'>{team1[0]}</span>"
    t1p2_styled = f"<span style='font-weight:bold; color:#fff500;'>{team1[1]}</span>"
    t2p1_styled = f"<span style='font-weight:bold; color:#fff500;'>{team2[0]}</span>"
    t2p2_styled = f"<span style='font-weight:bold; color:#fff500;'>{team2[1]}</span>"
    pairing_text = f"Team 1: {t1p1_styled} & {t1p2_styled} vs Team 2: {t2p1_styled} & {t2p2_styled}"
    
    return (pairing_text, team1_odds, team2_odds)

def calculate_enhanced_singles_odds(players, singles_rank_df):
    """
    Calculates odds for a singles match using a multi-factor Performance Score.
    """
    if len(players) != 2 or "" in players or singles_rank_df.empty:
        return (None, None)

    player_scores = {}
    for player in players:
        player_data = singles_rank_df[singles_rank_df["Player"] == player]
        if not player_data.empty:
            player_scores[player] = _calculate_performance_score(player_data.iloc[0], singles_rank_df)
        else:
            player_scores[player] = 0

    p1_score = player_scores.get(players[0], 0)
    p2_score = player_scores.get(players[1], 0)
    total_score = p1_score + p2_score

    p1_odds = (p1_score / total_score) * 100 if total_score > 0 else 50.0
    p2_odds = (p2_score / total_score) * 100 if total_score > 0 else 50.0

    return (p1_odds, p2_odds)

# ==============================================================================
# UPDATED: Original functions now call the new enhanced versions
# ==============================================================================

def suggest_balanced_pairing(players, doubles_rank_df):
    """Suggests balanced doubles teams. This function now calls the enhanced odds calculation."""
    if len(players) != 4 or "" in players:
        return ("Please select all four players for a doubles match.", None, None)
    
    return calculate_enhanced_doubles_odds(players, doubles_rank_df)

def suggest_singles_odds(players, singles_rank_df):
    """Calculates winning odds for a singles match. This function now calls the enhanced odds calculation."""
    if len(players) != 2 or "" in players:
        return (None, None)
        
    return calculate_enhanced_singles_odds(players, singles_rank_df)

# ==============================================================================
# END: NEW COMPLEX ODDS CALCULATION FUNCTIONS
# ==============================================================================


def delete_booking_from_db(booking_id):
    try:
        supabase.table(bookings_table_name).delete().eq("booking_id", booking_id).execute()
        st.session_state.bookings_df = st.session_state.bookings_df[st.session_state.bookings_df["booking_id"] != booking_id].reset_index(drop=True)
        save_bookings(st.session_state.bookings_df)
    except Exception as e:
        st.error(f"Error deleting booking from database: {str(e)}")

def display_rankings_table(rank_df, title):
    if rank_df.empty:
        st.info(f"No {title} ranking data available.")
        return
    display_df = rank_df[["Rank", "Player", "Points", "Win %", "Matches", "Wins", "Losses", "Games Won", "Game Diff Avg", "Recent Trend"]].copy()
    display_df["Points"] = display_df["Points"].map("{:.1f}".format)
    display_df["Win %"] = display_df["Win %"].map("{:.1f}%".format)
    display_df["Game Diff Avg"] = display_df["Game Diff Avg"].map("{:.2f}".format)
    display_df["Matches"] = display_df["Matches"].astype(int)
    display_df["Wins"] = display_df["Wins"].astype(int)
    display_df["Losses"] = display_df["Losses"].astype(int)
    display_df["Games Won"] = display_df["Games Won"].astype(int)
    st.subheader(f"{title} Rankings")
    st.dataframe(display_df, hide_index=True, height=300)

def display_match_table(df, title):
    if df.empty:
        st.info(f"No {title} match data available.")
        return

    table_df = df.copy()

    # Create a formatted Match column
    def format_match_info(row):
        scores = [s for s in [row['set1'], row['set2'], row['set3']] if s]
        scores_str = ", ".join(scores)

        if row['match_type'] == 'Doubles':
            players = f"{row['team1_player1']} & {row['team1_player2']} vs. {row['team2_player1']} & {row['team2_player2']}"
        else:
            players = f"{row['team1_player1']} vs. {row['team2_player1']}"

        # Handle tie and winner cases with "tied with" for ties
        if row['winner'] == "Tie":
            if row['match_type'] == 'Doubles':
                return f"{row['team1_player1']} & {row['team1_player2']} tied with {row['team2_player1']} & {row['team2_player2']} ({scores_str})"
            else:
                return f"{row['team1_player1']} tied with {row['team2_player1']} ({scores_str})"
        elif row['winner'] == "Team 1":
            return f"{row['team1_player1']} {'& ' + row['team1_player2'] if row['match_type']=='Doubles' else ''} def. {row['team2_player1']} {'& ' + row['team2_player2'] if row['match_type']=='Doubles' else ''} ({scores_str})"
        elif row['winner'] == "Team 2":
            return f"{row['team2_player1']} {'& ' + row['team2_player2'] if row['match_type']=='Doubles' else ''} def. {row['team1_player1']} {'& ' + row['team1_player2'] if row['match_type']=='Doubles' else ''} ({scores_str})"
        else:
            return f"{players} ({scores_str})"

    table_df['Match Details'] = table_df.apply(format_match_info, axis=1)

    # Select and rename columns for display
    display_df = table_df[['date', 'Match Details', 'match_image_url']].copy()
    display_df.rename(columns={
        'date': 'Date',
        'match_image_url': 'Image URL'
    }, inplace=True)

    # Format the date column as dd MMM yy
    display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%d %b %y')

    st.dataframe(display_df, height=300)


def generate_whatsapp_link(row):
    # Build side labels
    if row["match_type"] == "Singles":
        t1 = f"{row['team1_player1']}"
        t2 = f"{row['team2_player1']}"
    else:  # Doubles
        t1 = f"{row['team1_player1']} & {row['team1_player2']}"
        t2 = f"{row['team2_player1']} & {row['team2_player2']}"

    # Scores and date
    scores_list = []
    for s in [row['set1'], row['set2'], row['set3']]:
        if s:
            if "Tie Break" in s:
                tie_break_scores = s.replace("Tie Break", "").strip().split('-')
                if int(tie_break_scores[0]) > int(tie_break_scores[1]):
                    scores_list.append(f'*7-6({tie_break_scores[0]}:{tie_break_scores[1]})*')
                else:
                    scores_list.append(f'*6-7({tie_break_scores[0]}:{tie_break_scores[1]})*')
            else:
                scores_list.append(f'*{s.replace("-", ":")}*')
                
    scores_str = " ".join(scores_list)
    
    # Check if the date is valid before formatting
    if pd.notna(row['date']):
        date_str = row['date'].strftime('%A, %d %b')
    else:
        date_str = "Unknown Date" # Fallback text

    # Headline text: use "tied with" for ties
    if row["winner"] == "Tie":
        headline = f"*{t1} tied with {t2}*"
    elif row["winner"] == "Team 1":
        headline = f"*{t1} def. {t2}*"
    else:  # Team 2
        headline = f"*{t2} def. {t1}*"

    share_text = f"{headline}\nSet scores {scores_str} on *{date_str}*"
    encoded_text = urllib.parse.quote(share_text)
    return f"https://api.whatsapp.com/send/?text={encoded_text}&type=custom_url&app_absent=0"


# Birthday Functions added


def check_birthdays(players_df):
    """Checks for players whose birthday is today in various formats like dd-mm, d-m, dd MMM, dd MMM yyyy, etc."""
    today = datetime.now()
    birthday_players = []

    if 'birthday' in players_df.columns and not players_df.empty:
        valid_birthdays_df = players_df.dropna(subset=['birthday']).copy()

        for _, row in valid_birthdays_df.iterrows():
            raw_bday = str(row['birthday']).strip()
            if not raw_bday:
                continue

            try:
                # Parse with dateutil to support both numeric and text month formats
                bday_parsed = parser.parse(raw_bday, dayfirst=True)
                if bday_parsed.day == today.day and bday_parsed.month == today.month:
                    birthday_str = bday_parsed.strftime("%d %b")
                    birthday_players.append((row['name'], birthday_str))
            except (ValueError, TypeError):
                continue

    return birthday_players



def display_birthday_message(birthday_players):
    """Displays a prominent birthday banner for each player in the list."""
    for player_name, birthday_str in birthday_players:
        message = f"Happy Birthday {player_name}! "
        whatsapp_message = f"*{message}* 🎂🎈"
        encoded_message = urllib.parse.quote(whatsapp_message)
        whatsapp_link = f"https://wa.me/?text={encoded_message}"

        st.markdown(f"""
        <div class="birthday-banner">
            <span>🎂🎈 {message} 🎈🎂</span>
            <a href="{whatsapp_link}" target="_blank" class="whatsapp-share">
                <img src="https://img.icons8.com/color/48/000000/whatsapp.png" alt="WhatsApp Icon">
            </a>
        </div>
        """, unsafe_allow_html=True)

    

# --- Main App Logic ---
load_players()
load_matches()
load_bookings()

# Check for and display birthday messages
todays_birthdays = check_birthdays(st.session_state.players_df)
if todays_birthdays:
    display_birthday_message(todays_birthdays)


court_names = [
    "Alvorado 1","Alvorado 2", "Palmera 2", "Palmera 4", "Saheel", "Hattan",
    "MLC Mirador La Colleccion", "Al Mahra", "Mirador", "Reem 1", "Reem 2",
    "Reem 3", "Alma", "Mira 2", "Mira 4", "Mira 5 A", "Mira 5 B", "Mira Oasis 1",
    "Mira Oasis 2", "Mira Oasis 3 A","Mira Oasis 3 B", "Mira Oasis 3 C"
]

players_df = st.session_state.players_df
matches = st.session_state.matches_df
players = sorted([p for p in players_df["name"].dropna().tolist() if p != "Visitor"]) if "name" in players_df.columns else []

if not matches.empty and ("match_id" not in matches.columns or matches["match_id"].isnull().any()):
    matches['date'] = pd.to_datetime(matches['date'], errors='coerce')
    for i in matches.index:
        if pd.isna(matches.at[i, "match_id"]):
            match_date_for_id = matches.at[i, "date"] if pd.notna(matches.at[i, "date"]) else datetime.now()
            matches.at[i, "match_id"] = generate_match_id(matches, match_date_for_id)
    save_matches(matches)

st.image("https://raw.githubusercontent.com/mahadevbk/ar2/main/dubai.png", use_container_width=True)

tab_names = ["Rankings", "Matches", "Player Profile", "Maps", "Bookings","Mini Tourney"]

tabs = st.tabs(tab_names)

with tabs[0]:
    st.header(f"Rankings as of {datetime.now().strftime('%d %b')}")
    ranking_type = st.radio("Select Ranking View", ["Combined", "Doubles", "Singles", "Nerd Stuff", "Table View"], horizontal=True, key="ranking_type_selector")
    if ranking_type == "Doubles":
        filtered_matches = matches[matches['match_type'] == 'Doubles'].copy()
        rank_df, partner_stats = calculate_rankings(filtered_matches)
        #st.subheader(f"Rankings as of {datetime.now().strftime('%d/%m')}")
        st.markdown('<div class="rankings-table-container">', unsafe_allow_html=True)
        st.markdown('<div class="rankings-table-scroll">', unsafe_allow_html=True)
        if rank_df.empty:
            st.info("No ranking data available for this view.")
        else:
            for index, row in rank_df.iterrows():
                profile_html = f'<a href="{row["Profile"]}" target="_blank"><img src="{row["Profile"]}" class="profile-image" alt="Profile"></a>' if row["Profile"] else ''
                player_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['Player']}</span>"
                points_value_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['Points']:.1f}</span>"
                trend_value_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['Recent Trend']}</span>"
                st.markdown(f"""
                <div class="ranking-row">
                    <div class="rank-profile-player-group">
                        <div class="rank-col">{row["Rank"]}</div>
                        <div class="profile-col">{profile_html}</div>
                        <div class="player-col">{player_styled}</div>
                    </div>
                    <div class="points-col">{points_value_styled}</div>
                    <div class="win-percent-col">{row["Win %"]:.1f}%</div>
                    <div class="matches-col">{int(row["Matches"])}</div>
                    <div class="wins-col">{int(row["Wins"])}</div>
                    <div class="losses-col">{int(row["Losses"])}</div>
                    <div class="game-diff-avg-col">{row["Game Diff Avg"]:.2f}</div>
                    <div class="games-won-col">{int(row["Games Won"])}</div>
                    <div class="trend-col">{trend_value_styled}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.subheader("Player Insights")
        selected_player_rankings = st.selectbox("Select a player for insights", [""] + players, index=0, key="insights_player_rankings_doubles")
        if selected_player_rankings:
            display_player_insights(selected_player_rankings, players_df, filtered_matches, rank_df, partner_stats, key_prefix="rankings_doubles_")
        else:
            st.info("Player insights will be available once a player is selected.")
    elif ranking_type == "Singles":
        filtered_matches = matches[matches['match_type'] == 'Singles'].copy()
        rank_df, partner_stats = calculate_rankings(filtered_matches)
        current_date_formatted = datetime.now().strftime("%d/%m")
        st.subheader(f"Rankings as of {current_date_formatted}")
        st.markdown('<div class="rankings-table-container">', unsafe_allow_html=True)
        st.markdown('<div class="rankings-table-scroll">', unsafe_allow_html=True)
        if rank_df.empty:
            st.info("No ranking data available for this view.")
        else:
            for index, row in rank_df.iterrows():
                profile_html = f'<a href="{row["Profile"]}" target="_blank"><img src="{row["Profile"]}" class="profile-image" alt="Profile"></a>' if row["Profile"] else ''
                player_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['Player']}</span>"
                points_value_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['Points']:.1f}</span>"
                trend_value_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['Recent Trend']}</span>"
                st.markdown(f"""
                <div class="ranking-row">
                    <div class="rank-profile-player-group">
                        <div class="rank-col">{row["Rank"]}</div>
                        <div class="profile-col">{profile_html}</div>
                        <div class="player-col">{player_styled}</div>
                    </div>
                    <div class="points-col">{points_value_styled}</div>
                    <div class="win-percent-col">{row["Win %"]:.1f}%</div>
                    <div class="matches-col">{int(row["Matches"])}</div>
                    <div class="wins-col">{int(row["Wins"])}</div>
                    <div class="losses-col">{int(row["Losses"])}</div>
                    <div class="game-diff-avg-col">{row["Game Diff Avg"]:.2f}</div>
                    <div class="games-won-col">{int(row["Games Won"])}</div>
                    <div class="trend-col">{trend_value_styled}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.subheader("Player Insights")
        selected_player_rankings = st.selectbox("Select a player for insights", [""] + players, index=0, key="insights_player_rankings_singles")
        if selected_player_rankings:
            display_player_insights(selected_player_rankings, players_df, filtered_matches, rank_df, partner_stats, key_prefix="rankings_singles_")
        else:
            st.info("Player insights will be available once a player is selected.")
    elif ranking_type == "Nerd Stuff":
        if matches.empty or players_df.empty:
            st.info("No match data available to generate interesting stats.")
        else:
            rank_df, partner_stats = calculate_rankings(matches)

            # Most Effective Partnership
            st.markdown("### 🤝 Most Effective Partnership")
            best_partner = None
            max_value = -1
            for player, partners in partner_stats.items():
                if player == "Visitor":
                    continue
                for partner, stats in partners.items():
                    if partner == "Visitor" or player < partner:  # Avoid double counting
                        win_rate = stats['wins'] / stats['matches'] if stats['matches'] > 0 else 0
                        avg_game_diff = stats['game_diff_sum'] / stats['matches'] if stats['matches'] > 0 else 0
                        score = win_rate + (avg_game_diff / 10)  # Adjust weight of game diff
                        if score > max_value:
                            max_value = score
                            best_partner = (player, partner, stats)

            if best_partner:
                p1, p2, stats = best_partner
                p1_styled = f"<span style='font-weight:bold; color:#fff500;'>{p1}</span>"
                p2_styled = f"<span style='font-weight:bold; color:#fff500;'>{p2}</span>"
                win_rate = (stats['wins'] / stats['matches'] * 100) if stats['matches'] > 0 else 0
                st.markdown(f"The most effective partnership is {p1_styled} and {p2_styled} with **{stats['wins']}** wins, **{stats['losses']}** losses, and a total game difference of **{stats['game_diff_sum']:.2f}** (win rate: {win_rate:.1f}%).", unsafe_allow_html=True)
            else:
                st.info("No doubles matches have been played to determine the most effective partnership.")

            st.markdown("---")

            # Best Player to Partner With
            st.markdown("### 🥇 Best Player to Partner With")
            player_stats = defaultdict(lambda: {'wins': 0, 'gd_sum': 0, 'partners': set()})
            for _, row in matches.iterrows():
                if row['match_type'] == 'Doubles':
                    t1 = [row['team1_player1'], row['team1_player2']]
                    t2 = [row['team2_player1'], row['team2_player2']]

                    match_gd_sum = 0
                    set_count = 0
                    for set_score in [row['set1'], row['set2'], row['set3']]:
                        if set_score and '-' in set_score:
                            try:
                                team1_games, team2_games = map(int, set_score.split('-'))
                                match_gd_sum += team1_games - team2_games
                                set_count += 1
                            except ValueError:
                                continue

                    if set_count > 0:
                        if row["winner"] == "Team 1":
                            for p in t1:
                                if p != "Visitor":
                                    player_stats[p]['wins'] += 1
                                    player_stats[p]['gd_sum'] += match_gd_sum
                                    for partner in t1:
                                        if partner != p and partner != "Visitor":
                                            player_stats[p]['partners'].add(partner)
                        elif row["winner"] == "Team 2":
                            for p in t2:
                                if p != "Visitor":
                                    player_stats[p]['wins'] += 1
                                    player_stats[p]['gd_sum'] += match_gd_sum
                                    for partner in t2:
                                        if partner != p and partner != "Visitor":
                                            player_stats[p]['partners'].add(partner)

            if player_stats:
                best_partner_candidate = None
                max_score = -1

                wins_list = [stats['wins'] for stats in player_stats.values()]
                gd_list = [stats['gd_sum'] for stats in player_stats.values()]
                partners_list = [len(stats['partners']) for stats in player_stats.values()]

                max_wins = max(wins_list) if wins_list else 1
                max_gd = max(gd_list) if gd_list else 1
                max_partners = max(partners_list) if partners_list else 1

                for player, stats in player_stats.items():
                    # Normalize scores and create a composite score
                    normalized_wins = stats['wins'] / max_wins
                    normalized_gd = stats['gd_sum'] / max_gd
                    normalized_partners = len(stats['partners']) / max_partners

                    composite_score = normalized_wins + normalized_gd + normalized_partners

                    if composite_score > max_score:
                        max_score = composite_score
                        best_partner_candidate = (player, stats)

                if best_partner_candidate:
                    player_name, stats = best_partner_candidate
                    player_styled = f"<span style='font-weight:bold; color:#fff500;'>{player_name}</span>"
                    st.markdown(f"The best player to partner with is {player_styled} based on their high number of wins, game difference sum, and variety of partners. They have:", unsafe_allow_html=True)
                    st.markdown(f"- **Total Wins**: {stats['wins']}")
                    st.markdown(f"- **Total Game Difference**: {stats['gd_sum']:.2f}")
                    st.markdown(f"- **Unique Partners Played With**: {len(stats['partners'])}")
                else:
                    st.info("Not enough data to determine the best player to partner with.")
            else:
                st.info("No doubles matches have been recorded yet.")

            st.markdown("---")

            # Most Frequent Player
            st.markdown("### 🏟️ Most Frequent Player")
            if not rank_df.empty:
                most_frequent_player = rank_df.sort_values(by="Matches", ascending=False).iloc[0]
                player_styled = f"<span style='font-weight:bold; color:#fff500;'>{most_frequent_player['Player']}</span>"
                st.markdown(f"{player_styled} has played the most matches, with a total of **{int(most_frequent_player['Matches'])}** matches played.", unsafe_allow_html=True)
            else:
                st.info("No match data available to determine the most frequent player.")

            st.markdown("---")

            # Player with highest Game Difference
            st.markdown("### 📈 Player with highest Game Difference")
            cumulative_game_diff = defaultdict(int)
            for _, row in matches.iterrows():
                t1 = [row['team1_player1'], row['team1_player2']] if row['match_type'] == 'Doubles' else [row['team1_player1']]
                t2 = [row['team2_player1'], row['team2_player2']] if row['match_type'] == 'Doubles' else [row['team2_player1']]
                for set_score in [row['set1'], row['set2'], row['set3']]:
                    if set_score and '-' in set_score:
                        try:
                            team1_games, team2_games = map(int, set_score.split('-'))
                            set_gd = team1_games - team2_games
                            for p in t1:
                                if p != "Visitor":
                                    cumulative_game_diff[p] += set_gd
                            for p in t2:
                                if p != "Visitor":
                                    cumulative_game_diff[p] -= set_gd
                        except ValueError:
                            continue

            if cumulative_game_diff:
                highest_gd_player, highest_gd_value = max(cumulative_game_diff.items(), key=lambda item: item[1])
                player_styled = f"<span style='font-weight:bold; color:#fff500;'>{highest_gd_player}</span>"
                st.markdown(f"{player_styled} has the highest cumulative game difference: <span style='font-weight:bold; color:#fff500;'>{highest_gd_value}</span>.", unsafe_allow_html=True)
            else:
                st.info("No match data available to calculate game difference.")

            st.markdown("---")

            # Player with the most wins
            st.markdown(f"### 👑 Player with the Most Wins")
            most_wins_player = rank_df.sort_values(by="Wins", ascending=False).iloc[0]
            player_styled = f"<span style='font-weight:bold; color:#fff500;'>{most_wins_player['Player']}</span>"
            st.markdown(f"{player_styled} holds the record for most wins with **{int(most_wins_player['Wins'])}** wins.", unsafe_allow_html=True)

            st.markdown("---") 

            # Player with the highest win percentage (minimum 5 matches)
            st.markdown(f"### 🔥 Highest Win Percentage (Min. 5 Matches)")
            eligible_players = rank_df[rank_df['Matches'] >= 5].sort_values(by="Win %", ascending=False)
            if not eligible_players.empty:
                highest_win_percent_player = eligible_players.iloc[0]
                player_styled = f"<span style='font-weight:bold; color:#fff500;'>{highest_win_percent_player['Player']}</span>"
                st.markdown(f"{player_styled} has the highest win percentage at **{highest_win_percent_player['Win %']:.2f}%**.", unsafe_allow_html=True)
            else:
                st.info("No players have played enough matches to calculate a meaningful win percentage.")

            st.markdown("---")
            st.markdown(f"### 🗓️ Community Activity : Last 7 Days ")    

            if 'matches_df' in st.session_state and not st.session_state.matches_df.empty:
                display_community_stats(st.session_state.matches_df)

            st.markdown("---")
            st.markdown("### 📊 Player Performance Overview")
            nerd_chart = create_nerd_stats_chart(rank_df)
            if nerd_chart:
                st.plotly_chart(nerd_chart, use_container_width=True)
            else:
                st.info("Not enough data to generate the performance chart.")
            # --- End of Inserted Chart Section ---
            # --- Start of new chart integration ---
            st.markdown("---")
            st.markdown("### 🤝 Partnership Performance Analyzer")

            # Get a list of players who have played doubles
            doubles_players = []
            if partner_stats:
                doubles_players = sorted([p for p in partner_stats.keys() if p != "Visitor"])

            if not doubles_players:
                st.info("No doubles match data available to analyze partnerships.")
            else:
                selected_player_for_partners = st.selectbox(
                    "Select a player to see their partnership stats:",
                    doubles_players
                )

                if selected_player_for_partners:
                    partnership_chart = create_partnership_chart(selected_player_for_partners, partner_stats, players_df)
                    if partnership_chart:
                        st.plotly_chart(partnership_chart, use_container_width=True)
                    else:
                        st.info(f"{selected_player_for_partners} has no partnership data to display.")

            # --- End of new chart integration ---

            st.markdown("---")
            with st.expander("Process being used for Rankings" , expanded=False, icon="➡️"):
                st.markdown("""
                ### Ranking System Overview
                - **Points**: Players earn 3 points for a win, 1 point for a loss, and 1.5 points for a tie.
                - **Win Percentage**: Calculated as (Wins / Matches Played) * 100.
                - **Game Difference Average**: The average difference in games won vs. lost per match.
                - **Games Won**: Total games won across all sets.
                - **Ranking Criteria**: Players are ranked by Points (highest first), then by Win Percentage, Game Difference Average, Games Won, and finally alphabetically by name.
                - **Matches Included**: All matches, including those with a 'Visitor', contribute to AR players' stats, but 'Visitor' is excluded from rankings and insights.

                Detailed Ranking Logic at https://github.com/mahadevbk/ar2/blob/main/ar_ranking_logic.pdf
                
                """)
    elif ranking_type == "Table View":
        # Calculate combined rankings
        rank_df_combined, _ = calculate_rankings(matches)
        display_rankings_table(rank_df_combined, "Combined")
        
        # Calculate doubles rankings
        doubles_matches = matches[matches['match_type'] == 'Doubles']
        rank_df_doubles, _ = calculate_rankings(doubles_matches)
        display_rankings_table(rank_df_doubles, "Doubles")
        
        # Calculate singles rankings
        singles_matches = matches[matches['match_type'] == 'Singles']
        rank_df_singles, _ = calculate_rankings(singles_matches)
        display_rankings_table(rank_df_singles, "Singles")
        
        # Add PDF download button
        st.markdown("---")
        st.subheader("Download Rankings as PDF")
        if st.button("Download All Rankings", key="download_rankings_pdf"):
            try:
                pdf_data = generate_pdf_reportlab(rank_df_combined, rank_df_doubles, rank_df_singles)
                st.download_button(
                    label="Download PDF",
                    data=pdf_data,
                    file_name="AR_Tennis_League_Rankings.pdf",
                    mime="application/pdf",
                    key="download_pdf_button"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
    else:  # Combined view
        filtered_matches = matches.copy()
        rank_df, partner_stats = calculate_rankings(filtered_matches)
        current_date_formatted = datetime.now().strftime("%d/%m")
        #st.subheader(f"Rankings as of {current_date_formatted}")

        # --- START: New Top 3 Players Display ---
        if not rank_df.empty and len(rank_df) >= 3:
            top_3_players = rank_df.head(3)
            
            # Custom CSS for the podium display
            st.markdown("""
            <style>
            .podium-container {
                display: flex;
                flex-direction: row;
                justify-content: space-around;
                align-items: flex-end;
                width: 100%;
                margin: 20px 0;
                padding: 10px 0;
                height: 220px;
                border-bottom: 2px solid #fff500;
            }
            .podium-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                color: white;
                width: 32%; /* Ensure they fit side-by-side */
            }
            .podium-item img {
                width: 90px;
                height: 90px;
                border-radius: 50%;
                border: 1px solid #fff500;
                transition: transform 0.2s;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4), 0 0 10px rgba(255, 245, 0, 0.6);
                margin-bottom: 10px;
                object-fit: cover;
            }
            .podium-name {
                font-weight: bold;
                font-size: 1.1em;
                color: #fff500;
            }
            .podium-rank {
                font-size: 1.5em;
                font-weight: bold;
                color: white;
            }
            /* Use flexbox order to arrange 2nd, 1st, 3rd */
            .podium-item.rank-1 { order: 2; align-self: flex-start; } /* Center and Top */
            .podium-item.rank-2 { order: 1; } /* Left */
            .podium-item.rank-3 { order: 3; } /* Right */
            </style>
            """, unsafe_allow_html=True)

            # Extract player data
            p1 = top_3_players.iloc[0]
            p2 = top_3_players.iloc[1]
            p3 = top_3_players.iloc[2]
            
            # Create the HTML structure
            podium_html = f"""
            <div class="podium-container">
                <div class="podium-item rank-2">
                    <img src="{p2['Profile']}" alt="{p2['Player']}">
                    <div class="podium-rank">🥈 {p2['Rank'].replace('🏆 ', '')}</div>
                    <div class="podium-name">{p2['Player']}</div>
                </div>
                <div class="podium-item rank-1">
                    <img src="{p1['Profile']}" alt="{p1['Player']}">
                    <div class="podium-rank">🥇 {p1['Rank'].replace('🏆 ', '')}</div>
                    <div class="podium-name">{p1['Player']}</div>
                </div>
                <div class="podium-item rank-3">
                    <img src="{p3['Profile']}" alt="{p3['Player']}">
                    <div class="podium-rank">🥉 {p3['Rank'].replace('🏆 ', '')}</div>
                    <div class="podium-name">{p3['Player']}</div>
                </div>
            </div>
            """
            st.markdown(podium_html, unsafe_allow_html=True)
        # --- END: New Top 3 Players Display ---
        
        st.markdown('<div class="rankings-table-container">', unsafe_allow_html=True)
        st.markdown('<div class="rankings-table-scroll">', unsafe_allow_html=True)
        if rank_df.empty:
            st.info("No ranking data available for this view.")
        else:
            for index, row in rank_df.iterrows():
                profile_html = f'<a href="{row["Profile"]}" target="_blank"><img src="{row["Profile"]}" class="profile-image" alt="Profile"></a>' if row["Profile"] else ''
                player_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['Player']}</span>"
                # matches styled 
                matches_styled = f"<span style='font-weight:bold; color:#fff500;'>{int(row['Matches'])} (Doubles: {int(row['Doubles Matches'])}, Singles: {int(row['Singles Matches'])})</span>"
                points_value_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['Points']:.1f}</span>"
                trend_value_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['Recent Trend']}</span>"
                st.markdown(f"""
                <div class="ranking-row">
                    <div class="rank-profile-player-group">
                        <div class="rank-col">{row["Rank"]}</div>
                        <div class="profile-col">{profile_html}</div>
                        <div class="player-col">{player_styled}</div>
                    </div>
                    <div class="points-col">{points_value_styled}</div>
                    <div class="win-percent-col">{row["Win %"]:.1f}%</div>
                    <div class="matches-col">{matches_styled}</div>
                    <div class="wins-col">{int(row["Wins"])}</div>
                    <div class="losses-col">{int(row["Losses"])}</div>
                    <div class="game-diff-avg-col">{row["Game Diff Avg"]:.2f}</div>
                    <div class="games-won-col">{int(row["Games Won"])}</div>
                    <div class="trend-col">{trend_value_styled}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.subheader("Player Insights")
        selected_player_rankings = st.selectbox("Select a player for insights", [""] + players, index=0, key="insights_player_rankings_combined")
        if selected_player_rankings:
            display_player_insights(selected_player_rankings, players_df, filtered_matches, rank_df, partner_stats, key_prefix="rankings_combined_")
        else:
            st.info("Player insights will be available once a player is selected.")

with tabs[1]:
    st.header("Matches")
    with st.expander("➕ Post New Match Result", expanded=False, icon="➡️"):
        st.subheader("Enter Match Result")
        match_type_new = st.radio("Match Type", ["Doubles", "Singles"], horizontal=True, key=f"post_match_type_new_{st.session_state.form_key_suffix}")
        available_players = sorted(players.copy() + ["Visitor"] if players else ["Visitor"])
        if not available_players:
            st.warning("No players available. Please add players in the Player Profile tab.")
        else:
            with st.form(key=f"new_match_form_{st.session_state.form_key_suffix}"):
                if match_type_new == "Doubles":
                    col1, col2 = st.columns(2)
                    with col1:
                        p1_new = st.selectbox("Team 1 - Player 1", [""] + available_players, key=f"t1p1_new_post_{st.session_state.form_key_suffix}")
                        p2_new = st.selectbox("Team 1 - Player 2", [""] + available_players, key=f"t1p2_new_post_{st.session_state.form_key_suffix}")
                    with col2:
                        p3_new = st.selectbox("Team 2 - Player 1", [""] + available_players, key=f"t2p1_new_post_{st.session_state.form_key_suffix}")
                        p4_new = st.selectbox("Team 2 - Player 2", [""] + available_players, key=f"t2p2_new_post_{st.session_state.form_key_suffix}")
                else:
                    p1_new = st.selectbox("Player 1", [""] + available_players, key=f"s1p1_new_post_{st.session_state.form_key_suffix}")
                    p3_new = st.selectbox("Player 2", [""] + available_players, key=f"s1p2_new_post_{st.session_state.form_key_suffix}")
                    p2_new = ""
                    p4_new = ""
                set1_new = st.selectbox("Set 1 *", tennis_scores(), index=4, key=f"set1_new_post_{st.session_state.form_key_suffix}")
                set2_new = st.selectbox("Set 2 *" if match_type_new == "Doubles" else "Set 2 (optional)", [""] + tennis_scores(), key=f"set2_new_post_{st.session_state.form_key_suffix}")
                set3_new = st.selectbox("Set 3 (optional)", [""] + tennis_scores(), key=f"set3_new_post_{st.session_state.form_key_suffix}")
                winner_new = st.radio("Winner", ["Team 1", "Team 2", "Tie"], key=f"winner_new_post_{st.session_state.form_key_suffix}")
                match_image_new = st.file_uploader("Upload Match Image (optional)", type=["jpg", "jpeg", "png", "gif", "bmp", "webp"], key=f"match_image_new_post_{st.session_state.form_key_suffix}")
                st.markdown("*Required fields", unsafe_allow_html=True)
                submit_button = st.form_submit_button("Submit Match")
            if submit_button:
                selected_players = [p1_new, p2_new, p3_new, p4_new] if match_type_new == "Doubles" else [p1_new, p3_new]
                if "" in selected_players:
                    st.error("Please select all players.")
                elif len(selected_players) != len(set(selected_players)):
                    st.error("Please select different players for each position.")
                elif not set1_new:
                    st.error("Set 1 score is required.")
                elif match_type_new == "Doubles" and not set2_new:
                    st.error("Set 2 score is required for doubles matches.")
                else:
                    new_match_date = datetime.now()
                    match_id_new = generate_match_id(st.session_state.matches_df, new_match_date)
                    image_url_new = ""
                    if match_image_new:
                        image_url_new = upload_image_to_supabase(match_image_new, match_id_new, image_type="match")
                    new_match_entry = {
                        "match_id": match_id_new,
                        "date": new_match_date,
                        "match_type": match_type_new,
                        "team1_player1": p1_new,
                        "team1_player2": p2_new,
                        "team2_player1": p3_new,
                        "team2_player2": p4_new,
                        "set1": set1_new,
                        "set2": set2_new,
                        "set3": set3_new,
                        "winner": winner_new,
                        "match_image_url": image_url_new
                    }
                    matches_to_save = pd.concat([st.session_state.matches_df, pd.DataFrame([new_match_entry])], ignore_index=True)
                    save_matches(matches_to_save)
                    load_matches()  # Reload data from DB
                    st.success("Match submitted.")
                    st.session_state.form_key_suffix += 1
                    st.rerun()

    #st.markdown("---")
    #st.markdown("---")
    #st.subheader("Match History")

    # Create columns for the filters
    col1_filter, col2_filter = st.columns(2)
    with col1_filter:
        match_filter = st.radio("Filter by Type", ["All", "Singles", "Doubles"], horizontal=True, key="match_history_filter")
    with col2_filter:
        player_search = st.selectbox("Filter by Player", ["All Players"] + players, key="player_search_filter")

    # Start with a clean copy of the matches
    filtered_matches = st.session_state.matches_df.copy()

    # Apply type filter first
    if match_filter != "All":
        filtered_matches = filtered_matches[filtered_matches["match_type"] == match_filter]

    # Apply player search filter on the result
    if player_search != "All Players":
        filtered_matches = filtered_matches[
            (filtered_matches['team1_player1'] == player_search) |
            (filtered_matches['team1_player2'] == player_search) |
            (filtered_matches['team2_player1'] == player_search) |
            (filtered_matches['team2_player2'] == player_search)
        ]

    # --- START: Robust Date Handling and Sorting ---
    if not filtered_matches.empty:
        # Convert date column, turning errors into NaT (Not a Time)
        filtered_matches['date'] = pd.to_datetime(filtered_matches['date'], errors='coerce')

        # Keep only the rows with valid dates
        valid_matches = filtered_matches.dropna(subset=['date']).copy()
        
        # If some rows were dropped, inform the user
        if len(valid_matches) < len(filtered_matches):
            st.warning("Some match records were hidden due to missing or invalid date formats in the database.")
        
        if not valid_matches.empty:
            # Sort ascending to assign serial numbers correctly (oldest = #1)
            valid_matches = valid_matches.sort_values(by='date', ascending=True).reset_index(drop=True)
            valid_matches['serial_number'] = valid_matches.index + 1
            
            # Re-sort descending for display (newest first)
            display_matches = valid_matches.sort_values(by='date', ascending=False).reset_index(drop=True)
        else:
            display_matches = pd.DataFrame() # Ensure an empty dataframe if no valid dates
    else:
        display_matches = pd.DataFrame()
    # --- END: Robust Date Handling and Sorting ---


    def format_match_players(row):
        if row["match_type"] == "Singles":
            p1_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['team1_player1']}</span>"
            p2_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['team2_player1']}</span>"
            if row["winner"] == "Tie":
                return f"{p1_styled} tied with {p2_styled}"
            elif row["winner"] == "Team 1":
                return f"{p1_styled} def. {p2_styled}"
            else:  # Team 2
                return f"{p2_styled} def. {p1_styled}"
        else:  # Doubles
            p1_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['team1_player1']}</span>"
            p2_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['team1_player2']}</span>"
            p3_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['team2_player1']}</span>"
            p4_styled = f"<span style='font-weight:bold; color:#fff500;'>{row['team2_player2']}</span>"
            if row["winner"] == "Tie":
                return f"{p1_styled} & {p2_styled} tied with {p3_styled} & {p4_styled}"
            elif row["winner"] == "Team 1":
                return f"{p1_styled} & {p2_styled} def. {p3_styled} & {p4_styled}"
            else:  # Team 2
                return f"{p3_styled} & {p4_styled} def. {p1_styled} & {p2_styled}"


    def format_match_scores_and_date(row):
        score_parts_plain = []
        for s in [row['set1'], row['set2'], row['set3']]:
            if s:
                if "Tie Break" in s:
                    tie_break_scores = s.replace("Tie Break", "").strip().split('-')
                    if int(tie_break_scores[0]) > int(tie_break_scores[1]):
                        score_parts_plain.append(f"7-6({s})")
                    else:
                        score_parts_plain.append(f"6-7({s})")
                else:
                    score_parts_plain.append(s)

        score_text = ", ".join(score_parts_plain)
        target_width = 23
        padding_spaces = " " * (target_width - len(score_text))
        
        score_parts_html = [f"<span style='font-weight:bold; color:#fff500;'>{s}</span>" for s in score_parts_plain]
        score_html = ", ".join(score_parts_html)
        
        if pd.notna(row['date']):
            date_str = row['date'].strftime('%A, %d %b')
        else:
            date_str = "Invalid Date"
            
        return f"<div style='font-family: monospace; white-space: pre;'>{score_html}{padding_spaces}{date_str}</div>"

    if display_matches.empty:
        st.info("No matches found for the selected filters.")
    else:
        for index, row in display_matches.iterrows():
            # Create four columns: serial number, image, match details, and share button
            cols = st.columns([1, 1, 7, 1])
            with cols[0]:
                # Display serial number
                st.markdown(f"<span style='font-weight:bold; color:#fff500;'>{row['serial_number']}</span>", unsafe_allow_html=True)
            with cols[1]:
                if row["match_image_url"]:
                    try:
                        st.image(row["match_image_url"], width=50, caption="")
                    except Exception as e:
                        st.error(f"Error displaying match image: {str(e)}")
            with cols[2]:
                st.markdown(f"{format_match_players(row)}", unsafe_allow_html=True)
                st.markdown(format_match_scores_and_date(row), unsafe_allow_html=True)
            with cols[3]:
                share_link = generate_whatsapp_link(row)
                st.markdown(f'<a href="{share_link}" target="_blank" style="text-decoration:none; color:#ffffff;"><img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp Share" style="width:30px;height:30px;"/></a>', unsafe_allow_html=True)
            st.markdown("<hr style='border-top: 1px solid #333333; margin: 10px 0;'>", unsafe_allow_html=True)
# ... (rest of the code remains unchanged)

    st.markdown("---")
   
    st.markdown("---")
   
    st.subheader("✏️ Manage Existing Match")
    clean_match_options = []
    # Note: We are using 'display_matches' which is already sorted with the latest first
    for _, row in display_matches.iterrows():
        score_plain = f"{row['set1']}"
        if row['set2']:
            score_plain += f", {row['set2']}"
        if row['set3']:
            score_plain += f", {row['set3']}"

        if pd.notna(row['date']):
            date_plain = row['date'].strftime('%d %b %y %H:%M')
        else:
            date_plain = "Invalid Date"
            
        if row["match_type"] == "Singles":
            if row["winner"] == "Tie":
                desc_plain = f"{row['team1_player1']} tied with {row['team2_player1']}"
            elif row["winner"] == "Team 1":
                desc_plain = f"{row['team1_player1']} def. {row['team2_player1']}"
            else:  # Team 2
                desc_plain = f"{row['team2_player1']} def. {row['team1_player1']}"
        else:  # Doubles
            if row["winner"] == "Tie":
                desc_plain = f"{row['team1_player1']} & {row['team1_player2']} tied with {row['team2_player1']} & {row['team2_player2']}"
            elif row["winner"] == "Team 1":
                desc_plain = f"{row['team1_player1']} & {row['team1_player2']} def. {row['team2_player1']} & {row['team2_player2']}"
            else:  # Team 2
                desc_plain = f"{row['team2_player1']} & {row['team2_player2']} def. {row['team1_player1']} & {row['team1_player2']}"
        clean_match_options.append(f"{desc_plain} | {score_plain} | {date_plain} | {row['match_id']}")
    
    # Use a unique key to avoid conflicts
    selected_match_to_edit = st.selectbox("Select a match to edit or delete", [""] + clean_match_options, key="select_match_to_edit_1")
    if selected_match_to_edit:
        selected_id = selected_match_to_edit.split(" | ")[-1]
        # Use display_matches which is the final sorted and valid dataframe
        row = display_matches[display_matches["match_id"] == selected_id].iloc[0]
        idx = st.session_state.matches_df[st.session_state.matches_df["match_id"] == selected_id].index[0]
        current_date_dt = pd.to_datetime(row["date"])
        all_scores = [""] + tennis_scores()
        set1_index = all_scores.index(row["set1"]) if row["set1"] in all_scores else 0
        set2_index = all_scores.index(row["set2"]) if row["set2"] in all_scores else 0
        set3_index = all_scores.index(row["set3"]) if row["set3"] in all_scores else 0
        with st.expander("Edit Match Details"):
            date_edit = st.date_input("Match Date", value=current_date_dt.date(), key=f"edit_date_{selected_id}")
            time_edit = st.time_input("Match Time", value=current_date_dt.time(), key=f"edit_time_{selected_id}")
            match_type_edit = st.radio("Match Type", ["Doubles", "Singles"], index=0 if row["match_type"] == "Doubles" else 1, key=f"edit_match_type_{selected_id}")
            
            # Conditionally render player selectboxes based on match type
            if match_type_edit == "Doubles":
                col1, col2 = st.columns(2)
                with col1:
                    p1_edit = st.selectbox("Team 1 - Player 1", [""] + available_players, index=available_players.index(row["team1_player1"]) + 1 if row["team1_player1"] in available_players else 0, key=f"edit_t1p1_{selected_id}")
                    p2_edit = st.selectbox("Team 1 - Player 2", [""] + available_players, index=available_players.index(row["team1_player2"]) + 1 if row["team1_player2"] in available_players else 0, key=f"edit_t1p2_{selected_id}")
                with col2:
                    p3_edit = st.selectbox("Team 2 - Player 1", [""] + available_players, index=available_players.index(row["team2_player1"]) + 1 if row["team2_player1"] in available_players else 0, key=f"edit_t2p1_{selected_id}")
                    p4_edit = st.selectbox("Team 2 - Player 2", [""] + available_players, index=available_players.index(row["team2_player2"]) + 1 if row["team2_player2"] in available_players else 0, key=f"edit_t2p2_{selected_id}")
            else:  # Singles
                p1_edit = st.selectbox("Player 1", [""] + available_players, index=available_players.index(row["team1_player1"]) + 1 if row["team1_player1"] in available_players else 0, key=f"edit_t1p1_{selected_id}")
                p3_edit = st.selectbox("Player 2", [""] + available_players, index=available_players.index(row["team2_player1"]) + 1 if row["team2_player1"] in available_players else 0, key=f"edit_t2p1_{selected_id}")
                p2_edit = ""  # Explicitly set to empty for Singles
                p4_edit = ""  # Explicitly set to empty for Singles
            
            set1_edit = st.selectbox("Set 1", all_scores, index=set1_index, key=f"edit_set1_{selected_id}")
            set2_edit = st.selectbox("Set 2 (optional)", all_scores, index=set2_index, key=f"edit_set2_{selected_id}")
            set3_edit = st.selectbox("Set 3 (optional)", all_scores, index=set3_index, key=f"edit_set3_{selected_id}")
            winner_edit = st.selectbox("Winner", ["Team 1", "Team 2", "Tie"], index=["Team 1", "Team 2", "Tie"].index(row["winner"]), key=f"edit_winner_{selected_id}")
            match_image_edit = st.file_uploader("Update Match Image (optional)", type=["jpg", "jpeg", "png", "gif", "bmp", "webp"], key=f"edit_image_{selected_id}")
            if st.button("Save Changes", key=f"save_match_changes_{selected_id}"):
                image_url_edit = row["match_image_url"]
                if match_image_edit:
                    image_url_edit = upload_image_to_supabase(match_image_edit, selected_id, image_type="match")
                combined_datetime = datetime.combine(date_edit, time_edit)
                st.session_state.matches_df.loc[idx] = {
                    "match_id": selected_id,
                    "date": combined_datetime,
                    "match_type": match_type_edit,
                    "team1_player1": p1_edit,
                    "team1_player2": p2_edit,
                    "team2_player1": p3_edit,
                    "team2_player2": p4_edit,
                    "set1": set1_edit,
                    "set2": set2_edit,
                    "set3": set3_edit,
                    "winner": winner_edit,
                    "match_image_url": image_url_edit
                }
                save_matches(st.session_state.matches_df)
                load_matches()
                st.success("Match updated.")
                st.rerun()
            if st.button("🗑️ Delete This Match", key=f"delete_match_{selected_id}"):
                delete_match_from_db(selected_id)
                load_matches()
                st.success("Match deleted.")
                st.rerun()

# Player Profile tab
with tabs[2]:
    st.header("Player Profile")
    #st.subheader("Add or Edit Player Profiles")
    with st.expander("Add, Edit or Remove Player", expanded=False, icon="➡️"):
        st.markdown("##### Add New Player")
        new_player = st.text_input("Player Name", key="new_player_input").strip()
        if st.button("Add Player", key="add_player_button"):
            if new_player:
                if new_player.lower() == "visitor":
                    st.warning("The name 'Visitor' is reserved and cannot be added.")
                elif new_player in st.session_state.players_df["name"].tolist():
                    st.warning(f"{new_player} already exists.")
                else:
                    new_player_data = {"name": new_player, "profile_image_url": "", "birthday": ""}
                    st.session_state.players_df = pd.concat([st.session_state.players_df, pd.DataFrame([new_player_data])], ignore_index=True)
                    save_players(st.session_state.players_df)
                    load_players()
                    st.success(f"{new_player} added.")
                    st.rerun()
            else:
                st.warning("Please enter a player name to add.")
        st.markdown("---")
        st.markdown("##### Edit or Remove Existing Player")
        players = sorted([p for p in st.session_state.players_df["name"].dropna().tolist() if p != "Visitor"]) if "name" in st.session_state.players_df.columns else []
        if not players:
            st.info("No players available. Add a new player to begin.")
        else:
            selected_player_manage = st.selectbox("Select Player", [""] + players, key="manage_player_select")
            if selected_player_manage:
                player_data = st.session_state.players_df[st.session_state.players_df["name"] == selected_player_manage].iloc[0]
                current_image = player_data.get("profile_image_url", "")
                current_birthday = player_data.get("birthday", "")
                st.markdown(f"**Current Profile for {selected_player_manage}**")
                if current_image:
                    st.image(current_image, width=100)
                else:
                    st.write("No profile image set.")
                profile_image = st.file_uploader("Upload New Profile Image (optional)", type=["jpg", "jpeg", "png", "gif", "bmp", "webp"], key=f"profile_image_upload_{selected_player_manage}")
                default_day = 1
                default_month = 1
                if current_birthday and isinstance(current_birthday, str) and re.match(r'^\d{2}-\d{2}$', current_birthday):
                    try:
                        day_str, month_str = current_birthday.split("-")
                        default_day = int(day_str)
                        default_month = int(month_str)
                    except (ValueError, IndexError):
                        pass
                birthday_day = st.number_input("Birthday Day", min_value=1, max_value=31, value=default_day, key=f"birthday_day_{selected_player_manage}")
                birthday_month = st.number_input("Birthday Month", min_value=1, max_value=12, value=default_month, key=f"birthday_month_{selected_player_manage}")
                col_save, col_delete = st.columns(2)
                with col_save:
                    if st.button("Save Profile Changes", key=f"save_profile_changes_{selected_player_manage}"):
                        image_url = current_image
                        if profile_image:
                            image_url = upload_image_to_supabase(profile_image, f"profile_{selected_player_manage}_{uuid.uuid4().hex[:6]}", image_type="profile")
                        st.session_state.players_df.loc[st.session_state.players_df["name"] == selected_player_manage, "profile_image_url"] = image_url
                        st.session_state.players_df.loc[st.session_state.players_df["name"] == selected_player_manage, "birthday"] = f"{birthday_day:02d}-{birthday_month:02d}"
                        save_players(st.session_state.players_df)
                        load_players()
                        st.success(f"Profile for {selected_player_manage} updated.")
                        st.rerun()
                with col_delete:
                    if st.button("Remove Player", key=f"remove_player_{selected_player_manage}"):
                        if selected_player_manage.lower() == "visitor":
                            st.warning("The 'Visitor' player cannot be removed.")
                        else:
                            # Check for associated matches
                            if st.session_state.matches_df[
                                (st.session_state.matches_df["team1_player1"] == selected_player_manage) |
                                (st.session_state.matches_df["team1_player2"] == selected_player_manage) |
                                (st.session_state.matches_df["team2_player1"] == selected_player_manage) |
                                (st.session_state.matches_df["team2_player2"] == selected_player_manage)
                            ].shape[0] > 0:
                                st.warning(f"Cannot delete {selected_player_manage} because they have associated matches. Delete their matches first.")
                            else:
                                delete_player_from_db(selected_player_manage)
                                st.session_state.players_df = st.session_state.players_df[st.session_state.players_df["name"] != selected_player_manage].reset_index(drop=True)
                                save_players(st.session_state.players_df)
                                load_players()
                                st.success(f"{selected_player_manage} removed.")
                                st.rerun()
    st.markdown("---")
    st.header("Player Insights")
    rank_df_combined, partner_stats_combined = calculate_rankings(st.session_state.matches_df)
    if players:
        display_player_insights(players, st.session_state.players_df, st.session_state.matches_df, rank_df_combined, partner_stats_combined, key_prefix="profile_")
    else:
        st.info("No players available for insights. Please add players above.")

with tabs[3]:
    st.header("Court Locations")
    
    # Icon URL (use a free tennis court icon; you can host it or use an external link)
    court_icon_url = "https://img.icons8.com/color/48/000000/tennis.png"  # Example from Icons8; replace if needed
    
    # Arabian Ranches courts (as a list of dicts for name and URL)
    ar_courts = [
        {"name": "Alvorado 1", "url": "https://maps.google.com/?q=25.041792,55.259258"},
        {"name": "Alvorado 2", "url": "https://maps.google.com/?q=25.041792,55.259258"},
        {"name": "Palmera 2", "url": "https://maps.app.goo.gl/CHimjtqQeCfU1d3W6"},
        {"name": "Palmera 4", "url": "https://maps.app.goo.gl/4nn1VzqMpgVkiZGN6"},
        {"name": "Saheel", "url": "https://maps.app.goo.gl/a7qSvtHCtfgvJoxJ8"},
        {"name": "Hattan", "url": "https://maps.app.goo.gl/fjGpeNzncyG1o34c7"},
        {"name": "MLC Mirador La Colleccion", "url": "https://maps.app.goo.gl/n14VSDAVFZ1P1qEr6"},
        {"name": "Al Mahra", "url": "https://maps.app.goo.gl/zVivadvUsD6yyL2Y9"},
        {"name": "Mirador", "url": "https://maps.app.goo.gl/kVPVsJQ3FtMWxyKP8"},
        {"name": "Reem 1", "url": "https://maps.app.goo.gl/qKswqmb9Lqsni5RD7"},
        {"name": "Reem 2", "url": "https://maps.app.goo.gl/oFaUFQ9DRDMsVbMu5"},
        {"name": "Reem 3", "url": "https://maps.app.goo.gl/o8z9pHo8tSqTbEL39"},
        {"name": "Alma", "url": "https://maps.app.goo.gl/BZNfScABbzb3osJ18"},
    ]
    
    # Mira & Mira Oasis courts
    mira_courts = [
        {"name": "Mira 2", "url": "https://maps.app.goo.gl/JeVmwiuRboCnzhnb9"},
        {"name": "Mira 4", "url": "https://maps.app.goo.gl/e1Vqv5MJXB1eusv6A"},
        {"name": "Mira 5 A", "url": "https://maps.app.goo.gl/rWBj5JEUdw4LqJZb6"},
        {"name": "Mira 5 B", "url": "https://maps.app.goo.gl/rWBj5JEUdw4LqJZb6"},
        {"name": "Mira Oasis 1", "url": "https://maps.app.goo.gl/F9VYsFBwUCzvdJ2t8"},
        {"name": "Mira Oasis 2", "url": "https://maps.app.goo.gl/ZNJteRu8aYVUy8sd9"},
        {"name": "Mira Oasis 3 A", "url": "https://maps.app.goo.gl/ouXQGUxYSZSfaW1z9"},
        {"name": "Mira Oasis 3 B", "url": "https://maps.app.goo.gl/ouXQGUxYSZSfaW1z9"},
        {"name": "Mira Oasis 3 C", "url": "https://maps.app.goo.gl/kf7A9K7DoYm4PEPu8"},
    ]
    
    # Function to display courts in a grid
    def display_courts(section_title, courts_list):
        st.subheader(section_title)
        num_cols = 3 if len(courts_list) > 6 else 2  # Responsive: 2-3 columns based on list length
        for i in range(0, len(courts_list), num_cols):
            cols = st.columns(num_cols)
            for j, court in enumerate(courts_list[i:i+num_cols]):
                with cols[j]:
                    st.markdown(f"""
                    <div class="court-card">
                        <img src="{court_icon_url}" class="court-icon" alt="Tennis Court Icon">
                        <h4>{court['name']}</h4>
                        <a href="{court['url']}" target="_blank">View on Map</a>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Display sections
    with st.expander("Arabian Ranches Tennis Courts", expanded=False, icon="➡️"):
        display_courts("", ar_courts)  # No extra title inside expander
    with st.expander("Mira & Mira Oasis Tennis Courts", expanded=False, icon="➡️"):
        display_courts("", mira_courts)

        
#-----TAB 4 WITH THUMBNAILS INSIDE BOOKING BOX AND WHATSAPP SHARE WITH PROPER FORMATTING--------------------------------------------




with tabs[4]:
    load_bookings()
    with st.expander("Add New Booking", expanded=False, icon="➡️"):
        st.subheader("Add New Booking")
        match_type = st.radio("Match Type", ["Doubles", "Singles"], index=0, key=f"new_booking_match_type_{st.session_state.form_key_suffix}")
        
        with st.form(key=f"add_booking_form_{st.session_state.form_key_suffix}"):
            date = st.date_input("Booking Date *", value=datetime.today())
            hours = [datetime.strptime(f"{h}:00", "%H:%M").strftime("%-I:00 %p") for h in range(6, 22)]
            time = st.selectbox("Booking Time *", hours, key=f"new_booking_time_{st.session_state.form_key_suffix}")
            
            if match_type == "Doubles":
                col1, col2 = st.columns(2)
                with col1:
                    p1 = st.selectbox("Player 1 (optional)", [""] + available_players, key=f"t1p1_{st.session_state.form_key_suffix}")
                    p2 = st.selectbox("Player 2 (optional)", [""] + available_players, key=f"t1p2_{st.session_state.form_key_suffix}")
                with col2:
                    p3 = st.selectbox("Player 3 (optional)", [""] + available_players, key=f"t2p1_{st.session_state.form_key_suffix}")
                    p4 = st.selectbox("Player 4 (optional)", [""] + available_players, key=f"t2p2_{st.session_state.form_key_suffix}")
            else:
                p1 = st.selectbox("Player 1 (optional)", [""] + available_players, key=f"s1p1_{st.session_state.form_key_suffix}")
                p3 = st.selectbox("Player 2 (optional)", [""] + available_players, key=f"s1p2_{st.session_state.form_key_suffix}")
                p2 = ""
                p4 = ""
            
            standby = st.selectbox("Standby Player (optional)", [""] + available_players, key=f"standby_{st.session_state.form_key_suffix}")
            court = st.selectbox("Court Name *", [""] + court_names, key=f"court_{st.session_state.form_key_suffix}")
            screenshot = st.file_uploader("Booking Screenshot (optional)", type=["jpg", "jpeg", "png", "gif", "bmp", "webp"], key=f"screenshot_{st.session_state.form_key_suffix}")
            st.markdown("*Required fields", unsafe_allow_html=True)
            
            submit = st.form_submit_button("Add Booking")
            if submit:
                if not court:
                    st.error("Court name is required.")
                elif not date or not time:
                    st.error("Booking date and time are required.")
                else:
                    selected_players = [p for p in [p1, p2, p3, p4, standby] if p]
                    if match_type == "Doubles" and len(set(selected_players)) != len(selected_players):
                        st.error("Please select different players for each position.")
                    else:
                        booking_id = str(uuid.uuid4())
                        screenshot_url = upload_image_to_supabase(screenshot, booking_id, image_type="booking") if screenshot else None
                        time_24hr = datetime.strptime(time, "%I:%M %p").strftime("%H:%M")
                        new_booking = {
                            "booking_id": booking_id,
                            "date": date.isoformat(),
                            "time": time_24hr,
                            "match_type": match_type,
                            "court_name": court,
                            "player1": p1 if p1 else None,
                            "player2": p2 if p2 else None,
                            "player3": p3 if p3 else None,
                            "player4": p4 if p4 else None,
                            "standby_player": standby if standby else None,
                            "screenshot_url": screenshot_url
                        }
                        st.session_state.bookings_df = pd.concat([st.session_state.bookings_df, pd.DataFrame([new_booking])], ignore_index=True)
                        try:
                            expected_columns = ['booking_id', 'date', 'time', 'match_type', 'court_name', 'player1', 'player2', 'player3', 'player4', 'standby_player', 'screenshot_url']
                            bookings_to_save = st.session_state.bookings_df[expected_columns].copy()
                            for col in ['player1', 'player2', 'player3', 'player4', 'standby_player', 'screenshot_url']:
                                bookings_to_save[col] = bookings_to_save[col].replace("", None)
                            save_bookings(bookings_to_save)
                            load_bookings()
                            st.success("Booking added successfully.")
                            st.session_state.form_key_suffix += 1
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to save booking: {str(e)}")
                            st.rerun()
    
    st.markdown("---")
    
    st.subheader("📅 Upcoming Bookings")
    bookings_df = st.session_state.bookings_df.copy()
    court_url_mapping = {court["name"]: court["url"] for court in ar_courts + mira_courts}
    if bookings_df.empty:
        st.info("No upcoming bookings found.")
    else:
        if 'standby_player' not in bookings_df.columns:
            bookings_df['standby_player'] = ""
        if 'standby' in bookings_df.columns:
            bookings_df = bookings_df.drop(columns=['standby'])
        if 'players' in bookings_df.columns:
            bookings_df = bookings_df.drop(columns=['players'])
        
        # Create datetime column
        bookings_df['datetime'] = pd.to_datetime(
            bookings_df['date'].astype(str) + ' ' + bookings_df['time'],
            errors='coerce',
            utc=True
        ).dt.tz_convert('Asia/Dubai')
        
        # Filter upcoming bookings
        upcoming_bookings = bookings_df[
            (bookings_df['datetime'].notna()) & 
            (bookings_df['datetime'] >= pd.Timestamp.now(tz='Asia/Dubai'))
        ].sort_values('datetime')
        
        if upcoming_bookings.empty:
            st.info("No upcoming bookings found.")
        else:
            # =====================================================================
            # START: MODIFICATION FOR NEW ODDS CALCULATION
            # =====================================================================
            try:
                # Calculate format-specific rankings for odds calculation
                doubles_matches_df = st.session_state.matches_df[st.session_state.matches_df['match_type'] == 'Doubles']
                singles_matches_df = st.session_state.matches_df[st.session_state.matches_df['match_type'] == 'Singles']
                
                doubles_rank_df, _ = calculate_rankings(doubles_matches_df)
                singles_rank_df, _ = calculate_rankings(singles_matches_df)
            except Exception as e:
                doubles_rank_df = pd.DataFrame()
                singles_rank_df = pd.DataFrame()
                st.warning(f"Unable to load rankings for pairing suggestions: {str(e)}")
            # =====================================================================
            # END: MODIFICATION FOR NEW ODDS CALCULATION
            # =====================================================================

            for _, row in upcoming_bookings.iterrows():
                players = [p for p in [row['player1'], row['player2'], row['player3'], row['player4']] if p]
                players_str = ", ".join([f"<span style='font-weight:bold; color:#fff500;'>{p}</span>" for p in players]) if players else "No players specified"
                standby_str = f"<span style='font-weight:bold; color:#fff500;'>{row['standby_player']}</span>" if row['standby_player'] else "None"
                date_str = pd.to_datetime(row['date']).strftime('%A, %d %b')
                ###time_ampm = datetime.strptime(row['time'], "%H:%M").strftime("%-I:%M %p")
                time_value = str(row['time']).strip()

                time_ampm = ""
                if time_value and time_value not in ["NaT", "nan", "None"]:
                    try:
                        # Try HH:MM
                        dt_obj = datetime.strptime(time_value, "%H:%M")
                    except ValueError:
                        try:
                            # Try HH:MM:SS
                            dt_obj = datetime.strptime(time_value, "%H:%M:%S")
                        except ValueError:
                            dt_obj = None
                    
                    if dt_obj:
                        time_ampm = dt_obj.strftime("%-I:%M %p")  # e.g. 2:30 PM
                
                court_url = court_url_mapping.get(row['court_name'], "#")
                court_name_html = f"<a href='{court_url}' target='_blank' style='font-weight:bold; color:#fff500; text-decoration:none;'>{row['court_name']}</a>"
    
                pairing_suggestion = ""
                plain_suggestion = ""
                try:
                    # =====================================================================
                    # START: MODIFICATION FOR NEW ODDS CALCULATION
                    # =====================================================================
                    if row['match_type'] == "Doubles" and len(players) == 4:
                        suggested_pairing, team1_odds, team2_odds = suggest_balanced_pairing(players, doubles_rank_df)
                        if team1_odds is not None and team2_odds is not None:
                            teams = suggested_pairing.split(' vs ')
                            team1_players = teams[0].replace('Team 1: ', '')
                            team2_players = teams[1].replace('Team 2: ', '')
                            pairing_suggestion = (
                                f"<div><strong style='color:white;'>Suggested Pairing:</strong> "
                                f"<span style='font-weight:bold;'>{team1_players}</span> (<span style='font-weight:bold; color:#fff500;'>{team1_odds:.1f}%</span>) vs "
                                f"<span style='font-weight:bold;'>{team2_players}</span> (<span style='font-weight:bold; color:#fff500;'>{team2_odds:.1f}%</span>)</div>"
                            )
                            plain_suggestion = f"\n*Suggested Pairing: {re.sub(r'<.*?>', '', team1_players)} ({team1_odds:.1f}%) vs {re.sub(r'<.*?>', '', team2_players)} ({team2_odds:.1f}%)*"
                        else:
                            pairing_suggestion = (
                                f"<div><strong style='color:white;'>Suggested Pairing:</strong> "
                                f"<span style='font-weight:bold;'>{suggested_pairing}</span></div>"
                            )
                            plain_suggestion = f"\n*Suggested Pairing: {re.sub(r'<.*?>', '', suggested_pairing).replace('Suggested Pairing: ', '').strip()}*"
                    elif row['match_type'] == "Singles" and len(players) == 2:
                        p1_odds, p2_odds = suggest_singles_odds(players, singles_rank_df)
                        if p1_odds is not None:
                            p1_styled = f"<span style='font-weight:bold; color:#fff500;'>{players[0]}</span>"
                            p2_styled = f"<span style='font-weight:bold; color:#fff500;'>{players[1]}</span>"
                            pairing_suggestion = (
                                f"<div><strong style='color:white;'>Odds:</strong> "
                                f"<span style='font-weight:bold;'>{p1_styled}</span> ({p1_odds:.1f}%) vs "
                                f"<span style='font-weight:bold;'>{p2_styled}</span> ({p2_odds:.1f}%)</div>"
                            )
                            plain_suggestion = f"\n*Odds: {players[0]} ({p1_odds:.1f}%) vs {players[1]} ({p2_odds:.1f}%)*"
                    # =====================================================================
                    # END: MODIFICATION FOR NEW ODDS CALCULATION
                    # =====================================================================
                    elif row['match_type'] == "Doubles" and len(players) < 4:
                        pairing_suggestion = "<div><strong style='color:white;'>Suggested Pairing:</strong> Not enough players for pairing suggestion</div>"
                        plain_suggestion = "\n*Suggested Pairing: Not enough players for pairing suggestion*"
                except Exception as e:
                    pairing_suggestion = f"<div><strong style='color:white;'>Suggestion:</strong> Error calculating: {e}</div>"
                    plain_suggestion = f"\n*Suggestion: Error calculating: {str(e)}*"

                weekday = pd.to_datetime(row['date']).strftime('%a')
                date_part = pd.to_datetime(row['date']).strftime('%d %b')
                full_date = f"{weekday} , {date_part} , {time_ampm}"
                court_name = row['court_name']
                players_list = "\n".join([f"{i+1}. *{p}*" for i, p in enumerate(players)]) if players else "No players"
                standby_text = f"\nSTD. BY : *{row['standby_player']}*" if row['standby_player'] else ""
                
                share_text = f"*Game Booking :* \nDate : *{full_date}* \nCourt : *{court_name}*\nPlayers :\n{players_list}{standby_text}{plain_suggestion}\nCourt location : {court_url}"
                encoded_text = urllib.parse.quote(share_text)
                whatsapp_link = f"https://api.whatsapp.com/send/?text={encoded_text}&type=custom_url&app_absent=0"
    
                booking_text = f"""
                <div class="booking-row" style='background-color: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
                    <div><strong>Date:</strong> <span style='font-weight:bold; color:#fff500;'>{date_str}</span></div>
                    <div><strong>Court:</strong> {court_name_html}</div>
                    <div><strong>Time:</strong> <span style='font-weight:bold; color:#fff500;'>{time_ampm}</span></div>
                    <div><strong>Match Type:</strong> <span style='font-weight:bold; color:#fff500;'>{row['match_type']}</span></div>
                    <div><strong>Players:</strong> {players_str}</div>
                    <div><strong>Standby Player:</strong> {standby_str}</div>
                    {pairing_suggestion}
                    <div style="margin-top: 10px;">
                        <a href="{whatsapp_link}" class="whatsapp-share" target="_blank">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" style="width: 30px; height: 30px;">
                        </a>
                    </div>
                """
    
                visuals_html = '<div style="display: flex; flex-direction: row; align-items: center; margin-top: 10px;">'
                screenshot_url = row["screenshot_url"] if row["screenshot_url"] and isinstance(row["screenshot_url"], str) else None
                if screenshot_url:
                    visuals_html += f'<a href="{screenshot_url}" target="_blank"><img src="{screenshot_url}" style="width:120px; margin-right:20px; cursor:pointer;" title="Click to view full-size"></a>'
                visuals_html += '<div style="display: flex; flex-direction: row; align-items: center; flex-wrap: nowrap;">'
                booking_players = [row['player1'], row['player2'], row['player3'], row['player4'], row.get('standby_player', '')]
                players_df = st.session_state.players_df
                image_urls = []
                placeholder_initials = []
                for player_name in booking_players:
                    if player_name and isinstance(player_name, str) and player_name.strip() and player_name != "Visitor":
                        player_data = players_df[players_df["name"] == player_name]
                        if not player_data.empty:
                            img_url = player_data.iloc[0].get("profile_image_url")
                            if img_url and isinstance(img_url, str) and img_url.strip():
                                image_urls.append((player_name, img_url))
                            else:
                                placeholder_initials.append((player_name, player_name[0].upper()))
                for player_name, img_url in image_urls:
                    visuals_html += f'<img src="{img_url}" class="profile-image" style="width: 50px; height: 50px; margin-right: 8px;" title="{player_name}">'
                for player_name, initial in placeholder_initials:
                    visuals_html += f'<div title="{player_name}" style="width: 50px; height: 50px; margin-right: 8px; border-radius: 50%; background-color: #07314f; border: 2px solid #fff500; display: flex; align-items: center; justify-content: center; font-size: 22px; color: #fff500; font-weight: bold;">{initial}</div>'
                visuals_html += '</div></div>'
                booking_text += visuals_html + '</div>'
    
                try:
                    st.markdown(booking_text, unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"Failed to render HTML for booking {row['booking_id']}: {str(e)}")
                    st.markdown(f"""
                    **Court:** {court_name_html}  
                    **Date:** {date_str}  
                    **Time:** {time_ampm}  
                    **Match Type:** {row['match_type']}  
                    **Players:** {', '.join(players) if players else 'No players'}  
                    **Standby Player:** {row.get('standby_player', 'None')}  
                    {pairing_suggestion.replace('<div><strong style="color:white;">', '**').replace('</strong>', '**').replace('</div>', '').replace('<span style="font-weight:bold; color:#fff500;">', '').replace('</span>', '')}
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <a href="{whatsapp_link}" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" style="width:30px; height:30px; vertical-align:middle; margin-top:10px;">
                    </a>
                    """, unsafe_allow_html=True)
                    if screenshot_url:
                        st.markdown(f"""
                        <a href="{screenshot_url}" target="_blank">
                            <img src="{screenshot_url}" style="width:120px; cursor:pointer;" title="Click to view full-size">
                        </a>
                        """, unsafe_allow_html=True)
                    if image_urls or placeholder_initials:
                        cols = st.columns(len(image_urls) + len(placeholder_initials))
                        col_idx = 0
                        for player_name, img_url in image_urls:
                            with cols[col_idx]:
                                st.image(img_url, width=50, caption=player_name)
                            col_idx += 1
                        for player_name, initial in placeholder_initials:
                            with cols[col_idx]:
                                st.markdown(f"""
                                <div style='width: 50px; height: 50px; border-radius: 50%; background-color: #07314f; border: 2px solid #fff500; display: flex; align-items: center; justify-content: center; font-size: 22px; color: #fff500; font-weight: bold;'>{initial}</div>
                                <div style='text-align: center;'>{player_name}</div>
                                """, unsafe_allow_html=True)
                            col_idx += 1
    
            #st.markdown("<hr style='border-top: 1px solid #333333; margin: 15px 0;'>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("✏️ Manage Existing Booking")
    if 'edit_booking_key' not in st.session_state:
        st.session_state.edit_booking_key = 0
    unique_key = f"select_booking_to_edit_{st.session_state.edit_booking_key}"
    
    if bookings_df.empty:
        st.info("No bookings available to manage.")
    else:
        # Check for duplicate booking_ids
        duplicate_ids = bookings_df[bookings_df.duplicated(subset=['booking_id'], keep=False)]['booking_id'].unique()
        if len(duplicate_ids) > 0:
            st.warning(f"Found duplicate booking_id values: {duplicate_ids.tolist()}. Please remove duplicates in Supabase before editing.")
        else:
            booking_options = []
    
            # --- Safe time formatting helper ---
            def format_time_safe(time_str):
                if not time_str or str(time_str).lower() in ["nat", "nan", "none"]:
                    return "Unknown Time"
                t = str(time_str).strip()
                for fmt in ["%H:%M", "%H:%M:%S"]:
                    try:
                        return datetime.strptime(t, fmt).strftime("%-I:%M %p")
                    except ValueError:
                        continue
                return "Unknown Time"
    
            for _, row in bookings_df.iterrows():
                date_str = pd.to_datetime(row['date'], errors="coerce").strftime('%A, %d %b') if row['date'] else "Unknown Date"
                time_ampm = format_time_safe(row['time'])
                players = [p for p in [row['player1'], row['player2'], row['player3'], row['player4']] if p]
                players_str = ", ".join(players) if players else "No players"
                standby_str = row.get('standby_player', "None")
                desc = f"Court: {row['court_name']} | Date: {date_str} | Time: {time_ampm} | Match Type: {row['match_type']} | Players: {players_str} | Standby: {standby_str}"
                booking_options.append(f"{desc} | Booking ID: {row['booking_id']}")
    
            selected_booking = st.selectbox("Select a booking to edit or delete", [""] + booking_options, key=unique_key)
            if selected_booking:
                booking_id = selected_booking.split(" | Booking ID: ")[-1]
                booking_row = bookings_df[bookings_df["booking_id"] == booking_id].iloc[0]
                booking_idx = bookings_df[bookings_df["booking_id"] == booking_id].index[0]
    
                with st.expander("Edit Booking Details", expanded=True):
                    date_edit = st.date_input(
                        "Booking Date *",
                        value=pd.to_datetime(booking_row["date"], errors="coerce").date(),
                        key=f"edit_booking_date_{booking_id}"
                    )
    
                    # Safe conversion of current booking time
                    current_time_ampm = format_time_safe(booking_row["time"])
    
                    hours = [datetime.strptime(f"{h}:00", "%H:%M").strftime("%-I:%M %p") for h in range(6, 22)]
                    time_index = hours.index(current_time_ampm) if current_time_ampm in hours else 0
    
                    time_edit = st.selectbox("Booking Time *", hours, index=time_index, key=f"edit_booking_time_{booking_id}")
                    match_type_edit = st.radio("Match Type", ["Doubles", "Singles"],
                                               index=0 if booking_row["match_type"] == "Doubles" else 1,
                                               key=f"edit_booking_match_type_{booking_id}")
    
                    if match_type_edit == "Doubles":
                        col1, col2 = st.columns(2)
                        with col1:
                            p1_edit = st.selectbox("Player 1 (optional)", [""] + available_players,
                                                   index=available_players.index(booking_row["player1"]) + 1 if booking_row["player1"] in available_players else 0,
                                                   key=f"edit_t1p1_{booking_id}")
                            p2_edit = st.selectbox("Player 2 (optional)", [""] + available_players,
                                                   index=available_players.index(booking_row["player2"]) + 1 if booking_row["player2"] in available_players else 0,
                                                   key=f"edit_t1p2_{booking_id}")
                        with col2:
                            p3_edit = st.selectbox("Player 3 (optional)", [""] + available_players,
                                                   index=available_players.index(booking_row["player3"]) + 1 if booking_row["player3"] in available_players else 0,
                                                   key=f"edit_t2p1_{booking_id}")
                            p4_edit = st.selectbox("Player 4 (optional)", [""] + available_players,
                                                   index=available_players.index(booking_row["player4"]) + 1 if booking_row["player4"] in available_players else 0,
                                                   key=f"edit_t2p2_{booking_id}")
                    else:
                        p1_edit = st.selectbox("Player 1 (optional)", [""] + available_players,
                                               index=available_players.index(booking_row["player1"]) + 1 if booking_row["player1"] in available_players else 0,
                                               key=f"edit_s1p1_{booking_id}")
                        p3_edit = st.selectbox("Player 2 (optional)", [""] + available_players,
                                               index=available_players.index(booking_row["player3"]) + 1 if booking_row["player3"] in available_players else 0,
                                               key=f"edit_s1p2_{booking_id}")
                        p2_edit = ""
                        p4_edit = ""
    
                    standby_initial_index = 0
                    if "standby_player" in booking_row and booking_row["standby_player"] and booking_row["standby_player"] in available_players:
                        standby_initial_index = available_players.index(booking_row["standby_player"]) + 1
    
                    standby_edit = st.selectbox("Standby Player (optional)", [""] + available_players,
                                                index=standby_initial_index, key=f"edit_standby_{booking_id}")
                    court_edit = st.selectbox("Court Name *", [""] + court_names,
                                              index=court_names.index(booking_row["court_name"]) + 1 if booking_row["court_name"] in court_names else 0,
                                              key=f"edit_court_{booking_id}")
                    screenshot_edit = st.file_uploader("Update Booking Screenshot (optional)",
                                                       type=["jpg", "jpeg", "png", "gif", "bmp", "webp"],
                                                       key=f"edit_screenshot_{booking_id}")
                    st.markdown("*Required fields", unsafe_allow_html=True)
    
                    col_save, col_delete = st.columns(2)
                    with col_save:
                        if st.button("Save Changes", key=f"save_booking_changes_{booking_id}"):
                            if not court_edit:
                                st.error("Court name is required.")
                            elif not date_edit or not time_edit:
                                st.error("Booking date and time are required.")
                            else:
                                players_edit = [p for p in [p1_edit, p2_edit, p3_edit, p4_edit] if p]
                                if len(set(players_edit)) != len(players_edit):
                                    st.error("Please select different players for each position.")
                                else:
                                    screenshot_url_edit = booking_row["screenshot_url"]
                                    if screenshot_edit:
                                        screenshot_url_edit = upload_image_to_supabase(screenshot_edit, booking_id, image_type="booking")
    
                                    time_24hr_edit = datetime.strptime(time_edit, "%I:%M %p").strftime("%H:%M")
                                    updated_booking = {
                                        "booking_id": booking_id,
                                        "date": date_edit.isoformat(),
                                        "time": time_24hr_edit,
                                        "match_type": match_type_edit,
                                        "court_name": court_edit,
                                        "player1": p1_edit if p1_edit else None,
                                        "player2": p2_edit if p2_edit else None,
                                        "player3": p3_edit if p3_edit else None,
                                        "player4": p4_edit if p4_edit else None,
                                        "standby_player": standby_edit if standby_edit else None,
                                        "screenshot_url": screenshot_url_edit if screenshot_url_edit else None
                                    }
                                    try:
                                        st.session_state.bookings_df.loc[booking_idx] = {**updated_booking, "date": date_edit.isoformat()}
                                        expected_columns = ['booking_id', 'date', 'time', 'match_type', 'court_name',
                                                            'player1', 'player2', 'player3', 'player4', 'standby_player', 'screenshot_url']
                                        bookings_to_save = st.session_state.bookings_df[expected_columns].copy()
                                        for col in ['player1', 'player2', 'player3', 'player4', 'standby_player', 'screenshot_url']:
                                            bookings_to_save[col] = bookings_to_save[col].replace("", None)
                                        bookings_to_save = bookings_to_save.drop_duplicates(subset=['booking_id'], keep='last')
                                        save_bookings(bookings_to_save)
                                        load_bookings()
                                        st.success("Booking updated successfully.")
                                        st.session_state.edit_booking_key += 1
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Failed to save booking: {str(e)}")
                                        st.session_state.edit_booking_key += 1
                                        st.rerun()
                    with col_delete:
                        if st.button("🗑️ Delete This Booking", key=f"delete_booking_{booking_id}"):
                            try:
                                delete_booking_from_db(booking_id)
                                load_bookings()
                                st.success("Booking deleted.")
                                st.session_state.edit_booking_key += 1
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to delete booking: {str(e)}")
                                st.session_state.edit_booking_key += 1
                                st.rerun()









# ... End of Tab[4]-------------------------------------------------------------------------



#--MINI TOURNEY -----------------------
with tabs[5]:
    st.header("Mini Tournaments Organiser")
    st.markdown("<small><i>Assignments of teams and courts are done randomly.</i></small>", unsafe_allow_html=True)

    # Input fields
    st.subheader("Tournament Setup")
    tournament_name = st.text_input("Enter Tournament Name")
    num_teams = st.number_input("Enter number of teams", min_value=2, step=1)
    num_courts = st.number_input("Enter number of courts", min_value=1, step=1)
    enter_names = st.radio("Do you want to enter team names?", ("No", "Yes"))
    enter_court_names = st.radio("Do you want to enter court names?", ("No", "Yes"))

    # Collect team names early, depending on radio selection
    team_names = []
    if num_teams and enter_names == "Yes":
        st.subheader("Enter Team Names")
        if num_teams <= 8:
            cols = st.columns(2)
        elif num_teams <= 16:
            cols = st.columns(3)
        else:
            cols = st.columns(4)

        for i in range(num_teams):
            col = cols[i % len(cols)]
            with col:
                name = st.text_input(f"Team {i+1} Name", key=f"team_{i}")
                team_names.append(name if name else f"Team {i+1}")
    else:
        team_names = [f"Team {i+1}" for i in range(num_teams)]

    # Optional court names
    court_names = []
    if num_courts and enter_court_names == "Yes":
        st.subheader("Enter Court Names")
        for i in range(num_courts):
            key = f"court_name_{i}"
            if key not in st.session_state:
                st.session_state[key] = f"Court {i+1}"
            name = st.text_input(f"Court {i+1} Name", key=key)
            court_names.append(name)
    else:
        court_names = [f"Court {i+1}" for i in range(num_courts)]

    # Optional tournament rules input
    rules = st.text_area("Enter Tournament Rules (optional, supports rich text)")

    if num_teams % 2 != 0:
        st.warning("Number of teams is odd. Consider adding one more team for even distribution.")

    if st.button("Organise Tournament"):
        random.shuffle(team_names)

        base = len(team_names) // num_courts
        extras = len(team_names) % num_courts

        courts = []
        idx = 0
        for i in range(num_courts):
            num = base + (1 if i < extras else 0)
            if num % 2 != 0:
                if i < num_courts - 1:
                    num += 1
            court_teams = team_names[idx:idx+num]
            courts.append((court_names[i], court_teams))
            idx += num

        st.markdown("---")
        st.subheader("Court Assignments")

        # Dynamic court layout with styled boxes matching ar.py colors
        primary_color = "#07314f"  # From ar.py gradient
        accent_color = "#fff500"   # Optic yellow from ar.py

        if len(courts) <= 4:
            num_cols = len(courts)
        elif len(courts) <= 8:
            num_cols = 4
        elif len(courts) <= 12:
            num_cols = 3
        else:
            num_cols = 2

        for i in range(0, len(courts), num_cols):
            row = st.columns(num_cols)
            for j, court in enumerate(courts[i:i + num_cols]):
                with row[j]:
                    court_name, teams = court
                    st.markdown(
                        f"""
                        <div style='border: 2px solid {accent_color}; border-radius: 12px; padding: 15px; margin: 10px 0; background-color: {primary_color}; color: white;'>
                            <img src='court.png' width='100%' style='border-radius: 8px;' />
                            <h4 style='text-align:center; color:{accent_color};'>{court_name}</h4>
                            <ul>{''.join(f'<li><b style="color:{accent_color};">{team}</b></li>' for team in teams)}</ul>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        if rules:
            st.subheader("Tournament Rules")
            st.markdown(rules, unsafe_allow_html=True)

        # PDF Generation
        def generate_pdf(tournament_name, courts, rules):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, tournament_name, ln=True, align="C")
            pdf.ln(10)

            pdf.set_font("Arial", '', 12)
            for court_name, teams in courts:
                pdf.set_text_color(7, 49, 79)  # RGB for #07314f
                pdf.cell(0, 10, court_name, ln=True)
                pdf.set_text_color(0, 0, 0)
                for team in teams:
                    pdf.cell(10)
                    pdf.cell(0, 10, f"- {team}", ln=True)
                pdf.ln(2)

            if rules:
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "Tournament Rules", ln=True)
                pdf.set_font("Arial", '', 11)
                for line in rules.splitlines():
                    pdf.multi_cell(0, 8, line)

            return pdf.output(dest='S').encode('latin-1')

        pdf_bytes = generate_pdf(tournament_name, courts, rules)
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name=f"{tournament_name or 'tournament'}.pdf",
            mime='application/pdf'
        )
        #----MINI TOURNEY-------


#st.markdown("---")

# Backup Download Button

st.markdown("---")
st.subheader("Data Backup")

zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
    # --- Matches CSV ---
    matches_csv = st.session_state.matches_df.to_csv(index=False)
    zip_file.writestr("matches.csv", matches_csv)

    # --- Players CSV ---
    players_csv = st.session_state.players_df.to_csv(index=False)
    zip_file.writestr("players.csv", players_csv)

    # --- Bookings CSV ---
    bookings_csv = st.session_state.bookings_df.to_csv(index=False)
    zip_file.writestr("bookings.csv", bookings_csv)

    # --- Profile Images ---
    for _, row in st.session_state.players_df.iterrows():
        url = row.get("profile_image_url")
        if url:
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    # sanitize name for safe filename
                    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', str(row["name"]))
                    zip_file.writestr(f"profile_images/{safe_name}.jpg", r.content)
            except Exception as e:
                st.warning(f"Could not download profile image for {row.get('name')}: {e}")

    # --- Match Images ---
    for _, row in st.session_state.matches_df.iterrows():
        url = row.get("match_image_url")
        if url:
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    match_id = row.get("match_id", str(uuid.uuid4()))
                    zip_file.writestr(f"match_images/{match_id}.jpg", r.content)
            except Exception as e:
                st.warning(f"Could not download match image for {row.get('match_id')}: {e}")

zip_buffer.seek(0)

# Format current date and time for filename
current_time = datetime.now().strftime("%Y%m%d-%H%M")
st.download_button(
    label="Backup",
    data=zip_buffer,
    file_name=f"ar-tennis-data-{current_time}.zip",
    mime="application/zip",
    key=f"backup_download_{st.session_state.get('form_key_suffix', 0)}"
)


st.markdown("""
<div style='background-color: #0d5384; padding: 1rem; border-left: 5px solid #fff500; border-radius: 0.5rem; color: white;'>
Built with ❤️ using <a href='https://streamlit.io/' style='color: #ccff00;'>Streamlit</a> — free and open source.
<a href='https://devs-scripts.streamlit.app/' style='color: #ccff00;'>Other Scripts by dev</a> on Streamlit.
</div>
""", unsafe_allow_html=True)
