import pandas as pd
import altair as alt
from pyodide.http import open_url

df = pd.read_csv(open_url("https://raw.githubusercontent.com/felicyairenea/Snapchat-Project/main/data/IN-ADH-90-days.csv"))

#data cleaning
df = df.drop(columns=['inventory_id', 'campaign_id', 'adgroup_id', 'video_id', 'UU'])
df = df.dropna(axis=0)

df['adgroup_name'] = df['adgroup_name'].str.split(':')
df['adgroup'] = df.adgroup_name.apply(lambda x: x[0])
df['adtype'] = df.adgroup_name.apply(lambda x: x[1])
df = df.drop(columns=['adgroup_name'])

#trying to transform daily data into weekly data
#new_df = df.copy()
#new_df.index = new_df.Date
#new_df = new_df.resample('1W').mean()
#print(new_df.head().to_html())

alt.data_transformers.disable_max_rows()

pts = alt.selection(type = 'single', encodings=['x'])

bar = alt.Chart(df).mark_bar().encode(
    alt.X('week(Date):N', title='Day of week'),
    alt.Y('average(cost_usd):Q', title='Average Cost (in USD)'),
    color='month(Date):N',
    tooltip = ['adgroup','adtype','cost_usd','Date']
).add_selection(
    pts
)

rect = alt.Chart(df).mark_bar().encode(
    alt.X('impressions:Q', bin=True),
    alt.Y('clicks:Q', bin=True),
    color=alt.condition(pts, 'clicks:Q', alt.value('lightgray'))
)

line = alt.Chart(df).mark_line().encode(
    alt.X('day(Date):N'),
    alt.Y('average(d7_retention):Q'),
    color='month(Date):N'
)

bar | rect | line