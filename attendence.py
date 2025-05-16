import os
from datetime import datetime

def mark_attendance(name):
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%H:%M:%S')
    file_path = 'attendance.csv'

    # If the file doesn't exist, create it and write the header
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('Name,Date,Time,Status\n')

    # Read existing lines to check if this person is already marked today
    with open(file_path, 'r+') as f:
        lines = f.readlines()
        # Check if attendance already recorded today for this name
        recorded = [line for line in lines if name in line and date_str in line]
        if not recorded:
            # If not recorded, write a new line with the attendance info
            f.write(f'{name},{date_str},{time_str},Present\n')
