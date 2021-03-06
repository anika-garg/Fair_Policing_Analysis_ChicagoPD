#!usr/bin/env python
#
# Author(s):    Roman Rivera (Invisible Institute)

'''import script for complaints-investigators_2000-2016_2016-11_p046957'''

import pandas as pd
import __main__

from import_functions import read_p046957_file, collect_metadata
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
        'input_files': [
            'input/p046957_-_report_1.1_-_all_complaints_in_time_frame.xls',
            'input/p046957_-_report_1.2_-_all_complaints_in_time_frame.xls',
            'input/p046957_-_report_1.3_-_all_complaints_in_time_frame.xls',
            'input/p046957_-_report_1.4_-_all_complaints_in_time_frame.xls',
            'input/p046957_-_report_1.5_-_all_complaints_in_time_frame.xls',
            'input/p046957_-_report_1.6_-_all_complaints_in_time_frame.xls'
            ],
        'output_file': 'output/complaints-investigators_2000-2016_2016-11.csv.gz',
        'metadata_file': 'output/metadata_complaints-investigators_2000-2016_2016-11.csv.gz',
        'column_names': [
            'cr_id', 'full_name', 'current_unit',
            'current_rank', 'current_star', 'appointed_date'
            ]
        }

    assert all(input_file.startswith('input/')
               for input_file in args['input_files']),\
        "An input_file is malformed: {}".format(args['input_files'])
    assert (args['output_file'].startswith('output/') and
            args['output_file'].endswith('.csv.gz')),\
        "output_file is malformed: {}".format(args['output_file'])

    return setup.do_setup(script_path, args)


cons, log = get_setup()


data_df = pd.DataFrame()
meta_df = pd.DataFrame()

for input_file in cons.input_files:
    df, report_produced_date, FOIA_request = \
                            read_p046957_file(input_file,
                                              original_crid_col='Number:',
                                              isnull='Number:',
                                              notnull='Location Code:',
                                              drop_col='Beat:')
    log.info(('Processing {0} file, of FOIA number {1}, produced on {2}'
              '').format(input_file, FOIA_request, report_produced_date))
    cons.write_yamlvar("{}-Report_Produced_Date".format(input_file),
                       report_produced_date)
    cons.write_yamlvar("{}-FOIA_Request".format(input_file),
                       FOIA_request)

    df.columns = cons.column_names

    data_df = (data_df
               .append(df)
               .reset_index(drop=True))

    meta_df = (meta_df
               .append(collect_metadata(df, input_file, cons.output_file))
               .reset_index(drop=True))

data_df.insert(0, 'row_id', data_df.index+1)
data_df.to_csv(cons.output_file, **cons.csv_opts)
meta_df.to_csv(cons.metadata_file, **cons.csv_opts)
