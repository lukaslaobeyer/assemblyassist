config = {
    'templatedir': 'template/',
    'output_top': 'output/assemblyassist_top.html',
    'output_bottom': 'output/assemblyassist_bot.html',
    'delimiter': ',', # CSV delimiter
    'quotechar': '"', # CSV quote character
    'bom': {
        'file': 'input/bom.csv', # BOM filename
        'rd_start': 1, # Index of line to start reading at (0-indexed)
        'pn_col': 1, # Part number column index
        'designator_col': 7, # Designator(s) column index
        'value_col': 4, # Part value column index
        'description_col': 5, # Part description column index
    },
    'pnp': {
        'file': 'input/xy.csv', # Filename of CSV file containing XY pick and place information
        'rd_start': 2, # Index of line to start reading at (0-indexed)
        'designator_col': 0, # Designator column index
        'layer_col': 4, # Layer column index
        'rot_col': 5, # Rotation column index
        'x_col': 2, # X coordinate column index
        'y_col': 3, # Y coordinate column index
    },
    'inventory': {
        'file': 'input/inventory.csv', # Filename of CSV file containing component location in inventory
        'rd_start': 1, # Index of line to start reading at (0-indexed)
        'pn_col': 0, # Part number column index
        'location_col': 6, # Part inventory location column index
    },
    'graphics': {
        'offset_x': 0, # X coordinate of the origin for the PnP xy file
        'offset_y': 0, # Y coordinate of the origin for the PnP xy file
        'flip_x': False, # Invert X
        'flip_y': False, # Invert Y
        'width': 4251.969, # Width of the board
        'image_top': 'input/board_top.png',
        'image_bottom': 'input/board_bottom.png'
    }
}
