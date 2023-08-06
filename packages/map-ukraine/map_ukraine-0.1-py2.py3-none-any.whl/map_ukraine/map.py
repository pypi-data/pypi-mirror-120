import pandas as pd
import plotly.express as px
import os
import json


def map(df, region_key_column, data_column,level, color_continuous_scale="Blues", marker_line_width=1, marker_line_color='white', title=None):

    if level not in [0,1,2]:
        raise Exception("Level should be in [0,1,2]")

    shape_city = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'map_data', 'UKR_admin{}.geojson'.format(level))
    with open(shape_city) as file:
        geojson = json.load(file)

    data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'map_data', 'UKR_admin{}.csv'.format(level))
    df_base = pd.read_csv(data_file)

    df_merged = df_base.merge(df, left_on='ID_{}'.format(level), right_on=region_key_column)

    fig=px.choropleth(df,
                        geojson=geojson,
                        featureidkey='properties.ID_{}'.format(level),
                        locations=df_merged['ID_{}'.format(level)],
                        #  animation_frame='Year',       #dataframe
                        color=df_merged[data_column],
                        color_continuous_scale=color_continuous_scale,
                        title=title ,
                  )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(marker_line_width=marker_line_width)
    fig.update_traces(marker_line_color=marker_line_color)

    return fig



if __name__=="__main__":
    data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'map_data', 'UKR_admin2.csv')
    df = pd.read_csv(data_file)

    fig = map(df,'ID_2','ID_2',2)
    fig.show()

    data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'map_data', 'UKR_admin2.csv')
    df = pd.read_csv(data_file)

    fig = map(df, 'ID_1', 'ID_1', 1)
    fig.show()

    data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'map_data', 'UKR_admin2.csv')
    df = pd.read_csv(data_file)

    fig = map(df, 'ID_0', 'ID_0', 0)
    fig.show()