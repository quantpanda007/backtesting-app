import pandas as pd

def load_data_from_folder(filepath):
    """Load and preprocess CSV file from a folder."""
    try:
        # Load CSV
        data = pd.read_csv(filepath, index_col=0, parse_dates=True)

        # Ensure data is numeric
        data = data.apply(pd.to_numeric, errors='coerce')

        # Drop any columns or rows with all NaN values
        data = data.dropna(how='all', axis=1).dropna(how='all', axis=0)

        if data.empty:
            raise ValueError("The file contains no valid data.")

        return data
    except Exception as e:
        raise ValueError(f"Failed to load data: {e}")
