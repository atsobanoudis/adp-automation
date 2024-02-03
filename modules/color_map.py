import pandas as pd

def load_color_mapping(filepath):
    """Load color mappings from a file."""
    mapping = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                color, type_ = line.strip().split(',')
                mapping[color] = type_
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        raise
    return mapping

def apply_color_mapping_to_df(df, mapping):
    """Apply color mappings to the DataFrame."""
    df['type'] = df['color'].map(mapping).fillna('Unknown')
    return df.drop('color', axis=1)

def update_df_with_color_mapping(df, filepath='color_mapping.txt'):
    """Load color mapping and apply it to the DataFrame."""
    mapping = load_color_mapping(filepath)
    return apply_color_mapping_to_df(df, mapping)
