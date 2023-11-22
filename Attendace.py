import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os.path

# File path for the Excel file
excel_file_path = r"https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2FRomilai%2FAttendace_Tracker_Emp%2Fmain%2Fattendance_data.xlsx&wdOrigin=BROWSELINK"

# Define a shared variable to hold the attendance data

def get_attendance_data():
    if os.path.exists(excel_file_path):
        return pd.read_excel(excel_file_path)
    else:
        return pd.DataFrame(columns=["Employee ID", "Name", "Date", "Check-In Time", "Check-Out Time"])


attendance_data = get_attendance_data()

# Streamlit app layout
st.title("Employee Attendance and Time Tracker")

# Input fields for Employee ID and Name
employee_id = st.text_input("Employee ID")
employee_name = st.text_input("Name")

# Get today's date in string format without the time part
today_date = (datetime.now()).strftime("%Y-%m-%d")

# Check-In and Check-Out buttons
def checkin():
    global attendance_data

    # Check if data already exists for the given Employee ID, Name, and Date
    existing_data = attendance_data[
        (attendance_data["Employee ID"].astype(str) == str(employee_id)) &
        (attendance_data["Name"].astype(str) == str(employee_name)) &
        (attendance_data["Date"].astype(str) == today_date)
    ]

    if not existing_data.empty:
        st.warning("Data already exists for today.")
    else:
        checkin_time = datetime.now().time()
        new_entry = {
            "Employee ID": str(employee_id),  # Convert to string
            "Name": str(employee_name),  # Convert to string
            "Date": today_date,
            "Check-In Time": checkin_time,
            "Check-Out Time": None
        }
        attendance_data = pd.concat([attendance_data, pd.DataFrame([new_entry])], ignore_index=True)
        attendance_data.to_excel(excel_file_path, index=False)  # Update Excel file
        st.success(f"Checked in at {checkin_time}")

if st.button("Check-In"):
    checkin()

def checkout():
    global attendance_data
    checkout_time = datetime.now().time()

    # Filter data for the current session (same employee_id, name, and date)
    current_session_data = attendance_data.loc[
        (attendance_data["Date"].astype(str) == today_date) &
        (attendance_data["Employee ID"].astype(str) == str(employee_id)) &
        (attendance_data["Name"].astype(str) == str(employee_name))
    ]

    if not current_session_data.empty:
        # Check if already checked out for today
        if current_session_data["Check-Out Time"].notna().any():
            st.warning("Already checked out for today.")
        else:
            # Update checkout time for each matching record
            for index in current_session_data.index:
                attendance_data.at[index, "Check-Out Time"] = checkout_time

            attendance_data.to_excel(excel_file_path, index=False)  # Update Excel file
            st.success(f"Checked out at {checkout_time}")
    else:
        st.error("No matching check-in found for this employee and date.")


if st.button("Check-Out"):
    checkout()

# Retrieve Employee IDs and Names for today's date
current_session_data = attendance_data.loc[
    (attendance_data["Date"].astype(str) == today_date), ["Employee ID", "Name"]
].drop_duplicates()

employee_ids_today = current_session_data["Employee ID"].tolist()
employee_names_today = current_session_data["Name"].tolist()

# Display retrieved data
st.write("### Employee IDs for Today:")
st.write(employee_ids_today)

st.write("### Employee Names for Today:")
st.write(employee_names_today)

# Run the app
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
