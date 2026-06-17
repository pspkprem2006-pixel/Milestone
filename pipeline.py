import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
import numpy as np

def phase1_generate_raw():
    output_dir = 'raw-session-data'
    os.makedirs(output_dir, exist_ok=True)
    start_date = datetime(2026, 6, 22)

    def get_session_date(n):
        current_date = start_date
        added_days = 0
        days_to_add = n - 1
        while added_days < days_to_add:
            current_date += timedelta(days=1)
            if current_date.weekday() != 6:
                added_days += 1
        return current_date

    disclaimer_options = ['No Response', 'OK', '']

    with open('sample.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    creation_time_idx = 15
    name_idx = 16
    email_idx = 17
    join_time_idx = 18
    leave_time_idx = 19
    duration_min_idx = 20
    disclaimer_idx = 22

    unique_emails = set()
    for row in rows:
        if len(row) > email_idx and row[email_idx]:
            unique_emails.add(row[email_idx])

    student_attendance_targets = {email: random.randint(25, 40) for email in unique_emails}

    for i in range(1, 41):
        session_date = get_session_date(i)
        new_rows = []
        for row in rows:
            if len(row) < 24 or (not row[name_idx] and not row[email_idx]):
                new_rows.append(row)
                continue
            new_row = list(row)
            email = row[email_idx]
            is_attending = email not in student_attendance_targets or student_attendance_targets[email] >= i
            join_total_minutes = random.randint(17*60, 18*60 + 30)
            join_h, join_m = divmod(join_total_minutes, 60)
            join_time = session_date.replace(hour=join_h, minute=join_m, second=random.randint(0, 59))
            if is_attending:
                leave_total_minutes = random.randint(join_total_minutes + 1, 19*60)
                leave_h, leave_m = divmod(leave_total_minutes, 60)
                leave_time = session_date.replace(hour=leave_h, minute=leave_m, second=random.randint(0, 59))
            else:
                leave_time = join_time
            duration = int((leave_time - join_time).total_seconds() // 60)
            creation_total_minutes = random.randint(8*60, 16*60 + 59)
            creation_h, creation_m = divmod(creation_total_minutes, 60)
            creation_time = session_date.replace(hour=creation_h, minute=creation_m, second=random.randint(0, 59))
            new_row[creation_time_idx] = creation_time.strftime('%-m/%-d/%Y %H:%M')
            new_row[join_time_idx] = join_time.strftime('%-m/%-d/%Y %H:%M')
            new_row[leave_time_idx] = leave_time.strftime('%-m/%-d/%Y %H:%M')
            new_row[duration_min_idx] = str(duration)
            new_row[disclaimer_idx] = random.choice(disclaimer_options)
            new_rows.append(new_row)
        filename = f'session_{i:02d}.csv'
        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(new_rows)
    print("Phase 1 complete.")

def phase2_preprocess():
    input_dir = 'raw-session-data'
    output_dir = 'preprocessed-session-data'
    os.makedirs(output_dir, exist_ok=True)
    for i in range(1, 41):
        filename = f'session_{i:02d}.csv'
        df = pd.read_csv(os.path.join(input_dir, filename), encoding='utf-8-sig')
        df = df.drop_duplicates()
        df = df.dropna(subset=['Name (original name)', 'Email'])
        df.columns = df.columns.str.strip().str.lower()
        for col in ['join time', 'leave time', 'creation time']:
            df[col] = pd.to_datetime(df[col])
        df['duration (min)'] = (df['leave time'] - df['join time']).dt.total_seconds() // 60
        df['duration (min)'] = df['duration (min)'].astype(int)
        df = df[df['duration (min)'] > 0]
        df.to_csv(os.path.join(output_dir, filename), index=False)
    print("Phase 2 complete.")

def phase3_4_report():
    input_dir = 'preprocessed-session-data'
    attendance_counts = {}
    student_names = {}
    for i in range(1, 41):
        filename = f'session_{i:02d}.csv'
        path = os.path.join(input_dir, filename)
        if not os.path.exists(path): continue
        df = pd.read_csv(path)
        unique_students = df.drop_duplicates(subset=['email'])
        for _, row in unique_students.iterrows():
            email = row['email']
            attendance_counts[email] = attendance_counts.get(email, 0) + 1
            student_names[email] = row['name (original name)']
    data = [{'student_name': student_names[e], 'student_email': e, 'classes_attended': c, 'certified': 'Yes' if c >= 34 else 'No'}
            for e, c in attendance_counts.items()]
    pd.DataFrame(data).to_csv('final.csv', index=False)
    print("Phase 3 & 4 complete.")

def phase5_visualize():
    df = pd.read_csv('final.csv')
    plt.figure(figsize=(12, 6))
    colors = df['classes_attended'].apply(lambda x: 'green' if x >= 34 else 'red')
    plt.scatter(range(len(df)), df['classes_attended'], c=colors, s=10, alpha=0.6)
    plt.axhline(y=34, color='black', linestyle='--', label='Certification Threshold (34)')
    plt.xlabel('Student Index')
    plt.ylabel('Classes Attended')
    plt.title('Student Attendance Overview')
    plt.legend()
    plt.tight_layout()
    plt.savefig('scatter_attendance.png')
    plt.close()
    plt.figure(figsize=(8, 6))
    cert_counts = df['certified'].value_counts()
    labels = ['Certified', 'Not Certified']
    values = [cert_counts.get('Yes', 0), cert_counts.get('No', 0)]
    bars = plt.bar(labels, values, color=['green', 'red'])
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', ha='center', va='bottom')
    plt.ylabel('Number of Students')
    plt.title('Certification Summary')
    plt.tight_layout()
    plt.savefig('bar_certification.png')
    plt.close()
    print("Phase 5 complete.")

if __name__ == "__main__":
    phase1_generate_raw()
    phase2_preprocess()
    phase3_4_report()
    phase5_visualize()
