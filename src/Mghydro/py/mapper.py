"""
Makes a nice little map in an .html file for viewing in a web browser
using a bit of javascript and Leaflet.
"""
import pandas as pd
from jinja2 import Template
from config import MAP_FOLDER, VERBOSE
import os

def create_folder_if_not_exists(folder_path: str) -> bool:
    """
    Check if a folder exists at the specified path. If not, create it.

    :param folder_path: The path of the folder to check/create.
    :return: True if the folder exists or is created, False otherwise.
    """
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            if VERBOSE: print(f"Created folder: {folder_path}")
        else:
            pass  # Folder is already there

        return True

    except Exception as e:
        print(f"Error creating folder: {e}")
        return False

def make_map(df: pd.DataFrame) -> bool:
    """

    input:
        df: a Pandas dataframe with the cols [id, lat, lng, name, area_reported, area_calc, result]

    returns:
        True if it successfully wrote the file viewer.html.
        Otherwise, the function will raise some kind of error message

    """
    # Reorganize the columns a bit so it looks good.
    # Here is the full set of columns, and the order I like
    cols_sorted = ['id', 'name', 'result', 'lat', 'lng', 'lat_snap', 'lng_snap', 'snap_dist', 'area_reported',
                   'area_calc', 'perc_diff']

    #if not HIGH_RES:
    #    cols_sorted.remove('lat_snap')
    #    cols_sorted.remove('lng_snap')


    # Get the actual columns in our table, because it can vary depending on user inputs.
    df['id'] = df.index
    cols = df.columns.tolist()
    for col in cols_sorted:
        if col not in cols:
            cols_sorted.remove(col)

    df = df[cols_sorted]

    if 'area_reported' in cols:
        df['area_reported'] = df['area_reported'].map('{:,.0f}'.format)

    df['area_calc'] = df['area_calc'].map('{:,.0f}'.format)
    df['lat'] = df['lat'].map('{:,.3f}'.format)
    df['lng'] = df['lng'].map('{:,.3f}'.format)

    if 'lat_snap' in cols:
        df['lat_snap'] = df['lat_snap'].map('{:,.3f}'.format)
        df['lng_snap'] = df['lng_snap'].map('{:,.3f}'.format)
        df.replace("nan", "", inplace=True)

    # Drop rows where result == 'failed'; these won't display correctly
    df = df[df.result != 'failed']

    # Use a jinja template to create the html file
    template_file = "py/viewer_template.html"
    with open(template_file, 'r') as f:
        template_str = f.read()

    template = Template(template_str)

    # Give the columns nicer names
    columns = df.columns.to_list()
    col_names = {
        'id': 'id',
        'name': 'Name',
        'result': 'Result',
        'lat': 'Lat',
        'lng': 'Lng',
        'lat_snap': 'Lat snap',
        'lng_snap': 'Lng snap',
        'snap_dist': 'Snap dist (m)',
        'area_reported': 'Area est. (km<sup>2</sup>)',
        'area_calc': 'Area calc. (km<sup>2</sup>)',
        'perc_diff': "Perc. diff."
    }

    pretty_columns = [col_names[c] for c in columns]

    html = template.render(
        rows=df.to_dict(orient='records'),
        columns=pretty_columns,
        cols=columns
    )

    # Make sure the folder is there. If not, try to create it.
    create_folder_if_not_exists(MAP_FOLDER)

    viewer_fname = f"{MAP_FOLDER}/_viewer.html"
    f = open(viewer_fname, 'w')
    f.write(html)
    f.close()

    return True
