import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

from IPython.display import display
from pprint import pprint
from tqdm import tqdm
import logging

import ipywidgets as widgets
import ipysheet 
import os, io, json


brackets_alias = [
    ('$0', '0'), 
    ('$1-$10,000', '1'), 
    ('$10,001-$50,000', '2'),
    ('$50,001-$100,000', '3'),
    ('$100,001-$500,000', '4'),
    ('$500,001-$1,000,000', '5'),
    ('over $1,000,000', '6'),
    ('delete this row', '-99'),
    ('special case', '99'), # special case
]

# utils
def safe_lmerge(
        df_left:pd.DataFrame, 
        df_right:pd.DataFrame, 
        on:list, 
        suffixes=('_left', '_right'),
        verbose = False,
        *args,
        **kwargs,
    ) -> pd.DataFrame:
    
    # remove redundant columns
    df_left = df_left.loc[:, ~df_left.columns.duplicated()]
    df_right = df_right.loc[:, ~df_right.columns.duplicated()]

    assert isinstance(on, list), '"on" should be of list type.'
    for key in on:
        assert key in df_left.columns, f'at least one of the keys, {key}, is not in the columns of df_left'
        assert key in df_right.columns, f'at least one of the keys, {key}, is not in the columns of df_right'

    # make sure all numeric columns are of type float, so that np.nan can be taken care. For example, a column including integer and nan will cast into float type.
    for key in on:
        if np.issubdtype(df_left[key].dtypes, np.number) and np.issubdtype(df_right[key].dtypes, np.number):
            df_left[key] = df_left[key].astype(float)
            df_right[key] = df_right[key].astype(float)

    for key in on:
        assert df_left[key].dtypes == df_right[key].dtypes, f'The type of "{key}" is not the same (left: {df_left[key].dtypes}, right: {df_right[key].dtypes})'
        
    # check if there is any NAs in the merging keys
    n_left_orig = df_left.shape[0]
    n_right_orig = df_right.shape[0]
    # df_left = df_left.dropna(subset=on)
    df_right = df_right.dropna(subset=on)
    n_left_new = df_left.shape[0]
    n_right_new = df_right.shape[0]

    # merge
    df_output = df_left.merge(df_right, on=on, how='left', suffixes=suffixes)


    shape_left = df_left.shape
    shape_output = df_output.shape
    if n_left_new == 0 or n_right_new==0:
        pass

    if verbose:
        print(f'''
        ======================================================================
        Check NAs before merging
        key: {on}
        ----------------------------------------------------------------------
        df_left: {n_left_orig} -> {n_left_new} (losing {(100-100*n_left_new/n_left_orig) if n_left_orig != 0 else np.nan:.2f} %)
        df_right: {n_right_orig} -> {n_right_new} (losing {(100-100*n_right_new/n_right_orig) if n_right_orig != 0 else np.nan:.2f}%)

        ----------------------------------------------------------------------
        Check if df_left is inflated because of duplicated {on}
        ----------------------------------------------------------------------
        shape : {shape_left} -> {shape_output}
        #(additional rows) = {shape_output[0] - shape_left[0]}
        #(additional columns) = {shape_output[1] - shape_left[1]}
        ======================================================================
        ''')

    return df_output

class Dashboard:
    def __init__(self):
        self.DIR_DATA_FMO_MANUAL_ITEMS = None
        self.year = None
        self.df = pd.DataFrame()
        self.df_brackets = pd.DataFrame(brackets_alias, columns = ['fmo', 'alias'])

    def set_parameters(self, year=None, dir_fmo_manual_items='data/fmo_manual_items', dir_fmo_html_contents='data/fmo_html_contents', dir_fmo_machine_items='data/fmo_machine_items'):
        self.DIR_DATA_FMO_HTML_CONTENTS = dir_fmo_html_contents
        self.DIR_DATA_FMO_MACHINE_ITEMS = dir_fmo_machine_items
        self.DIR_DATA_FMO_MANUAL_ITEMS = dir_fmo_manual_items
        self.year = year
        
        df = self.get_df_to_be_collected()
        if year is not None:
            df = df.query(f'(fyedt >= "{self.year}-01-01") and (fyedt <= "{self.year}-12-31")')
        self.df = df
        print(f'''
        [Dashboard] data to be collceted 
            sample period = ({self.df.fyedt.min()}, {self.df.fyedt.max()})
            #(url) = {self.df.url.nunique()}
            #(url, series) =  {self.df.drop_duplicates(subset=['url', 'series']).shape[0]}
        ''')

    def get_df_to_be_collected(self):
        df = (
            self.get_df_latest_snapshot()

            # select only those that need to be collected
            .loc[lambda x: x.fmo.isna(), ]     
        )
        return df

    def generator_df_series(self):
        assert not self.df.empty, 'Please run dashboard.set_parameters(year=year, dir_fmo_manual_items="data") first.'        
        grouped = self.df.groupby('url')
        urls = list(grouped.groups.keys())
        while len(urls) > 1:
            idx = np.random.randint(0, len(urls))
            url = urls.pop(idx)
            df_fmo_prefilled = self.get_existing_fmo_machine_items(url)
            df_url = grouped.get_group(url)
            for series, df_series in df_url.groupby('series'):
                df_series = (
                    df_series
                    .drop(columns=['fmo'])
                    .pipe(safe_lmerge, df_right=df_fmo_prefilled, on=['series_name', 'manager_name'])
                )
                yield ((url, series), df_series)

    def get_all_fmo_manual_items(self):
        assert self.DIR_DATA_FMO_MANUAL_ITEMS is not None, 'Please run dashboard.set_parameters(dir_fmo_manual_items="data") first. '
        fs = os.listdir(self.DIR_DATA_FMO_MANUAL_ITEMS)
        assert len(fs) != 0, f'there is no data in the directory "{self.DIR_DATA_FMO_MANUAL_ITEMS}".'
        # assert columns are included
        df = (
            pd.concat([
                pd.read_csv(f'{self.DIR_DATA_FMO_MANUAL_ITEMS}/{f}')
                for f in fs
                if f.endswith('.csv')
            ])
            .loc[:, ['fyedt', 'series', 'series_name', 'manager_name', 'fmo', 'url', 'who', 'collected_at']]
            
            # type
            .assign(
                series_name = lambda x: x.series_name.str.lower(), 
                manager_name = lambda x: x.manager_name.str.lower(),
            ) 
        )
        return df

    def get_df_latest_snapshot(self):
        df = (
            self.get_all_fmo_manual_items()
            
            # keep the most updated manual fmo
            .sort_values('collected_at', ascending = False)
            .drop_duplicates(subset=['fyedt', 'series_name', 'manager_name'], keep='first')
            
            # remove wrong manager name
            .query('(fmo != "delete this row")')
        )
        return df
        
    def get_filename_root(self, url:str) -> str:
        filename_root = f"{url.split('/data/')[-1].replace('/', '_').replace('.txt', '')}"
        return filename_root

    def get_filename_fmo_machine_items(self, url:str) -> str:
        filename_root = self.get_filename_root(url)
        filename = f'{self.DIR_DATA_FMO_MACHINE_ITEMS}/{filename_root}.csv'
        return filename

    def get_existing_fmo_machine_items(self, url:str) -> str:
        df = pd.DataFrame(columns=['series_name', 'manager_name', 'fmo'])
        filename = self.get_filename_fmo_machine_items(url)
        if os.path.exists(filename):
            df = (
                pd.read_csv(filename)
                .loc[:, ['edgar_series_name', 'msd_mgr_name', 'fmo']]
                .rename(columns = {'edgar_series_name': 'series_name', 'msd_mgr_name': 'manager_name'})
                .drop_duplicates()
            )
        return df

    def get_existing_fmo_html_contents(self, url:str) -> str:
        filename = f'{self.DIR_DATA_FMO_HTML_CONTENTS}/{self.get_filename_root(url)}.json'
        if not os.path.exists(filename):
            raise ValueError(f'not yet parse fmo html contents for {url}')
        with io.open(filename, mode='r', encoding='utf-8') as f:
            contents = json.load(f)
        return contents
    
    def map_alias_to_fmo(self, alias, fmo):
        '''
        alias must be string e.g. "3", "99", "-99"
        '''
        if not isinstance(alias, str):
            return None
        fmo_alias_mapping = self.df_brackets.set_index('alias').fmo.to_dict()
        if alias != '99':
            fmo = fmo_alias_mapping.get(alias, None)
        return fmo 


dashboard = Dashboard()

class SheetUI:
    def __init__(self, url, series, df_series):
        self.url = url
        self.series = series
        self.df_series = df_series
        self.sheet_input = self.load_sheet()
        
        # setup buttons
        self.set_buttons()
        
        # parameter
        self.has_saved = False

    def load_sheet(self):
        # initiate sheet
        df_input = (
            self.df_series
            .pipe(safe_lmerge, df_right=dashboard.df_brackets, on=['fmo']) # add alias
            .loc[:, ['fyedt', 'series_name', 'manager_name', 'fmo', 'alias']]
        )
        sheet_input = ipysheet.from_dataframe(df_input)
        sheet_input.row_headers = True # important for ipysheet.to_dataframe to function correctly on added rows
        return sheet_input

    def set_buttons(self):        
        output = widgets.Output()

        # add one row => update cell value
        self.row_button = widgets.Button(description='Add Row')
        self.row_button.on_click(self.add_row)

        # refresh 
        self.button_refresh = widgets.Button(description="Fill fmo")
        self.button_refresh.on_click(self.refresh_fmo)

    def add_row(self, b):
        self.sheet_input.rows += 1
        for colname, col in zip(self.sheet_input.column_headers, self.sheet_input.cells): # this assumes that each cell is a column, this might break otherwise
            col.row_end +=1 
            new_value = col.value[-1] if colname in ['fyedt', 'series_name'] else None
            col.value = col.value + [new_value]

    def refresh_fmo(self, b):
        self.sheet_input.cells[-1].value = [x if (x in dashboard.df_brackets.alias.tolist()) else None  for x in self.sheet_input.cells[-1].value]
        vals = []
        fmo_alias_mapping = dashboard.df_brackets.set_index('alias').fmo.to_dict()
        fmos = self.sheet_input.cells[-2].value
        aliases = self.sheet_input.cells[-1].value
        for fmo, alias in zip(fmos, aliases):
            if alias != '99':
                fmo = fmo_alias_mapping.get(alias, None)
            vals.append(fmo)
        self.sheet_input.cells[-2].value = vals

    def display(self):
        display(self.row_button)
        display(self.sheet_input)
        display(self.button_refresh)
    

if __name__ == '__main__':
    dashboard.set_parameters(
        year=2012, 
        dir_fmo_manual_items='/Users/chiayiyen/Dropbox/fmo_manual_collection/data/fmo_manual_items', 
        dir_fmo_html_contents='/Users/chiayiyen/Dropbox/fmo_manual_collection/data/fmo_html_contents', 
        dir_fmo_machine_items='/Users/chiayiyen/Dropbox/fmo_manual_collection/data/fmo_machine_items'
    )
    gen_df_series = dashboard.generator_df_series()
    for x in gen_df_series:
        print(x)
    pass