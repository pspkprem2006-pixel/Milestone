# Attendance Certification Pipeline

This project automates the process of tracking student attendance across multiple sessions and generating certification reports and visualizations.

## Project Overview

The pipeline processes session data to determine which students have met the attendance threshold for certification. The certification threshold is defined as attending **34 or more sessions out of 40** (85% attendance).

## Features

- **Data Generation:** Simulates raw session data for testing.
- **Preprocessing:** Cleans and standardizes session data (removes duplicates, handles missing values, standardizes column names).
- **Reporting:** Generates a final CSV report indicating certification status for each student.
- **Visualization:** Produces scatter plots of attendance and bar charts of certification summaries.

## Prerequisites

- Python 3.x
- pandas
- matplotlib
- numpy

You can install the dependencies using:
```bash
pip install pandas matplotlib numpy
```

## Project Structure

- `pipeline.py`: The main script containing the entire data pipeline.
- `raw-session-data/`: Directory containing generated raw CSV files.
- `preprocessed-session-data/`: Directory containing cleaned CSV files.
- `final.csv`: The final certification report.
- `scatter_attendance.png`: Scatter plot showing attendance per student.
- `bar_certification.png`: Bar chart summarizing certification results.

## Usage

To run the entire pipeline, execute the following command:

```bash
python pipeline.py
```

## Pipeline Phases

1. **Phase 1: Generate Raw Data** - Simulates 40 sessions of attendance data based on a sample template.
2. **Phase 2: Preprocess** - Cleans the raw data by removing duplicates, dropping rows with missing names/emails, and standardizing headers.
3. **Phase 3 & 4: Report Generation** - Aggregates attendance across all sessions and determines certification status.
4. **Phase 5: Visualize** - Generates visual representations of the attendance and certification data.
