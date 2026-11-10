import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import json

# Page Configuration
st.set_page_config(
    page_title="ARCHI-PLANNER – Smart Architectural Planning Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Architectural CSS Styling
st.markdown("""
<style>
    .main {
        background-color: #F8F9FA;
    }
    .stSidebar {
        background-color: #2C3E50;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #2C3E50;
    }
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 4px solid #3498DB;
        margin-bottom: 15px;
    }
    .architectural-header {
        background: linear-gradient(90deg, #2C3E50 0%, #34495E 100%);
        color: white;
        padding: 25px;
        border-radius: 8px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Data Persistence
if "project_info" not in st.session_state:
    st.session_state.project_info = {
        "name": "Residency Tower Alpha",
        "location": "Varanasi, Urban Zone A",
        "client": "Academic Studio Faculty",
        "site_length": 45.0,
        "site_width": 30.0,
        "setback_front": 5.0,
        "setback_rear": 3.0,
        "setback_side": 3.0,
        "fsi": 2.5,
        "ground_coverage_pct": 50.0,
        "num_floors": 4
    }

if "rooms" not in st.session_state:
    st.session_state.rooms = [
        {"name": "Living Room", "zone": "Public", "count": 1, "unit_area": 35.0},
        {"name": "Dining Room", "zone": "Semi-Public", "count": 1, "unit_area": 24.0},
        {"name": "Kitchen", "zone": "Service", "count": 1, "unit_area": 18.0},
        {"name": "Master Bedroom", "zone": "Private", "count": 2, "unit_area": 28.0},
        {"name": "Guest Bedroom", "zone": "Private", "count": 1, "unit_area": 20.0},
        {"name": "Bathrooms", "zone": "Service", "count": 3, "unit_area": 6.0},
        {"name": "Balcony / Deck", "zone": "Semi-Public", "count": 2, "unit_area": 12.0}
    ]

if "parking" not in st.session_state:
    st.session_state.parking = {
        "cars": 10,
        "two_wheelers": 15,
        "accessible": 2,
        "car_bay_area": 13.75,
        "two_wheeler_area": 3.0,
        "accessible_area": 18.0,
        "circulation_pct": 30.0,
        "ramp_allowance": 25.0
    }

if "zoning" not in st.session_state:
    st.session_state.zoning = {
        "building_pct": 50.0,
        "parking_pct": 20.0,
        "landscape_pct": 20.0,
        "open_pct": 10.0,
        "entrance_dir": "North"
    }

if "orientation" not in st.session_state:
    st.session_state.orientation = {
        "latitude": 25.3176,
        "longitude": 82.9739,
        "orientation_angle": 15.0,
        "date": "2026-06-21",
        "time": "12:00",
        "building_height": 15.0
    }

# Sidebar Navigation
st.sidebar.markdown("### 🏛️ ARCHI-PLANNER")
st.sidebar.markdown("*Smart Architectural Planning Assistant*")
st.sidebar.markdown("---")

module = st.sidebar.radio(
    "Navigation Menu",
    [
        "Dashboard",
        "1. Site Area Calculator",
        "2. Space Planner & Area Statement",
        "3. Parking Planner",
        "4. Site Zoning & Distribution",
        "5. Sun Path & Orientation",
        "6. Report Generator"
    ]
)

# ----------------------------------------------------
# MODULE 0: DASHBOARD
# ----------------------------------------------------
if module == "Dashboard":
    st.markdown("""
    <div class="architectural-header">
        <h1>ARCHI-PLANNER</h1>
        <p style="font-size: 1.1rem; margin-bottom: 0;">Comprehensive Preliminary Architectural Planning & Computation Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Welcome to ARCHI-PLANNER")
        st.write("""
        **ARCHI-PLANNER** is built specifically for architecture students and preliminary design professionals. It integrates architectural calculations, spatial programming, zoning layouts, parking estimation, solar orientation studies, and automated professional PDF report generation into a single unified desktop-ready workspace.
        
        #### Core Capabilities:
        - **Site & Envelope Calculations:** Automatically computes plot areas, permissible FSI floor areas, ground coverage limits, and setback envelopes.
        - **Interactive Space Programming:** Manage room schedules, zone categorization (Public, Semi-Public, Private, Service), and DSA-backed sorting/searching.
        - **Parking Estimation:** Calculate car, two-wheeler, and accessible parking bays with configurable circulation and ramp allowances.
        - **Conceptual Site Zoning:** Generate proportional zoning diagrams using Matplotlib.
        - **Solar & Orientation Studies:** Analyze sun exposure, daylighting, and shadows.
        - **Professional Report Generation:** Compile all metrics, tables, and diagrams into a structured PDF report.
        """)
        
        st.info("💡 **Tip:** Use the sidebar navigation to move between modules. All project data persists across modules during your session.")

    with col2:
        st.markdown("### Project Quick Info")
        p = st.session_state.project_info
        st.markdown(f"""
        <div class="metric-card">
            <b>Project:</b> {p['name']}<br>
            <b>Location:</b> {p['location']}<br>
            <b>Site Dimensions:</b> {p['site_length']}m × {p['site_width']}m<br>
            <b>Total Plot Area:</b> {p['site_length'] * p['site_width']:.2f} m²<br>
            <b>FSI / FAR:</b> {p['fsi']}<br>
            <b>Floors:</b> {p['num_floors']}
        </div>
        """, unsafe_allow_html=True)
        
        total_prog_area = sum([r['count'] * r['unit_area'] for r in st.session_state.rooms])
        max_allowable = (p['site_length'] * p['site_width']) * (p['ground_coverage_pct'] / 100.0) * p['num_floors']
        
        st.metric("Total Programmed Area", f"{total_prog_area:.1f} m²", f"Max Permissible: {max_allowable:.1f} m²")
        
# ----------------------------------------------------
# MODULE 1: SITE AREA CALCULATOR
# ----------------------------------------------------
elif module == "1. Site Area Calculator":

    st.markdown("## Module 1: Site Area & Building Envelope Calculator")

    st.write(
        "Configure site boundaries, setbacks, development controls "
        "(FSI/FAR), and ground coverage to determine the permissible "
        "building envelope."
    )

    # ------------------------------------------------
    # PROJECT AND SITE INPUTS
    # ------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Project & Site Inputs")

        p_name = st.text_input(
            "Project Name",
            st.session_state.project_info["name"],
            key="m1_project_name"
        )

        p_loc = st.text_input(
            "Project Location",
            st.session_state.project_info["location"],
            key="m1_project_location"
        )

        site_l = st.number_input(
            "Site Length (m)",
            min_value=5.0,
            max_value=500.0,
            value=float(st.session_state.project_info["site_length"]),
            step=1.0,
            key="m1_site_length"
        )

        site_w = st.number_input(
            "Site Width (m)",
            min_value=5.0,
            max_value=500.0,
            value=float(st.session_state.project_info["site_width"]),
            step=1.0,
            key="m1_site_width"
        )

        st.markdown("### Setbacks (m)")

        s_front = st.number_input(
            "Front Setback",
            min_value=0.0,
            max_value=50.0,
            value=float(st.session_state.project_info["setback_front"]),
            step=0.5,
            key="m1_front"
        )

        s_rear = st.number_input(
            "Rear Setback",
            min_value=0.0,
            max_value=50.0,
            value=float(st.session_state.project_info["setback_rear"]),
            step=0.5,
            key="m1_rear"
        )

        s_side = st.number_input(
            "Side Setback",
            min_value=0.0,
            max_value=50.0,
            value=float(st.session_state.project_info["setback_side"]),
            step=0.5,
            key="m1_side"
        )

    # ------------------------------------------------
    # DEVELOPMENT CONTROLS
    # ------------------------------------------------

    with col2:

        st.markdown("### Development Controls")

        fsi = st.number_input(
            "Floor Area Ratio (FAR / FSI)",
            min_value=0.1,
            max_value=10.0,
            value=float(st.session_state.project_info["fsi"]),
            step=0.1,
            key="m1_fsi"
        )

        gc_pct = st.number_input(
            "Ground Coverage Percentage (%)",
            min_value=10.0,
            max_value=100.0,
            value=float(st.session_state.project_info["ground_coverage_pct"]),
            step=1.0,
            key="m1_coverage"
        )

        floors = st.number_input(
            "Number of Floors",
            min_value=1,
            max_value=50,
            value=int(st.session_state.project_info["num_floors"]),
            step=1,
            key="m1_floors"
        )

    # ------------------------------------------------
    # SAVE PROJECT INPUTS
    # ------------------------------------------------

    st.session_state.project_info.update({

        "name": p_name,
        "location": p_loc,

        "site_length": site_l,
        "site_width": site_w,

        "setback_front": s_front,
        "setback_rear": s_rear,
        "setback_side": s_side,

        "fsi": fsi,
        "ground_coverage_pct": gc_pct,
        "num_floors": floors

    })

    st.markdown("---")

    # ------------------------------------------------
    # AREA CALCULATIONS
    # ------------------------------------------------

    st.markdown("### Calculated Results & Building Envelope")

    total_plot_area = site_l * site_w

    permissible_fsi_area = total_plot_area * fsi

    max_ground_coverage_area = (
        total_plot_area * gc_pct / 100.0
    )

    # Building envelope after setbacks

    env_length = max(
        0.0,
        site_l - s_front - s_rear
    )

    env_width = max(
        0.0,
        site_w - (2 * s_side)
    )

    envelope_footprint = env_length * env_width

    # Indicative average floor area

    avg_floor_area = (
        permissible_fsi_area / floors
        if floors > 0 else 0
    )

    # ------------------------------------------------
    # MAXIMUM PERMISSIBLE FOOTPRINT
    # ------------------------------------------------

    max_permissible_footprint = min(
        max_ground_coverage_area,
        envelope_footprint
    )

    # ------------------------------------------------
    # PROPOSED BUILDING FOOTPRINT
    # ------------------------------------------------

    st.markdown("### Proposed Building Footprint")

    st.caption(
        "Enter the actual proposed ground-floor building area "
        "to check ground coverage and setback compliance."
    )

    proposed_footprint = st.number_input(
        "Proposed Building Footprint (m²)",
        min_value=0.0,
        max_value=float(total_plot_area),
        value=float(max_permissible_footprint),
        step=10.0,
        key="m1_proposed_footprint"
    )

    # ------------------------------------------------
    # COMPLIANCE CALCULATIONS
    # ------------------------------------------------

    coverage_compliant = (
        proposed_footprint <= max_ground_coverage_area
    )

    setback_compliant = (
        proposed_footprint <= envelope_footprint
    )

    overall_compliant = (
        coverage_compliant and setback_compliant
    )

    excess_coverage = max(
        0.0,
        proposed_footprint - max_ground_coverage_area
    )

    excess_envelope = max(
        0.0,
        proposed_footprint - envelope_footprint
    )

    # ------------------------------------------------
    # DISPLAY MAIN RESULTS
    # ------------------------------------------------

    col_a, col_b, col_c, col_d = st.columns(4)

    col_a.metric(
        "Total Plot Area",
        f"{total_plot_area:,.2f} m²"
    )

    col_b.metric(
        "Permissible FSI Area",
        f"{permissible_fsi_area:,.2f} m²"
    )

    col_c.metric(
        "Max Ground Coverage",
        f"{max_ground_coverage_area:,.2f} m²"
    )

    col_d.metric(
        "Setback Footprint",
        f"{envelope_footprint:,.2f} m²"
    )

    # ------------------------------------------------
    # PERMISSIBLE BUILDING FOOTPRINT
    # ------------------------------------------------

    st.markdown("---")

    st.markdown("### Maximum Permissible Building Footprint")

    st.metric(
        "Maximum Permissible Footprint",
        f"{max_permissible_footprint:,.2f} m²"
    )

    # ------------------------------------------------
    # DETAILED CALCULATION SUMMARY
    # ------------------------------------------------

    st.markdown("---")

    st.markdown("### Detailed Calculation Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:

        st.write(
            f"**Building Envelope Dimensions:** "
            f"{env_length:.2f} m × {env_width:.2f} m"
        )

        st.write(
            f"**Setback Envelope Area:** "
            f"{envelope_footprint:,.2f} m²"
        )

        st.write(
            f"**Maximum Ground Coverage:** "
            f"{max_ground_coverage_area:,.2f} m²"
        )

    with summary_col2:

        st.write(
            f"**Proposed Building Footprint:** "
            f"{proposed_footprint:,.2f} m²"
        )

        st.write(
            f"**Maximum Permissible Footprint:** "
            f"{max_permissible_footprint:,.2f} m²"
        )

        st.write(
            f"**Indicative Average Floor Area:** "
            f"{avg_floor_area:,.2f} m² per floor "
            f"across {int(floors)} floors"
        )

    # ------------------------------------------------
    # REGULATORY COMPLIANCE STATUS
    # ------------------------------------------------

    st.markdown("---")

    st.markdown("### Regulatory Compliance Check")

    if overall_compliant:

        st.success(
            "PASS: Proposed building footprint is within "
            "the calculated ground coverage and setback limits."
        )

        st.write(
            f"Remaining ground coverage: "
            f"{max_ground_coverage_area - proposed_footprint:.2f} m²"
        )

        st.write(
            f"Remaining setback envelope: "
            f"{envelope_footprint - proposed_footprint:.2f} m²"
        )

    else:

        st.error(
            "FAIL: Proposed building footprint exceeds "
            "one or more calculated limits."
        )

        if not coverage_compliant:

            st.warning(
                f"Ground coverage exceeded by "
                f"{excess_coverage:.2f} m²."
            )

        if not setback_compliant:

            st.warning(
                f"Setback envelope exceeded by "
                f"{excess_envelope:.2f} m²."
            )

    # ------------------------------------------------
    # ADDITIONAL VALIDATION
    # ------------------------------------------------

    st.markdown("---")

    st.markdown("### Site Geometry Validation")

    if env_length <= 0 or env_width <= 0:

        st.error(
            "Invalid building envelope. The selected setbacks "
            "leave no available buildable dimensions."
        )

    elif envelope_footprint < proposed_footprint:

        st.warning(
            "The proposed building footprint is larger than "
            "the available setback envelope."
        )

    else:

        st.success(
            "Site dimensions and setback envelope are geometrically valid."
        )

    st.caption(
        "Note: These calculations are preliminary planning estimates. "
        "Actual development permission must be verified against applicable "
        "local building bye-laws, road width, height restrictions, "
        "fire safety, parking and other regulatory requirements."
    )

# ----------------------------------------------------


# MODULE 2: SPACE PLANNER & AREA STATEMENT
# ----------------------------------------------------
elif module == "2. Space Planner & Area Statement":

    st.markdown("## Module 2: Space Planner & Area Statement")

    st.write(
        "Manage architectural space programming, categorize zones, "
        "apply DSA sorting/searching, and compare with available built-up area."
    )

    # ------------------------------------------
    # CURRENT AREA STATEMENT
    # ------------------------------------------

    rooms_df = pd.DataFrame(st.session_state.rooms)

    rooms_df["Total Area"] = (
        rooms_df["count"] * rooms_df["unit_area"]
    )

    col_ctrl1, col_ctrl2 = st.columns([2, 1])

    with col_ctrl1:
        search_query = st.text_input(
            "🔍 Search Room Name (DSA Linear/Substring Search)",
            ""
        )

    with col_ctrl2:
        sort_order = st.selectbox(
            "📊 Sort Rooms by Area (DSA Quick/Merge Sort)",
            [
                "Descending (Largest First)",
                "Ascending (Smallest First)"
            ]
        )

    # ------------------------------------------
    # SEARCH FUNCTION
    # ------------------------------------------

    if search_query:
        rooms_df = rooms_df[
            rooms_df["name"].str.contains(
                search_query,
                case=False,
                na=False
            )
        ]

    # ------------------------------------------
    # SORTING FUNCTION
    # ------------------------------------------

    if "Descending" in sort_order:
        rooms_df = rooms_df.sort_values(
            by="Total Area",
            ascending=False
        )
    else:
        rooms_df = rooms_df.sort_values(
            by="Total Area",
            ascending=True
        )

    # ------------------------------------------
    # DISPLAY AREA STATEMENT
    # ------------------------------------------

    st.markdown("### Current Area Statement Table")

    if rooms_df.empty:
        st.info("No matching room found.")
    else:
        st.dataframe(
            rooms_df,
            use_container_width=True
        )

    # ------------------------------------------
    # MANAGE SPACES
    # ------------------------------------------

    st.markdown("### Manage Spaces")

    with st.form("add_room_form"):

        c1, c2, c3, c4 = st.columns(4)

        r_name = c1.text_input(
            "Room Name",
            "Study Room"
        )

        r_zone = c2.selectbox(
            "Zone",
            ["Public", "Semi-Public", "Private", "Service"]
        )

        r_count = c3.number_input(
            "Number of Units",
            min_value=1,
            max_value=20,
            value=1,
            step=1
        )

        r_area = c4.number_input(
            "Unit Area (m²)",
            min_value=1.0,
            max_value=500.0,
            value=15.0,
            step=0.5
        )

        submitted = st.form_submit_button(
            "Add Room to Programme"
        )

        # ------------------------------------------
        # VALIDATE AND ADD ROOM
        # ------------------------------------------

        if submitted:

            # Remove all extra whitespace
            r_name = " ".join(r_name.split())

            if not r_name:

                st.error("Room name cannot be empty.")

            else:

                st.session_state.rooms.append({
                    "name": r_name,
                    "zone": r_zone,
                    "count": int(r_count),
                    "unit_area": float(r_area)
                })

                st.success(
                    f"Added {r_name} successfully!"
                )

                st.rerun()

    # ------------------------------------------
    # DELETE ROOM
    # ------------------------------------------

    room_names = [
        r["name"] for r in st.session_state.rooms
    ]

    if room_names:

        to_delete = st.selectbox(
            "Select Room to Delete",
            room_names
        )

        if st.button("Delete Selected Room"):

            st.session_state.rooms = [
                r for r in st.session_state.rooms
                if r["name"] != to_delete
            ]

            st.success(
                f"Deleted {to_delete}!"
            )

            st.rerun()

    # ------------------------------------------
    # TOTAL PROGRAMMED AREA
    # ------------------------------------------

    total_programmed = sum(
        r["count"] * r["unit_area"]
        for r in st.session_state.rooms
    )

    # ------------------------------------------
    # MAXIMUM ALLOWABLE BUILT-UP AREA
    # ------------------------------------------

    p = st.session_state.project_info

    max_allowable = (
        p["site_length"] * p["site_width"]
    ) * (
        p["ground_coverage_pct"] / 100.0
    ) * p["num_floors"]

    # ------------------------------------------
    # SPACE PROGRAMMING VS BUILT-UP CAPACITY
    # ------------------------------------------

    st.markdown(
        "### Space Programming vs. Built-Up Capacity"
    )

    col_m1, col_m2, col_m3 = st.columns(3)

    col_m1.metric(
        "Total Programmed Area",
        f"{total_programmed:.2f} m²"
    )

    col_m2.metric(
        "Max Allowable Built-up Area",
        f"{max_allowable:.2f} m²"
    )

    diff = max_allowable - total_programmed

    col_m3.metric(
        "Area Variance / Buffer",
        f"{diff:.2f} m²",
        delta=f"{'Surplus' if diff >= 0 else 'Deficit'}"
    )

    # ------------------------------------------
    # EXPORT AREA STATEMENT AS CSV
    # ------------------------------------------

    csv_data = rooms_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Export Area Statement as CSV",
        data=csv_data,
        file_name="area_statement.csv",
        mime="text/csv"
    )

# ----------------------------------------------------

# MODULE 3: PARKING PLANNER
# ----------------------------------------------------
elif module == "3. Parking Planner":

    st.markdown("## Module 3: Parking Estimation & Circulation Planner")

    st.write(
        "Calculate car and two-wheeler parking bay requirements, "
        "circulation driveways, ramp allowances, and total parking "
        "footprint based on local standards."
    )

    # ------------------------------------------
    # VEHICLE COUNTS & PARKING BAY INPUTS
    # ------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Vehicle Counts & Bays")

        cars = st.number_input(
            "Number of Cars",
            min_value=0,
            max_value=200,
            value=int(st.session_state.parking["cars"]),
            step=1
        )

        twos = st.number_input(
            "Number of Two-Wheelers",
            min_value=0,
            max_value=500,
            value=int(st.session_state.parking["two_wheelers"]),
            step=1
        )

        # Accessible spaces cannot exceed car spaces
        acc = st.number_input(
            "Accessible Parking Spaces",
            min_value=0,
            max_value=int(cars),
            value=min(
                int(st.session_state.parking["accessible"]),
                int(cars)
            ),
            step=1
        )

        car_area = st.number_input(
            "Area per Car Bay (m²)",
            min_value=10.0,
            max_value=30.0,
            value=float(st.session_state.parking["car_bay_area"]),
            step=0.25
        )

        two_area = st.number_input(
            "Area per Two-Wheeler Bay (m²)",
            min_value=1.0,
            max_value=10.0,
            value=float(st.session_state.parking["two_wheeler_area"]),
            step=0.25
        )

        acc_area = st.number_input(
            "Area per Accessible Bay (m²)",
            min_value=10.0,
            max_value=40.0,
            value=float(st.session_state.parking["accessible_area"]),
            step=0.5
        )

    # ------------------------------------------
    # CIRCULATION & SERVICE ALLOWANCES
    # ------------------------------------------

    with col2:

        st.markdown("### Circulation & Service Allowances")

        circ_pct = st.number_input(
            "Driveway & Circulation Allowance (%)",
            min_value=10.0,
            max_value=100.0,
            value=float(st.session_state.parking["circulation_pct"]),
            step=1.0
        )

        ramp_pct = st.number_input(
            "Ramp / Basement Service Allowance (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.parking["ramp_allowance"]),
            step=1.0
        )

    # ------------------------------------------
    # UPDATE PARKING SESSION DATA
    # ------------------------------------------

    st.session_state.parking.update({
        "cars": int(cars),
        "two_wheelers": int(twos),
        "accessible": int(acc),
        "car_bay_area": float(car_area),
        "two_wheeler_area": float(two_area),
        "accessible_area": float(acc_area),
        "circulation_pct": float(circ_pct),
        "ramp_allowance": float(ramp_pct)
    })

    # ------------------------------------------
    # PARKING AREA CALCULATIONS
    # ------------------------------------------

    # Regular car spaces
    regular_cars = int(cars) - int(acc)

    car_total = regular_cars * car_area

    # Accessible parking spaces
    acc_total = int(acc) * acc_area

    # Two-wheeler parking spaces
    two_total = int(twos) * two_area

    # Total base parking area
    base_parking = (
        car_total + acc_total + two_total
    )

    # Circulation and driveway allowance
    circulation_area = (
        base_parking * (circ_pct / 100.0)
    )

    # Ramp and basement service allowance
    ramp_area = (
        (base_parking + circulation_area)
        * (ramp_pct / 100.0)
    )

    # Total parking footprint
    total_parking_footprint = (
        base_parking + circulation_area + ramp_area
    )

    # ------------------------------------------
    # PARKING SUMMARY
    # ------------------------------------------

    st.markdown("---")

    st.markdown("### Parking Summary & Breakdown")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Base Bay Area",
        f"{base_parking:.2f} m²"
    )

    m2.metric(
        "Circulation / Driveways",
        f"{circulation_area:.2f} m²"
    )

    m3.metric(
        "Ramp / Basement Allowance",
        f"{ramp_area:.2f} m²"
    )

    m4.metric(
        "Total Parking Footprint",
        f"{total_parking_footprint:.2f} m²"
    )

    # ------------------------------------------
    # PARKING AREA BREAKDOWN CHART
    # ------------------------------------------

    fig, ax = plt.subplots(figsize=(8, 4))

    categories = [
        "Car Bays",
        "Accessible Bays",
        "Two-Wheeler Bays",
        "Circulation",
        "Ramp Allowance"
    ]

    values = [
        car_total,
        acc_total,
        two_total,
        circulation_area,
        ramp_area
    ]

    colors_list = [
        "#3498DB",
        "#9B59B6",
        "#1ABC9C",
        "#F1C40F",
        "#E74C3C"
    ]

    ax.barh(
        categories,
        values,
        color=colors_list
    )

    ax.set_xlabel("Area in m²")
    ax.set_title("Parking Area Breakdown")

    st.pyplot(fig)

# ----------------------------------------------------

# MODULE 4: SITE ZONING & DISTRIBUTION
# ----------------------------------------------------
elif module == "4. Site Zoning & Distribution":

    st.markdown("## Module 4: Conceptual Site Zoning & Distribution")
    st.write(
        "Generate proportional conceptual site zoning layouts "
        "based on percentage area allocations for buildings, "
        "parking, landscaping, and open circulation."
    )

    c1, c2 = st.columns(2)

    with c1:
        b_pct = st.number_input(
            "Building Footprint Zone (%)",
            min_value=10.0,
            max_value=80.0,
            value=float(st.session_state.zoning["building_pct"]),
            step=1.0
        )

        p_pct = st.number_input(
            "Parking Zone (%)",
            min_value=5.0,
            max_value=50.0,
            value=float(st.session_state.zoning["parking_pct"]),
            step=1.0
        )

        l_pct = st.number_input(
            "Landscape & Green Zone (%)",
            min_value=5.0,
            max_value=50.0,
            value=float(st.session_state.zoning["landscape_pct"]),
            step=1.0
        )

        total_pct = b_pct + p_pct + l_pct

        entrance = st.selectbox(
            "Main Access / Entrance Direction",
            ["North", "South", "East", "West"],
            index=["North", "South", "East", "West"].index(
                st.session_state.zoning.get("entrance_dir", "North")
            )
        )

        if total_pct > 100:
            open_pct = 0.0

            st.session_state.zoning.update({
                "building_pct": b_pct,
                "parking_pct": p_pct,
                "landscape_pct": l_pct,
                "open_pct": open_pct,
                "entrance_dir": entrance
            })

            st.error(
                f"Invalid allocation! Total zone allocation is "
                f"{total_pct:.1f}%. It cannot exceed 100%. "
                f"Please reduce the percentages by {total_pct - 100:.1f}%."
            )

        else:
            open_pct = 100.0 - total_pct

            st.info(
                f"Open Circulation & Paved Spaces "
                f"(Auto-calculated remainder): {open_pct:.1f}%"
            )

            st.session_state.zoning.update({
                "building_pct": b_pct,
                "parking_pct": p_pct,
                "landscape_pct": l_pct,
                "open_pct": open_pct,
                "entrance_dir": entrance
            })

    if total_pct <= 100:

        with c2:
            st.markdown("### Zone Area Distribution")

            p = st.session_state.project_info
            total_site = p["site_length"] * p["site_width"]

            b_area = total_site * (b_pct / 100.0)
            p_area = total_site * (p_pct / 100.0)
            l_area = total_site * (l_pct / 100.0)
            o_area = total_site * (open_pct / 100.0)

            st.markdown(f"""
            - **Total Site Area:** {total_site:.2f} m²
            - **Building Footprint Area:** {b_area:.2f} m² ({b_pct:.1f}%)
            - **Parking Zone Area:** {p_area:.2f} m² ({p_pct:.1f}%)
            - **Landscape / Green Area:** {l_area:.2f} m² ({l_pct:.1f}%)
            - **Open Circulation / Paved Area:** {o_area:.2f} m² ({open_pct:.1f}%)
            - **Main Access Direction:** {entrance}
            """)

        st.markdown("### Conceptual Zoning Diagram")

        fig, ax = plt.subplots(figsize=(7, 6))

        labels = [
            'Building Footprint',
            'Parking',
            'Landscape / Green',
            'Open Circulation'
        ]

        sizes = [b_pct, p_pct, l_pct, open_pct]

        colors = [
            '#2C3E50',
            '#E74C3C',
            '#27AE60',
            '#F39C12'
        ]

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=140,
            textprops=dict(color="black")
        )

        plt.setp(autotexts, size=10, weight="bold")

        ax.set_title(
            f"Conceptual Site Zoning Layout "
            f"(Main Entrance: {entrance})",
            fontsize=12,
            pad=20
        )

        st.pyplot(fig)


# ----------------------------------------------------
# MODULE 5: SUN PATH & ORIENTATION
# ----------------------------------------------------

elif module == "5. Sun Path & Orientation":

    st.markdown("## Module 5: Sun Path & Orientation Analysis")
    st.write("Study approximate solar position, building orientation and shadow length.")

    o = st.session_state.orientation

    col1, col2 = st.columns(2)

    with col1:
        latitude = st.number_input(
            "Latitude (degrees)",
            min_value=-90.0,
            max_value=90.0,
            value=float(o["latitude"])
        )

        longitude = st.number_input(
            "Longitude (degrees)",
            min_value=-180.0,
            max_value=180.0,
            value=float(o["longitude"])
        )

        orientation_angle = st.number_input(
            "Building Orientation Angle (degrees)",
            min_value=0.0,
            max_value=360.0,
            value=float(o["orientation_angle"])
        )

    with col2:
        selected_date = st.date_input(
            "Select Date",
            value=pd.to_datetime(o["date"]).date()
        )

        selected_time = st.time_input(
            "Select Local Time",
            value=pd.to_datetime(o["time"]).time()
        )

        building_height = st.number_input(
            "Building Height (m)",
            min_value=1.0,
            max_value=500.0,
            value=float(o["building_height"])
        )

    st.session_state.orientation.update({
        "latitude": latitude,
        "longitude": longitude,
        "orientation_angle": orientation_angle,
        "date": str(selected_date),
        "time": str(selected_time),
        "building_height": building_height
    })

    # Approximate solar position calculation
    day_number = selected_date.timetuple().tm_yday

    B = 2 * np.pi * (day_number - 81) / 364

    declination = 23.45 * np.sin(
        np.deg2rad(360 * (284 + day_number) / 365)
    )

    equation_of_time = (
        9.87 * np.sin(2 * B)
        - 7.53 * np.cos(B)
        - 1.5 * np.sin(B)
    )

    clock_minutes = (
        selected_time.hour * 60
        + selected_time.minute
    )

    solar_minutes = (
        clock_minutes
        + equation_of_time
        + 4 * (longitude - 82.5)
    )

    solar_hour = solar_minutes / 60
    hour_angle = 15 * (solar_hour - 12)

    lat_rad = np.deg2rad(latitude)
    dec_rad = np.deg2rad(declination)
    ha_rad = np.deg2rad(hour_angle)

    altitude_value = np.arcsin(
        np.sin(lat_rad) * np.sin(dec_rad)
        + np.cos(lat_rad) * np.cos(dec_rad) * np.cos(ha_rad)
    )

    solar_altitude = np.rad2deg(altitude_value)

    azimuth = (
        np.rad2deg(
            np.arctan2(
                np.sin(ha_rad),
                np.cos(ha_rad) * np.sin(lat_rad)
                - np.tan(dec_rad) * np.cos(lat_rad)
            )
        ) + 180
    ) % 360

    st.markdown("---")
    st.markdown("### Solar Analysis Results")

    m1, m2, m3 = st.columns(3)

    m1.metric("Solar Altitude", f"{solar_altitude:.2f}°")
    m2.metric("Solar Azimuth", f"{azimuth:.2f}°")
    m3.metric("Building Orientation", f"{orientation_angle:.1f}°")

    if solar_altitude > 0:
        shadow_length = building_height / np.tan(altitude_value)
        st.metric("Approximate Shadow Length", f"{shadow_length:.2f} m")
    else:
        st.warning("The sun is below the horizon at this selected time.")

    st.markdown("### Architectural Recommendations")

    st.write("""
    - Study east and west facades for low-angle morning and evening sun.
    - Use suitable shading devices on exposed facades.
    - Consider daylight availability when positioning major spaces.
    - Use the solar altitude and azimuth as preliminary design inputs.
    """)

    st.info(
        "These are approximate solar calculations, not a certified "
        "solar simulation. Verify detailed design with a solar analysis tool."
    )


# ----------------------------------------------------

# MODULE 6: REPORT GENERATOR
# ----------------------------------------------------

elif module == "6. Report Generator":

    st.markdown("## Module 6: Architectural Report Generator")

    st.write(
        "Combine project information, area statement, parking, "
        "zoning and solar analysis into an Excel report."
    )

    # --------------------------------
    # GET PROJECT DATA
    # --------------------------------

    p = st.session_state.project_info
    rooms_df = pd.DataFrame(st.session_state.rooms)

    rooms_df["Total Area"] = (
        rooms_df["count"] * rooms_df["unit_area"]
    )

    parking = st.session_state.parking
    zoning = st.session_state.zoning
    orientation = st.session_state.orientation

    project_df = pd.DataFrame([p])
    parking_df = pd.DataFrame([parking])
    zoning_df = pd.DataFrame([zoning])

    # --------------------------------
    # SOLAR ANALYSIS CALCULATION
    # SAME FORMULA AS MODULE 5
    # --------------------------------

    latitude = float(orientation["latitude"])
    longitude = float(orientation["longitude"])
    orientation_angle = float(orientation["orientation_angle"])
    building_height = float(orientation["building_height"])

    selected_date = pd.to_datetime(
        orientation["date"]
    ).date()

    selected_time = pd.to_datetime(
        orientation["time"]
    ).time()

    day_number = selected_date.timetuple().tm_yday

    B = 2 * np.pi * (day_number - 81) / 364

    declination = 23.45 * np.sin(
        np.deg2rad(360 * (284 + day_number) / 365)
    )

    equation_of_time = (
        9.87 * np.sin(2 * B)
        - 7.53 * np.cos(B)
        - 1.5 * np.sin(B)
    )

    clock_minutes = (
        selected_time.hour * 60
        + selected_time.minute
    )

    solar_minutes = (
        clock_minutes
        + equation_of_time
        + 4 * (longitude - 82.5)
    )

    solar_hour = solar_minutes / 60
    hour_angle = 15 * (solar_hour - 12)

    lat_rad = np.deg2rad(latitude)
    dec_rad = np.deg2rad(declination)
    ha_rad = np.deg2rad(hour_angle)

    altitude_value = np.arcsin(
        np.sin(lat_rad) * np.sin(dec_rad)
        + np.cos(lat_rad) * np.cos(dec_rad) * np.cos(ha_rad)
    )

    solar_altitude = np.rad2deg(altitude_value)

    azimuth = (
        np.rad2deg(
            np.arctan2(
                np.sin(ha_rad),
                np.cos(ha_rad) * np.sin(lat_rad)
                - np.tan(dec_rad) * np.cos(lat_rad)
            )
        ) + 180
    ) % 360

    # --------------------------------
    # SHADOW LENGTH
    # --------------------------------

    if solar_altitude > 0:
        shadow_length = (
            building_height / np.tan(altitude_value)
        )
        shadow_result = round(float(shadow_length), 2)
        calculation_note = "Sun is above the horizon"
    else:
        shadow_result = None
        calculation_note = "Sun is below the horizon"

    # --------------------------------
    # ARCHITECTURAL RECOMMENDATIONS
    # --------------------------------

    recommendations = (
        "Study east and west facades for low-angle morning "
        "and evening sun. Use suitable shading devices on "
        "exposed facades. Consider daylight availability "
        "when positioning major spaces. Use solar altitude "
        "and azimuth as preliminary design inputs."
    )

    # --------------------------------
    # COMPLETE SOLAR DATAFRAME
    # --------------------------------

    solar_data = {
        "latitude": latitude,
        "longitude": longitude,
        "orientation": orientation_angle,
        "date": str(selected_date),
        "time": str(selected_time),
        "building_height": building_height,
        "solar_altitude_degrees": round(float(solar_altitude), 2),
        "solar_azimuth_degrees": round(float(azimuth), 2),
        "shadow_length_m": shadow_result,
        "architectural_recommendations": recommendations,
        "calculation_note": calculation_note
    }

    orientation_df = pd.DataFrame([solar_data])

    # --------------------------------
    # PROJECT SUMMARY
    # --------------------------------

    st.markdown("### Project Summary")

    st.write(f"**Project:** {p['name']}")
    st.write(f"**Location:** {p['location']}")

    st.write(
        f"**Site Area:** "
        f"{p['site_length'] * p['site_width']:.2f} m²"
    )

    # --------------------------------
    # AREA STATEMENT PREVIEW
    # --------------------------------

    st.markdown("### Area Statement Preview")

    st.dataframe(
        rooms_df,
        use_container_width=True
    )

    total_area = rooms_df["Total Area"].sum()

    st.metric(
        "Total Programmed Area",
        f"{total_area:.2f} m²"
    )

    # --------------------------------
    # SOLAR RESULTS PREVIEW
    # --------------------------------

    st.markdown("### Solar Analysis Preview")

    s1, s2, s3 = st.columns(3)

    s1.metric(
        "Solar Altitude",
        f"{solar_altitude:.2f}°"
    )

    s2.metric(
        "Solar Azimuth",
        f"{azimuth:.2f}°"
    )

    if shadow_result is not None:
        s3.metric(
            "Shadow Length",
            f"{shadow_result:.2f} m"
        )
    else:
        s3.metric(
            "Shadow Length",
            "Sun below horizon"
        )

    # --------------------------------
    # EXCEL REPORT GENERATION
    # --------------------------------

    st.markdown("### Export Complete Project Report")

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        project_df.to_excel(
            writer,
            sheet_name="Project Details",
            index=False
        )

        rooms_df.to_excel(
            writer,
            sheet_name="Area Statement",
            index=False
        )

        parking_df.to_excel(
            writer,
            sheet_name="Parking",
            index=False
        )

        zoning_df.to_excel(
            writer,
            sheet_name="Site Zoning",
            index=False
        )

        orientation_df.to_excel(
            writer,
            sheet_name="Sun Orientation",
            index=False
        )

    st.download_button(
        label="Download Complete Excel Report",
        data=excel_buffer.getvalue(),
        file_name="ARCHI_PLANNER_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.success(
        "Your complete project report is ready to download."
    )

