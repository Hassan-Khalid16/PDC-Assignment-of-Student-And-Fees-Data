#LINEAR APPROACH

import pandas as pd

# Load the CSV files for students and fees data

students_df = pd.read_csv("C:\Users\hassa\OneDrive - Higher Education Commission\Desktop\PDC\HASSAN KHALID (21B-149-CS) ASSIGNMENT\students_data.csv")
fees_df = pd.read_csv("C:\Users\hassa\OneDrive - Higher Education Commission\Desktop\PDC\HASSAN KHALID (21B-149-CS) ASSIGNMENT\fees_data.csv")

# Ensure student_id columns are cleaned and converted to integers
students_df["student_id"] = students_df["student_id"].astype(str).str.strip().astype(int)
fees_df["student_id"] = fees_df["student_id"].astype(str).str.strip().astype(int)

# Debugging: Display unique student IDs for verification
print("Unique Student IDs in students_df:", students_df["student_id"].unique())
print("Unique Student IDs in fees_df:", fees_df["student_id"].unique())

# Function to find the most relevant fee submission date for a student
def find_most_relevant_fee_date(group):
    date_counts = group["fee_submission_date"].value_counts()
    if all(date_counts == 1):  # If all dates are unique, choose the latest one
        return group["fee_submission_date"].max()
    else:  # Otherwise, pick the most frequent date
        return date_counts.idxmax()

# Create a mapping of student_id to the most relevant fee submission date
relevant_dates_mapping = fees_df.groupby("student_id").apply(find_most_relevant_fee_date).reset_index()
relevant_dates_mapping.columns = ["student_id", "most_relevant_date"]

# Process each student and print the most relevant fee submission date
for _, student_row in students_df.iterrows():
    student_id = student_row["student_id"]
    if pd.notna(student_id):  # Ensure valid student ID
        print(f"\nProcessing Student ID: {student_id}")

        # Find the relevant date for the student from the mapping
        relevant_date_row = relevant_dates_mapping[relevant_dates_mapping["student_id"] == student_id]

        if not relevant_date_row.empty:
            relevant_date = relevant_date_row["most_relevant_date"].iloc[0]
            print(f"Most relevant fee submission date for Student ID {student_id}: {relevant_date}")
        else:
            print(f"No fee records found for Student ID {student_id}")
    else:
        print(f"Invalid Student ID: {student_id}")

