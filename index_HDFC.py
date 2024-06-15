import pandas as pd
import numpy as np

def load_and_process_data(file_path):
    try:
        df = pd.read_excel(file_path)
        print("Data loaded successfully.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except ValueError as e:
        print(f"Value error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
    # Check for missing columns
    expected_columns = ["Date", "Narration", "Chq./Ref.No.", "Value Dt", "Withdrawal Amt.", "Deposit Amt.", "Closing Balance"]
    for col in expected_columns:
        if col not in df.columns:
            print(f"Missing expected column: {col}")
            return None

    # Drop rows where Date is missing
    df.dropna(subset=['Date'], inplace=True)
    
    # Convert 'Date' column to datetime
    try:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    except Exception as e:
        print(f"Error converting 'Date' column to datetime: {e}")
        return None

    # Fill NaNs in numeric columns with 0
    df['Withdrawal Amt.'] = df['Withdrawal Amt.'].fillna(0)
    df['Deposit Amt.'] = df['Deposit Amt.'].fillna(0)
    df['Closing Balance'] = df['Closing Balance'].fillna(method='ffill')

    # Group by 'Date' and calculate daily statistics
    daily_stats = df.groupby('Date').agg({
        'Withdrawal Amt.': ['sum', 'mean', 'max', 'min', 'count'],
        'Deposit Amt.': ['sum', 'mean', 'max', 'min', 'count'],
        'Closing Balance': ['last']
    }).reset_index()

    # Flatten the column names
    daily_stats.columns = ['_'.join(col).strip() if col[1] else col[0] for col in daily_stats.columns.values]

    return daily_stats

file_path = r'C:\Users\KIIT\Desktop\Devops And Cloud Engineering\Generative AI Tech, Data & Finance (May Batch)\Gen AI Assignment 1\HDFC_2.xlsx'
daily_stats = load_and_process_data(file_path)

if daily_stats is not None:
    print("Daily statistics calculated successfully.")
    print(daily_stats.head())
else:
    print("Failed to calculate daily statistics.")
