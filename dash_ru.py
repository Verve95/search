# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas
from datetime import datetime
import datetime
import searchconsole
import pandas as pd

#account = searchconsole.authenticate(client_config='client_secret_test_1.json', serialize='test_key_sc.json')



account = searchconsole.authenticate(client_config='/Users/administrator/Downloads/client_secret_test_1.json', credentials='/Users/administrator/Downloads/test_key_sc-2.json')
webproperty= account['https://skyup.aero/']
exampleGSC = webproperty.query.range('2021-01-04', '2021-01-17').dimension('query', 'date').get()
exampleBVreport = pd.DataFrame(data=exampleGSC)

from pymystem3 import Mystem
m = Mystem()

def lemmas(purpose):
    lemma = m.lemmatize(purpose)
    return lemma

exampleBVreport['lemm_word'] = exampleBVreport['query'].apply(lemmas)


def lemm_category(rows):
    if 'skyup' in rows:
        return 'skyup'
    if 'скай' in rows:
        return 'skyup'
    if 'sky' in rows:
        return 'skyup'
    if 'скайап' in rows:
        return 'skyup'

    if 'up' in rows:
        return 'skyup'
    if 'crfq' in rows:
        return 'skyup'
    if 'ылнгз' in rows:
        return 'skyup'
    if 'crfqfg' in rows:
        return 'skyup'

    if 'ска' in rows and 'ап' in rows:
        return 'skyup'
    if 'ску' in rows and 'ап' in rows:
        return 'skyup'
    if 'скац' in rows and 'ап' in rows:
        return 'skyup'
    if 'скуап' in rows and 'ап' in rows:
        return 'skyup'

    if 'сай' in rows and 'ап' in rows:
        return 'skyup'
    if 'сеай' in rows and 'ап' in rows:
        return 'skyup'
    if 'скаяп' in rows:
        return 'skyup'
    if 'флай' in rows and 'ап' in rows:
        return 'skyup'

    if 'суай' in rows and 'ап' in rows:
        return 'skyup'
    if 'скаап' in rows:
        return 'skyup'
    if 'сквйап' in rows:
        return 'skyup'
    if 'скацап' in rows:
        return 'skyup'

    else:
        return 'other'


exampleBVreport['key'] = exampleBVreport['query'].apply(lemm_category)
search_c = pd.DataFrame(exampleBVreport.groupby(['date', 'key'])[['impressions', 'clicks']].sum()).reset_index()
search_c['date'] = pd.to_datetime(search_c['date'])
#search_c["Date"] = pd.to_datetime(search_c["date"], format="%Y-%m-%d")
search_c['date_create'] = search_c['date'].dt.date
search_c['year'] = search_c['date'].dt.year
search_c['month'] = search_c['date'].dt.month
#search_c['week']  = search_c['date'].dt.week
search_c['year_week'] = search_c['date'].dt.strftime('%Y-%U')
search_c['wk'] = search_c['date'].apply(lambda x: str(x.isocalendar()[0]) + '-' +
                                       str(x.isocalendar()[1]).zfill(2))
search_c['wk'] = search_c['wk'].replace('-', '', regex=True) + ['-W']
#search_c['ISO'] = pd.DataFrame(search_c['year'].astype(str) + '-W' + search_c['week'].astype(str) + '-1')
df_skyup = search_c.query('key == "skyup"')
df_other = search_c.query('key == "other"')
df_skyup_clicks = pd.DataFrame(df_skyup.groupby('wk')['clicks'].sum()).reset_index()
df_skyup_imp = pd.DataFrame(df_skyup.groupby('wk')['impressions'].sum()).reset_index()

df_other_clicks = pd.DataFrame(df_other.groupby('wk')['clicks'].sum()).reset_index()
df_other_imp = pd.DataFrame(df_other.groupby('wk')['impressions'].sum()).reset_index()


app = dash.Dash()

# Предыдущий вариант без подключения
# df = pd.read_csv('/Users/administrator/Downloads/search_c.csv')
# df["Date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
# df_skyup = df.query('key == "skyup"')
# df_other = df.query('key == "other"')
# df.sort_values("Date", inplace=True)
# app = dash.Dash()
# Предыдущий вариант без подключения

app.layout = html.Div(
    children=[
        html.H1(children="Статистика запросов из Search Console"),
        html.P(
            children=""
            ,
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df_skyup_clicks["wk"],
                        "y": df_skyup_clicks["clicks"],
                        "type": "bar",
                        "name": "clicks",
                    },
                    {
                        "x": df_skyup_imp["wk"],
                        "y": df_skyup_imp["impressions"],
                        "type": "bar",
                        "name": "impressions",
                    },
                ],
                "layout": {"title": "Статистика запросов из Search Console по брендовым запросам"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df_other_clicks["wk"],
                        "y": df_other_clicks["clicks"],
                        "type": "bar",
                        "name": "clicks",
                    },
                    {
                        "x": df_other_imp["wk"],
                        "y": df_other_imp["impressions"],
                        "type": "bar",
                        "name": "impressions",
                    },
                ],
                    "layout": {"title": "Статистика запросов из Search Console по НЕ брендовым запросам"},
            },

        ),
    ]
)




if __name__ == '__main__':
    app.run_server(debug=True)
