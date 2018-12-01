import pandas as pd

## T
margins = pd.read_excel('Margins2.xlsx')
margins = margins.melt(id_vars='date', value_name='rack', var_name='area_name')
## T
#price_cols = margins.columns[margins.columns.str.contains('price')]
#tax_cols = margins.columns[margins.columns.str.contains('tax')]

## Test
refining_cols = margins.columns[margins.columns.str.contains('refining')]

margins = pd.melt(margins, id_vars='Day of', value_vars=refining_cols,
                  value_name='refining_margin', var_name='city_name')

margins['refining_margin'] = margins.groupby('city_name')['refining_margin'].ffill()
margins.city_name = margins.city_name.str.replace('refining_margin_', '')
