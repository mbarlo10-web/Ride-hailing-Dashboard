"""
Ride-Hailing Dashboard - Streamlit
Sky Harbor Airport ride-hailing display (Streamlit version)
"""

import sys
import time
from io import BytesIO
from pathlib import Path
from datetime import datetime, timedelta

# Project root and path setup (run from repo root: streamlit run src/streamlit_app.py)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
import pandas as pd
import qrcode

from data_loader import RideHailingDataLoader
from analyzer import RideHailingAnalyzer
from plate_utils import PlateImageManager


# Paths relative to project root
DATA_PATH = ROOT / "assets" / "ride_hailing.xlsx"
PLATES_DIR = ROOT / "assets" / "plates"


def auto_refresh(interval_sec: int = 5) -> None:
    """
    Automatically rerun the app every `interval_sec` seconds while it's open.
    Mimics the real-time refresh behavior from the original dashboard.
    """
    key = "last_refresh_ts"
    now = time.time()
    last = st.session_state.get(key)
    if last is None:
        st.session_state[key] = now
    elif now - last >= interval_sec:
        st.session_state[key] = now
        # Use the stable rerun API; fall back if needed
        if hasattr(st, "rerun"):
            st.rerun()
        elif hasattr(st, "experimental_rerun"):
            st.experimental_rerun()


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


def get_parking_zones(df, current_time=None, grid_rows=8, grid_cols=6):
    """Build parking zone grid (same logic as Flask API).

    If current_time is provided, we simulate 'now' at that timestamp so that
    the dashboard can move through time for demonstration.
    """
    if df is None or df.empty:
        return []
    # Use simulated time if provided, otherwise fall back to max timestamp
    if current_time is None:
        current_time = df["current_time"].max()
    active_window = current_time - timedelta(minutes=30)
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


def get_active_rides(df, plate_manager, current_time=None, top_n=20):
    """Build active rides list (same logic as Flask API).

    Uses current_time to control which rides are considered 'active'.
    """
    if df is None or df.empty:
        return []
    if current_time is None:
        current_time = df["current_time"].max()
    active_window = current_time - timedelta(minutes=30)
    recent = df[df["current_time"] >= active_window].copy()
    recent = recent.sort_values("current_time", ascending=False).head(top_n)
    recent = recent.copy()
    recent["wait_time"] = (
        (current_time - recent["current_time"]).dt.total_seconds() / 60
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


def get_simulated_current_time(df: pd.DataFrame) -> datetime | None:
    """
    Step through the dataset's timeline so the dashboard changes over time.

    Each rerun advances to the next distinct timestamp; when it reaches the end,
    it wraps back to the start. This gives visible motion in the grid and queue.
    """
    if df is None or df.empty or "current_time" not in df.columns:
        return None

    # Sorted unique timestamps from the data
    times = pd.to_datetime(df["current_time"].sort_values().unique())
    if len(times) == 0:
        return None

    key = "sim_index"
    idx = st.session_state.get(key, -1)
    idx = (idx + 1) % len(times)
    st.session_state[key] = idx
    return times[idx]


def build_qr_image(url: str) -> BytesIO:
    """Generate a QR code PNG image buffer for the given URL."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def main():
    st.set_page_config(
        page_title="Sky Harbor Airport - Ride-Hailing Display",
        page_icon="🚕",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Periodically rerun the app to simulate real-time updates
    auto_refresh(interval_sec=5)

    df, data_loader, analyzer, plate_manager = load_data()

    # Choose a simulated "current" time for data-driven components
    sim_time = get_simulated_current_time(df) if df is not None else None

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
        grid = get_parking_zones(df, current_time=sim_time)
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
        rides = get_active_rides(df, plate_manager, current_time=sim_time)
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

    # Footer stats (also driven by simulated time)
    occupied_count = sum(1 for row in grid for cell in row if cell["occupancy"] > 0)
    stats_time = sim_time or df["current_time"].max()
    recent_window = stats_time - timedelta(hours=1)
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

    # High-level analysis highlights (matches analytic capabilities from main app)
    st.subheader("Analysis Highlights")
    col_a, col_b = st.columns(2)
    with col_a:
        st.caption("Rides by hour of day")
        by_hour = df.copy()
        by_hour["hour"] = by_hour["current_time"].dt.hour
        rides_by_hour = by_hour.groupby("hour").size()
        st.bar_chart(rides_by_hour)

    with col_b:
        st.caption("Rides by service")
        if "service" in df.columns:
            service_counts = df["service"].value_counts()
            st.bar_chart(service_counts)
        else:
            st.info("No `service` column available in data.")

    # QR code + info section, similar intent to the original Flask info page
    with st.sidebar:
        st.caption("Ride-hailing display information")

        # Generate a QR code that links to general Sky Harbor information.
        target_url = "https://www.skyharbor.com/"
        qr_buf = build_qr_image(target_url)
        st.image(qr_buf, caption="Scan for Sky Harbor info", use_column_width=True)

        st.markdown("**How to use this display**")
        st.markdown(
            "- Check the **Parking Zone Status** grid to find less busy zones.\n"
            "- Look at the **Active Rides Queue** for plate, service, and wait time.\n"
            "- Use the QR code to open airport information on your phone."
        )
        st.page_link(target_url, label="Sky Harbor Airport website", icon="🔗")


if __name__ == "__main__":
    main()
