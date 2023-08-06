from functools import reduce

import pandas as pd
import numpy as np

from banner.utils.const import NW_VOLTAGE, NW_CURRENT, NW_TEMP, NW_AUX_CHANNEL, NW_STEP_RANGE, NW_TIMESTAMP, NW_DATESTAMP, NW_CHANNEL_GROUP, NEWARE_FACTOR_COLUMNS, PREV_SUFFIX, OUTLIER_STD_COEFFECIENT

def calc_neware_cols(data: pd.DataFrame):
    data = data.sort_values([NW_DATESTAMP, NW_TIMESTAMP])
    
    data[NW_VOLTAGE] = data[NW_VOLTAGE].apply(lambda obj: obj / 10000)
    data[NW_CURRENT] = data.apply(lambda row: round(row[NW_CURRENT] * __current_coeff(row[NW_STEP_RANGE]), 4), axis=1)

    def __calc_timestamp(row, time_per_step):
        try:
            step = time_per_step[time_per_step.index < row[NW_DATESTAMP]].iloc[-1]

            return row[NW_TIMESTAMP] + step

        except (IndexError, AssertionError):
            return row[NW_TIMESTAMP]

    time_per_step = calc_neware_step_start(data)
    
    data[NW_TIMESTAMP] = data.apply(lambda row: __calc_timestamp(row, time_per_step), axis=1)
    
    if NW_TEMP in data:
        data[NW_TEMP] = data[NW_TEMP].apply(lambda obj: obj / 10)
    
        if NW_AUX_CHANNEL in data:
            data = __group_by_auxchl(data)
    
    # Drop factor columns
    data.drop(
        NEWARE_FACTOR_COLUMNS, 
        axis=1, 
        errors='ignore',
        inplace=True
    )

    return data

def __current_coeff(cur_range):
    return 0.00001 * 10**min(4, len(str(cur_range))) * (0.1 if cur_range < 0 else 1)
    
def __group_by_auxchl(data):
    merge_columns = [column for column in list(data.columns) if column not in [NW_TEMP, NW_AUX_CHANNEL]]
    
    # groupby -> to list & rename NW_AUX_CHANNEL
    group_as_list = [
        df.loc[
            :, df.columns != NW_AUX_CHANNEL
        ].rename(columns={NW_TEMP: f'{NW_CHANNEL_GROUP}{group}'})
        for group, df in data.groupby([NW_AUX_CHANNEL])
    ]
    
    # Merge 
    merged_data = reduce(lambda left,right: pd.merge(left, right, on=merge_columns, how='left'), group_as_list)

    return merged_data

def calc_dq_dv(data: pd.DataFrame, raw=False):
    ''' 
        Calculate DQ/DV for a valid neware df
        raw=False: remove outliers
    '''
    required_columns = [NW_VOLTAGE, NW_CURRENT, NW_TIMESTAMP]

    if not all(col in data for col in required_columns) or not isinstance(data, pd.DataFrame):
        raise TypeError(f'Calculating DQ/DV requires DataFrame with {required_columns} columns')
    
    df = data[required_columns]

    dt = df[NW_TIMESTAMP] - df[NW_TIMESTAMP].shift(1)
    
    dv = df[NW_VOLTAGE] - df[NW_VOLTAGE].shift(1)
    
    current = df[NW_CURRENT]
        
    dq = current * dt / 1000 / 3600
    
    dqdv = dq / dv

    if not raw:
        dqdv.replace([np.inf, -np.inf], np.nan, inplace=True)
        
        dqdv[(np.abs(dqdv - dqdv.mean()) > (OUTLIER_STD_COEFFECIENT * dqdv.std()))] = np.nan
        
    # Merge based on column (V)
    data['dqdv'] = dqdv

    return data


def calc_neware_step_start(data):
    required_columns = [NW_DATESTAMP, NW_TIMESTAMP]

    if not all(col in data for col in required_columns) or not isinstance(data, pd.DataFrame):
        raise TypeError(f'Calculating Neware Timestamp requires DataFrame with {required_columns} columns')

    df = data[required_columns]
    
    prev_timestamp, prev_datestamp = NW_TIMESTAMP + PREV_SUFFIX, NW_DATESTAMP + PREV_SUFFIX

    # Remove chained_assignment warning
    __chained_assignment = pd.options.mode.chained_assignment
    pd.options.mode.chained_assignment = None

    df[prev_timestamp] = df[NW_TIMESTAMP].shift(1)
    df[prev_datestamp] = df[NW_DATESTAMP].shift(1)
    
    # Restore chained_assignment warning
    pd.options.mode.chained_assignment = __chained_assignment
    
    __start_times = df.loc[
        df[NW_TIMESTAMP] == 0, 
        [prev_datestamp, prev_timestamp]
    ]
    
    start_times = __start_times[prev_timestamp].cumsum()
    start_times.index = __start_times[prev_datestamp]
    
    return start_times.dropna()
