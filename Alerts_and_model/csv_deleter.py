import os
import glob
import time


def csv_deleter():
    folder_path = "C:/Users/Hemant Pathak/OneDrive/Desktop/chill/twitter_scrapper/tweets"

    # 📂 Match only .csv files
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    # 📦 Sort by last modified time (most recent first)
    csv_files.sort(key=os.path.getmtime, reverse=True)

    # 🔢 Number of files to keep
    keep_count = 2

    # 🧽 Files to delete
    files_to_delete = csv_files[keep_count:]

    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")
