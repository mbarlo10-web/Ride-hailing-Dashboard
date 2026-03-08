"""
Ride-Hailing Dashboard - Streamlit
Sky Harbor Airport ride-hailing display (Streamlit version)
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Project root and path setup (run from repo root: streamlit run src/streamlit_app.py)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
import pandas as pd

from data_loader import RideHailingDataLoader
from analyzer import RideHailingAnalyzer
from plate_utils import PlateImageManager


# Paths relative to project root
DATA_PATH = ROOT / "assets" / "ride_hailing.xlsx"
PLATES_DIR = ROOT / "assets" / "plates"


@st.cache_data(ttl=300)
def load_data():
    """Load and clean ride-hailing data (cached)."""
    if not DATA_PATH.exists():
        return None, None, None, None
    try:
        data_loader = RideHailingDataLoader(str(DATA_PATH))
        df = data_loader.clean_data()
        analyzer = RideHailingAnalyzer(data_loader)
        plate_manager = PlateImageManager(str(PLATES_DIR)) if PLATES_DIR.exists() else None
        return df, data_loader, analyzer, plate_manager
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None


def get_parking_zones(df, grid_rows=8, grid_cols=6):
    """Build parking zone grid (same logic as Flask API)."""
    if df is None or df.empty:
        return []
    latest_time = df["current_time"].max()
    active_window = latest_time - timedelta(minutes=30)
    recent = df[df["current_time"] >= active_window].copy()
    x_min, x_max = df["x"].min(), df["x"].max()
    y_min, y_max = df["y"].min(), df["y"].max()
    zone_occupancy = {}
    for _, ride in recent.iterrows():
        x_norm = (ride["x"] - x_min) / (x_max - x_min) if (x_max - x_min) > 0 else 0.5
        y_norm = (ride["y"] - y_min) / (y_max - y_min) if (y_max - y_min) > 0 else 0.5
        grid_x = min(int(x_norm * grid_cols), grid_cols - 1)
        grid_y = min(int(y_norm * grid_rows), grid_rows - 1)
        zone_id = f"{grid_y}-{grid_x}"
        if zone_id not in zone_occupancy:
            zone_occupancy[zone_id] = []
        zone_occupancy[zone_id].append(
            {
                "plate": ride.get("plate_number", "N/A"),
                "service": ride.get("service", "N/A"),
                "time": ride["current_time"].strftime("%H:%M"),
            }
        )
    grid = []
    for row in range(grid_rows):
        grid_row = []
        for col in range(grid_cols):
            zone_id = f"{row}-{col}"
            rides = zone_occupancy.get(zone_id, [])
            occupancy = len(rides)
            if occupancy == 0:
                status, color = "available", "green"
            elif occupancy <= 2:
                status, color = "moderate", "yellow"
            else:
                status, color = "busy", "red"
            grid_row.append(
                {
                    "zone_id": f"Zone {chr(65 + row)}{col + 1}",
                    "occupancy": occupancy,
                    "status": status,
                    "color": color,
                    "rides": rides[:3],
                }
            )
        grid.append(grid_row)
    return grid


def get_active_rides(df, plate_manager, top_n=20):
    """Build active rides list (same logic as Flask API)."""
    if df is None or df.empty:
        return []
    latest_time = df["current_time"].max()
    active_window = latest_time - timedelta(minutes=30)
    recent = df[df["current_time"] >= active_window].copy()
    recent = recent.sort_values("current_time", ascending=False).head(top_n)
    recent = recent.copy()
    recent["wait_time"] = (
        (latest_time - recent["current_time"]).dt.total_seconds() / 60
    ).clip(lower=1)
    rides = []
    for idx, (_, ride) in enumerate(recent.iterrows()):
        plate = ride.get("plate_number", "N/A")
        has_image = (
            plate_manager.get_plate_image(plate) is not None if plate_manager else False
        )
        rides.append(
            {
                "plate_number": plate,
                "service": ride.get("service", "N/A"),
                "time": ride["current_time"].strftime("%H:%M"),
                "wait_time": int(ride["wait_time"]),
                "has_image": has_image,
                "zone": f"Zone {chr(65 + (idx % 8))}{(idx % 6) + 1}",
                "status": "arriving" if ride["wait_time"] < 5 else "waiting",
            }
        )
    return rides


def main():
    st.set_page_config(
        page_title="Sky Harbor Airport - Ride-Hailing Display",
        page_icon="🚕",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    df, data_loader, analyzer, plate_manager = load_data()

    # Header
    col_title, col_time = st.columns([2, 1])
    with col_title:
        st.title("🚕 Sky Harbor Airport - Ride-Hailing Display")
    with col_time:
        now = datetime.now()
        st.metric("Time", now.strftime("%H:%M"))
        st.caption(now.strftime("%A, %B %d, %Y"))

    if df is None:
        st.warning(
            "Data file not found. Place `ride_hailing.xlsx` in `assets/` and restart."
        )
        st.stop()

    # Parking zones and active rides side by side
    col_zones, col_rides = st.columns([1, 1])

    with col_zones:
        st.subheader("Parking Zone Status")
        grid = get_parking_zones(df)
        for row in grid:
            cols = st.columns(6)
            for c, cell in enumerate(row):
                with cols[c]:
                    color = {
                        "green": "#4caf50",
                        "yellow": "#ffc107",
                        "red": "#f44336",
                    }.get(cell["color"], "#666")
                    st.markdown(
                        f'<div style="padding:10px; border-radius:8px; background:{color}; '
                        f'color:white; text-align:center; font-weight:bold;">'
                        f'{cell["zone_id"]}<br>{cell["occupancy"]}</div>',
                        unsafe_allow_html=True,
                    )

    with col_rides:
        st.subheader("Active Rides Queue")
        rides = get_active_rides(df, plate_manager)
        if not rides:
            st.info("No active rides in the last 30 minutes.")
        else:
            ride_df = pd.DataFrame(rides)[
                ["plate_number", "service", "time", "wait_time", "zone", "status"]
            ]
            ride_df = ride_df.rename(
                columns={
                    "plate_number": "Plate",
                    "wait_time": "Wait (min)",
                    "zone": "Zone",
                    "status": "Status",
                }
            )
            st.dataframe(ride_df, use_container_width=True, hide_index=True)

    # Footer stats
    occupied_count = sum(1 for row in grid for cell in row if cell["occupancy"] > 0)
    latest_time = df["current_time"].max()
    recent_window = latest_time - timedelta(hours=1)
    recent_count = len(df[df["current_time"] >= recent_window])
    unique_drivers = df["driver_id"].nunique()

    st.divider()
    stat1, stat2, stat3, _ = st.columns(4)
    with stat1:
        st.metric("Rides (last hour)", f"{recent_count:,}")
    with stat2:
        st.metric("Active drivers", unique_drivers)
    with stat3:
        st.metric("Occupied zones", occupied_count)

    # Optional: QR code for info page (link only on Streamlit Cloud)
    with st.sidebar:
        st.caption("Ride-hailing information")
        st.page_link("https://www.skyharbor.com/", label="Sky Harbor Airport info", icon="🔗")


if __name__ == "__main__":
    main()
