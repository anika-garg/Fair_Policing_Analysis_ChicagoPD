#!usr/bin/env python3
#
# Author(s):    Roman Rivera (Invisible Institute)

'''clean script for complaints-complaints_2000-2018_2018-03_18-060-157'''

import pandas as pd
import __main__

from clean_functions import clean_data
import setup


def get_setup():
    ''' encapsulates args.
        calls setup.do_setup() which returns constants and logger
        constants contains args and a few often-useful bits in it
        including constants.write_yamlvar()
        logger is used to write logging messages
    '''
    script_path = __main__.__file__
    args = {
        'input_file': 'input/complaints-complaints_2000-2018_2018-03.csv.gz',
        'output_file': 'output/complaints-complaints_2000-2018_2018-03.csv.gz'
        }

    assert (args['input_file'].startswith('input/') and
            args['input_file'].endswith('.csv.gz')),\
        "input_file is malformed: {}".format(args['input_file'])
    assert (args['output_file'].startswith('output/') and
            args['output_file'].endswith('.csv.gz')),\
        "output_file is malformed: {}".format(args['output_file'])

    return setup.do_setup(script_path, args)


cons, log = get_setup()

df = pd.read_csv(cons.input_file)
df = clean_data(df, log)
log.info('Purging phone numbers')
df['street_name'].fillna('', inplace=True)
df.loc[df['street_name'].str.contains(r'[0-9][0-9][0-9].{0,1}[0-9][0-9][0-9][0-9]') |
       df['street_name'].str.contains('phone',case=False),
       'street_name'] = ''
df.to_csv(cons.output_file, **cons.csv_opts)
