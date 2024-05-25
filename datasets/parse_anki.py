import sqlite3
import zipfile
import os
import pandas as pd


def extract_apkg(apkg_file: str, extracted_folder: str):
    with zipfile.ZipFile(apkg_file, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)


def fetch_data(db_path: str) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:

        cursor = conn.cursor()

        # Query to get the data from a table, e.g., cards
        cursor.execute("""
        SELECT 
            n.flds as fields
        FROM notes n
        JOIN cards c ON n.id = c.nid
        """)
        cards_data = cursor.fetchall()

        # Optionally, convert to pandas DataFrame for easier manipulation
        cards_df = pd.DataFrame(cards_data, columns=[description[0] for description in cursor.description])

    return cards_df


if __name__ == '__main__':
    # Define paths

    apkg_file = 'data/apkg_anki/Maths_sup_dfinitions_thormes_proprits.apkg'
    extracted_folder = './data/.cache/extracted_apkg'
    db_path = os.path.join(extracted_folder, 'collection.anki2')

    extract_apkg(apkg_file, extracted_folder)
    cards_df = fetch_data(db_path)

    cards_df = cards_df['fields'].str.split('\x1f', expand=True)
    cards_df.columns = ['front', 'back']
    cards_df.to_csv("math.csv", index=False)


