#!/usr/bin/env python3

import sys
import csv
import config
import itertools
import base64
from jinja2 import Template

def match_xy(designator, xylist):
    for line in xylist:
        xy_designator = line[config.config['pnp']['designator_col']]
        if xy_designator.lower().strip() == designator.lower().strip():
            x = line[config.config['pnp']['x_col']]
            y = line[config.config['pnp']['y_col']]
            rot = line[config.config['pnp']['rot_col']]
            layer = line[config.config['pnp']['layer_col']]
            try:
                x = x.replace('mil', '')
                y = y.replace('mil', '')
                x = float(x)
                y = float(y)
                rot = float(rot)
            except ValueError:
                print('warning: could not parse xy data as numbers')
                return None
            if layer.lower()[0] == 't':
                layer = 'TOP'
            elif layer.lower()[0] == 'b':
                layer = 'BOTTOM'
            else:
                print('warning: could not parse layer ID in xy file')
                return None
            return (x, y, rot, layer)
    return None


def match_inventory(pn, invlist):
    for line in invlist:
        inv_pn = line[config.config['inventory']['pn_col']]
        if inv_pn.lower().strip() == pn.lower().strip():
            return line[config.config['inventory']['location_col']]
    return None


def read_bom(bomlist, layer, xylist, invlist):
    matching = {}

    for line in bomlist:
        designators = line[config.config['bom']['designator_col']]
        designator_list = [x.strip() for x in designators.split(',')]

        pn = line[config.config['bom']['pn_col']]
        description = line[config.config['bom']['description_col']]
        location = match_inventory(pn, invlist)

        for designator in designator_list:
            match = match_xy(designator, xylist)
            if match is None:
                print('error: no xy data for {}'.format(designator))
                sys.exit()
            else:
                if match[3] == layer:
                    matching.setdefault((pn, description, location), []).append({
                        'designator': designator,
                        'pnp': {
                            'x': match[0],
                            'y': match[1],
                            'rot': match[2]
                        }
                    })
    return matching


def print_components(components):
    for (pn, description, location), components in components.items():
        if location is None:
            location = '**** NO INVENTORY DATA AVAILABLE ****'

        print('Take {} of {} ({}) from {}'.format(len(components), pn, description, location))
        for component in components:
            print('    * {} \t@(x: {}, y: {}, rot: {}deg)'.format(component['designator'],
                                                                  component['pnp']['x'],
                                                                  component['pnp']['y'],
                                                                  component['pnp']['rot']))

if __name__ == '__main__':
    try:
        bomfile = open(config.config['bom']['file'], 'r')
    except (OSError, IOError) as e:
        print('error: could not open BOM file: {}'.format(e))
        sys.exit()

    try:
        xyfile = open(config.config['pnp']['file'], 'r')
    except (OSError, IOError) as e:
        print('error: could not open PNP XY file: {}'.format(e))
        sys.exit()

    try:
        invfile = open(config.config['inventory']['file'], 'r')
    except (OSError, IOError) as e:
        print('error: could not open inventory file: {}'.format(e))
        sys.exit()

    try:
        templatefile = open(config.config['template'], 'r')
        templatestr = templatefile.read()
        outputfile_top = open(config.config['output_top'], 'w')
        outputfile_bot = open(config.config['output_bottom'], 'w')
    except (OSError, IOError) as e:
        print('error: could not open template file: {}'.format(e))
        sys.exit()

    xyreader = csv.reader(xyfile, delimiter=config.config['delimiter'], quotechar=config.config['quotechar'])
    xylist = list(itertools.islice(xyreader, config.config['pnp']['rd_start'], None))

    bomreader = csv.reader(bomfile, delimiter=config.config['delimiter'], quotechar=config.config['quotechar'])
    bomlist = list(itertools.islice(bomreader, config.config['bom']['rd_start'], None))

    invreader = csv.reader(invfile, delimiter=config.config['delimiter'], quotechar=config.config['quotechar'])
    invlist = list(itertools.islice(invreader, config.config['inventory']['rd_start'], None))

    print()
    print('TOP LAYER COMPONENTS')
    print('--------------------')
    components_top = read_bom(bomlist, 'TOP', xylist, invlist)
    print_components(components_top)
    print()
    print('BOTTOM LAYER COMPONENTS')
    print('-----------------------')
    components_bottom = read_bom(bomlist, 'BOTTOM', xylist, invlist)
    print_components(components_bottom)
    print()
    print('DONE')
    print('----')

    template = Template(templatestr)
    rendered = template.render(components=components_top,
                               board_img="data:image/png;base64," + base64.b64encode(open(config.config['graphics']['image_top'], "rb").read()).decode('ascii'),
                               config=config.config['graphics'])
    outputfile_top.write(rendered)
    print('{} written'.format(config.config['output_top']))

    rendered = template.render(components=components_bottom,
                               board_img="data:image/png;base64," + base64.b64encode(open(config.config['graphics']['image_bottom'], "rb").read()).decode('ascii'),
                               config=config.config['graphics'])
    outputfile_bot.write(rendered)
    print('{} written'.format(config.config['output_bottom']))
