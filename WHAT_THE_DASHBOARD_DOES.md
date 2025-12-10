# What Does the Dashboard Do?

## 🎯 Purpose
This dashboard is designed to be displayed on a **large screen at Sky Harbor Airport** to help passengers waiting for their ride-hailing services (Uber, Lyft, etc.).

## 📊 What You See on Screen

### Left Side: **Parking Zone Status Grid**
- Shows **48 parking/waiting zones** (8 rows × 6 columns)
- Each zone is color-coded:
  - 🟢 **Green** = Empty/Available (0 rides)
  - 🟡 **Yellow** = Moderate (1-2 rides waiting)
  - 🔴 **Red** = Busy (3+ rides waiting)
- **Why it's useful**: Passengers can see which waiting areas are less crowded

### Right Side: **Active Rides Queue**
- Shows a **live list of active rides** currently in the system
- Each entry shows:
  - License plate number (so passengers can find their ride)
  - Service type (Uber, Lyft, Other)
  - Wait time (how long until pickup)
  - Timestamp (when the ride was requested)
- **Why it's useful**: Passengers can see if their ride is coming soon and identify it by license plate

### Top: **Current Time**
- Large clock showing current time and date
- Updates every second

### Bottom: **Statistics**
- **Rides Today**: Total number of rides processed today
- **Active Drivers**: Number of drivers currently active
- **Occupied Zones**: How many zones currently have rides
- **QR Code**: Passengers can scan to get more information

## 🔄 How It Works

1. **Reads data** from your Excel file (`assets/ride_hailing.xlsx`)
2. **Maps rides to zones** based on their location (x, y coordinates)
3. **Updates automatically** every 5 seconds
4. **Shows recent activity** (rides from the last 30 minutes)

## 🎬 Real-World Use Case

Imagine you're at the airport:
- You order an Uber/Lyft
- You walk to the ride-hailing pickup area
- You see this dashboard on a big screen
- You can:
  - Find a less crowded waiting zone (green zones)
  - Check if your ride is in the queue
  - See how long until pickup
  - Scan the QR code for more info

## 💡 Key Features

✅ **Real-time updates** - Refreshes every 5 seconds  
✅ **Visual indicators** - Color coding makes it easy to understand at a glance  
✅ **License plate display** - Helps passengers identify their ride  
✅ **Wait time estimates** - Shows how long until pickup  
✅ **Zone occupancy** - Helps passengers find less crowded areas  

This is exactly like the dashboard shown in the demo video from the train station in China!

