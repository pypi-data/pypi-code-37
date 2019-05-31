import os
import calendar
import pandas as pd
import numpy as np
from .country_mapping import mapping

def load():
    url = 'https://en.wikipedia.org/wiki/List_of_next_general_elections'
    tables = pd.read_html(url, match='Parliamentary')
    df = pd.concat(tables)

    cols = ['country', 'fair', 'gdp', 'ihdi',
            'power', 'parl_prev', 'parl_next', 'parl_term',
            'pop', 'pres_prev', 'pres_next', 'pres_term', 'status']

    keep_cols = ['country', 'parl_prev', 'parl_next', 'parl_term',
                 'pres_prev', 'pres_next', 'pres_term']

    df.columns = cols
    df = df[keep_cols]

    # Remove countries with no next election info
    df = df[df.parl_next.notnull()]

    # Convert previous election to datetime
    df['parl_prev'] = pd.to_datetime(df.parl_prev)

    # Remove footnotes
    df.parl_term = df.parl_term.str.split('[', expand=True)[0]
    df.pres_term = df.pres_term.str.split('[', expand=True)[0]

    df = df.drop(['pres_prev', 'pres_next', 'pres_term'], axis=1)

    df['parl_next_year'] = df.parl_next.str[-4:]#.astype(int)
    df['parl_next_month'] = df.parl_next.str.extract('(\D+)')
    df.parl_next_month = df.parl_next_month.str.strip()
    df['parl_next_day'] = df.parl_next.str.extract('(\d{1,2}) ')#.astype(float).astype('Int64')

    month_names = list(calendar.month_name)

    df.parl_next_month = df.parl_next_month.apply(lambda x: month_names.index(x) if x in month_names else np.nan)
    df.parl_next_month = df.parl_next_month.astype('Int64').astype(str).str.replace('nan', '')

    df.parl_next = df.apply(lambda x: f'{x.parl_next_year}-{str(x.parl_next_month)}-{str(x.parl_next_day)}', axis=1)
    df.parl_next = df.parl_next.str.replace('-nan', '').str.replace('-$', '', regex=True)
    df.parl_term = df.parl_term.str.split(' ', expand=True)[0]
    df.country = df.country.replace('Korea', 'South Korea')
    df['iso_3'] = df.country.map(mapping)

    df = df.drop('country', axis=1).rename(columns={'iso_3': 'country'})
    df = df[['country', 'parl_prev', 'parl_term', 'parl_next']]
    df['election'] = df.apply(lambda x: f'{x.country}_{x.parl_next[:4]}', axis=1)
    df = df[['election', 'country', 'parl_prev', 'parl_term', 'parl_next']]

    return df


def to_ddf(df, path, name):
    df[['country']].to_csv(os.path.join(path, 'ddf--entities--country.csv'), index=False)
    df.to_csv(os.path.join(path, 'elections.csv'), index=False)
