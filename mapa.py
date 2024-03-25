import folium
import json
import pandas as pd
#Criando mapa
import basedosdados as bd
import plotly.express as px
import plotly.graph_objects as go

def plot_mapa():
    mapa = folium.Map(location = [-22.92, -43.36],
     zoom_start=11)
    estado = 'Limite_de_Bairros.geojson' #Colocar caminho do local do arquivo json
    geo_json_data = json.load(open(estado)) #ler arquivo json
    

    #Opção1
    folium.GeoJson(geo_json_data).add_to(mapa)
    mapa.save('mapa.html')
    return mapa

def plotlymapa():
    df = pd.read_csv('db/data/rj-cor.adm_cor_comando.ocorrencias.csv')
    fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', color='gravidade', 
                        color_discrete_sequence=["RGBA(0, 255, 255, 0.15)",
                                                  "RGBA(150, 255, 0, 0.15)", 
                                                  "RGBA(0, 255, 0, 0.15)", 
                                                  "RGBA(0, 255, 0, 0.15)", 
                                                  "RGBA(255, 0, 255, 0.15)",
                                                  "RGBA(200, 240, 0, 0.15)",
                                                  "RGBA(0, 0, 255, 0.15)"],
                        hover_data=['tipo', 'gravidade', 'bairro', 'status'],
                        template='plotly_dark',
                        center=dict(lat=-22.92, lon=-43.36), zoom=11)
    fig.update_layout(
    mapbox_style="carto-darkmatter")

    #chamadas
    df = pd.read_csv('db/data/datario.adm_central_atendimento_1746.chamado.csv')
    fig.add_trace(px.scatter_mapbox(df, lat='latitude', lon='longitude', color='categoria',
                                    hover_data=['categoria',
                                               'unidade_organizacional_ouvidoria',
                                               'tipo',
                                               'situacao',
                                               'reclamacoes'],
                                    color_discrete_sequence= ["RGBA(255, 0, 0, 0.15)"]).data[0])
    
    #clima_fluviometro
    df1 = pd.read_csv('db/data/rj-cor.clima_fluviometro.lamina_agua_inea.csv')
    df2 = pd.read_csv('db/data/rj-cor.clima_pluviometro.estacoes_alertario.csv')
    df = pd.merge(df1, df2, on='id_estacao', how='inner')
    df.dropna(subset=['latitude', 'longitude', 'altura_agua'], inplace=True)
    fig.add_trace(px.scatter_mapbox(df, lat='latitude', lon='longitude', size='altura_agua', color='estacao',
                                    hover_data=['estacao',
                                                'data_medicao',
                                                'altura_agua',
                                                'situacao'],
                                    color_discrete_sequence= ["RGBA(255, 255, 0, 0.15)"]).data[0])
    
    #clima_pluviometro websirene
    df1 = pd.read_csv('db/data/rj-cor.clima_pluviometro.estacoes_websirene.csv')
    df2 = pd.read_csv('db/data/rj-cor.clima_pluviometro.taxa_precipitacao_alertario_5min.csv')
    df = pd.merge(df1, df2, on='id_estacao', how='inner')
    df.dropna(subset=['latitude', 'longitude', 'acumulado_chuva_30min'], inplace=True)
    fig.add_trace(px.scatter_mapbox(df, lat='latitude', lon='longitude', size='acumulado_chuva_30min', color='estacao',
                                    hover_data=['estacao',
                                                'data_medicao',
                                                'acumulado_chuva_5min',
                                                'acumulado_chuva_10min',
                                                'acumulado_chuva_15min',
                                                'acumulado_chuva_30min',
                                                'acumulado_chuva_1h',
                                                'acumulado_chuva_2h',
                                                'acumulado_chuva_3h',
                                                'acumulado_chuva_4h',
                                                'acumulado_chuva_6h',
                                                'acumulado_chuva_12h',
                                                'acumulado_chuva_24h',
                                                'acumulado_chuva_96h',
                                                'acumulado_chuva_mes'],
                                    color_discrete_sequence= ["RGBA(0, 0, 255, 0.15)"]).data[0])

    #precipitação cemadem
    df1 = pd.read_csv('db/data/rj-cor.clima_pluviometro.estacoes_cemaden.csv')
    df2 = pd.read_csv('db/data/rj-cor.clima_pluviometro.taxa_precipitacao_cemaden.csv')
    df = pd.merge(df1, df2, on='id_estacao', how='inner')
    df.dropna(subset=['latitude', 'longitude', 'acumulado_chuva_1_h'], inplace=True)
    fig.add_trace(px.scatter_mapbox(df, lat='latitude', lon='longitude', size='acumulado_chuva_1_h', color='estacao',
                                    hover_data=['estacao',
                                                'acumulado_chuva_10_min',
                                                'acumulado_chuva_1_h',
                                                'acumulado_chuva_3_h',
                                                'acumulado_chuva_6_h',
                                                'acumulado_chuva_12_h',
                                                'acumulado_chuva_24_h',
                                                'acumulado_chuva_48_h',
                                                'acumulado_chuva_72_h',
                                                'acumulado_chuva_96_h'],
                                    color_discrete_sequence= ["RGBA(0, 0, 255, 0.15)"]).data[0])
    
    #precipitacao inea
    df1 = pd.read_csv('db/data/rj-cor.clima_pluviometro.estacoes_inea.csv')
    df2 = pd.read_csv('db/data/rj-cor.clima_pluviometro.taxa_precipitacao_inea.csv')
    df = pd.merge(df1, df2, on='id_estacao', how='inner')
    df.dropna(subset=['latitude', 'longitude', 'acumulado_chuva_1_h'], inplace=True)
    fig.add_trace(px.scatter_mapbox(df, lat='latitude', lon='longitude', size='acumulado_chuva_1_h', color='estacao',
                                    hover_data=['estacao',
                                                'acumulado_chuva_15_min',
                                                'acumulado_chuva_1_h',
                                                'acumulado_chuva_4_h',
                                                'acumulado_chuva_24_h',
                                                'acumulado_chuva_96_h',
                                                'acumulado_chuva_30_d'],
                                    color_discrete_sequence= ["RGBA(0, 0, 255, 0.15)"]).data[0])

    #precipitacao websirene
    df1 = pd.read_csv('db/data/rj-cor.clima_pluviometro.estacoes_websirene.csv')
    df2 = pd.read_csv('db/data/rj-cor.clima_pluviometro.taxa_precipitacao_websirene.csv')
    df = pd.merge(df1, df2, on='id_estacao', how='inner')
    df.dropna(subset=['latitude', 'longitude', 'acumulado_chuva_1_h'], inplace=True)
    fig.add_trace(px.scatter_mapbox(df, lat='latitude', lon='longitude', size='acumulado_chuva_1_h', color='estacao',
                                    hover_data=['estacao',
                                                'acumulado_chuva_15_min',
                                                'acumulado_chuva_1_h',
                                                'acumulado_chuva_4_h',
                                                'acumulado_chuva_24_h',
                                                'acumulado_chuva_96_h',
                                                'horario'],
                                    color_discrete_sequence= ["RGBA(0, 0, 255, 0.15)"]).data[0])

    #alagamento
    df = pd.read_csv('db/data/rj-rioaguas.saneamento_drenagem.ponto_supervisionado_alagamento.csv')
    fig.add_trace(px.scatter_mapbox(df, lat='latitude', lon='longitude', color='classe', 
                                    hover_data=['classe', 
                                                'causa_alagamento', 
                                                'medida_cor', 'eliminado', 
                                                'bacia_hidrografica', 
                                                'sub_bacia_hidrografica'],
                                    color_discrete_sequence= ["RGBA(255, 255, 0, 0.15)"]).data[0])
    
    


    fig.write_html('html/mapa.html')


    return fig

#plot_mapa()
plotlymapa()

