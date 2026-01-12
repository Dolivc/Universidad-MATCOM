import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from Tools import cargar_datos_mip, cargar_datos_Mercatoria
from Tools import pais_moda_arroz, pais_moda_frijoles
from Tools import mercatoria_moda, promedio_canasta_basica, heatmap_tabla, yogurt_data
datos_completos = cargar_datos_mip()
data_mer = cargar_datos_Mercatoria()

def g_moda_pais_comparativa(datos_completos, data_mercatoria):

    pais_arroz_mip, contador_arroz_mip = pais_moda_arroz(datos_completos)
    pais_frijoles_mip, contador_frijoles_mip = pais_moda_frijoles(datos_completos)
    
    Country_frij_mer, Count_frij_mer, Country_arroz_mer, Count_arroz_mer = mercatoria_moda(data_mercatoria)
        
    max_idx_arroz_mip = contador_arroz_mip.index(max(contador_arroz_mip))
    max_idx_frijoles_mip = contador_frijoles_mip.index(max(contador_frijoles_mip))

    max_idx_arroz_mer = Count_arroz_mer.index(max(Count_arroz_mer)) 
    max_idx_frijoles_mer = Count_frij_mer.index(max(Count_frij_mer)) 

    rojo_borgona = '#800020' 

    colores_paleta = [
        '#F7E7CE',  
        '#FBCEB1',  
        '#E2725B',  
        '#D2691E',  
        '#CF9B7A',  
        '#E6B8A2',  
        '#DEB887',  
    ]

    def generar_colores(indice_maximo, total_elementos):
        colores = []
        for i in range(total_elementos):
            if i == indice_maximo:
                colores.append(rojo_borgona)
            else:
                color_idx = (i % len(colores_paleta))
                colores.append(colores_paleta[color_idx])
        return colores

    colores_frijoles_mip = []
    if pais_frijoles_mip and max_idx_frijoles_mip is not None:
        colores_frijoles_mip = generar_colores(max_idx_frijoles_mip, len(pais_frijoles_mip))

    colores_arroz_mip = []
    if pais_arroz_mip and max_idx_arroz_mip is not None:
        colores_arroz_mip = generar_colores(max_idx_arroz_mip, len(pais_arroz_mip))

    colores_frijoles_mer = []
    if Country_frij_mer and max_idx_frijoles_mer is not None:
        colores_frijoles_mer = generar_colores(max_idx_frijoles_mer, len(Country_frij_mer))

    colores_arroz_mer = []
    if Country_arroz_mer and max_idx_arroz_mer is not None:
        colores_arroz_mer = generar_colores(max_idx_arroz_mer, len(Country_arroz_mer))
        fig = make_subplots(
            rows=2, 
            cols=2,
            specs=[[{'type':'domain'}, {'type':'domain'}],
                [{'type':'domain'}, {'type':'domain'}]],
            subplot_titles=("Frijoles - MIPYMES", "Arroz - MIPYMES",
                        "Frijoles - Mercatoria", "Arroz - Mercatoria"),
            vertical_spacing=0.15
        )
    
    if pais_frijoles_mip and contador_frijoles_mip:
        fig.add_trace(go.Pie(
            labels=pais_frijoles_mip,
            values=contador_frijoles_mip,
            textinfo='label+percent',
            marker=dict(colors=colores_frijoles_mip, line=dict(color='#000000', width=1))
        ), 1, 1)
    
    if pais_arroz_mip and contador_arroz_mip:
        fig.add_trace(go.Pie(
            labels=pais_arroz_mip,
            values=contador_arroz_mip,
            textinfo='label+percent',
            marker=dict(colors=colores_arroz_mip, line=dict(color='#000000', width=1))
        ), 1, 2)
    
    if Country_frij_mer and Count_frij_mer:
        fig.add_trace(go.Pie(
            labels=Country_frij_mer,
            values=Count_frij_mer,
            textinfo='label+percent',
            marker=dict(colors=colores_frijoles_mer, line=dict(color='#000000', width=1))
        ), 2, 1)
    
    if Country_arroz_mer and Count_arroz_mer:
        fig.add_trace(go.Pie(
            labels=Country_arroz_mer,
            values=Count_arroz_mer,
            textinfo='label+percent',
            marker=dict(colors=colores_arroz_mer, line=dict(color='#000000', width=1))
        ), 2, 2)

    fig.update_traces(hole=.4)
 
    fig.update_layout(
        title_text="Comparativa: Países que más exportan frijoles y arroz",
        title_font=dict(size=20, color='#EBCB6A'),
        paper_bgcolor="#111C15", 
        height=800,
        legend=dict(
            font=dict(color="#EBCB6A", size=13),
            bordercolor="#F4DDB8",
            borderwidth=1
        ),
    )

    fig.update_annotations(font=dict(size=14, color="#EBCB6A"))
    
    return fig

def barr_comp(datos_completos, data_mer):

    Country_frij_mer, Count_frij_mer, Country_arroz_mer, Count_arroz_mer = mercatoria_moda(data_mer)

    Country_frij_mip, Count_frij_mip = pais_moda_frijoles(datos_completos)
    Country_arroz_mip, Count_arroz_mip = pais_moda_arroz(datos_completos)

    paises_comunes_frij = []
    for pais in Country_frij_mer:
        if pais in Country_frij_mip:
            paises_comunes_frij.append(pais)

    paises_comunes_arroz = []
    for pais in Country_arroz_mer:
        if pais in Country_arroz_mip:
            paises_comunes_arroz.append(pais)

    frij_mer_values = []
    for pais in paises_comunes_frij:
        idx = Country_frij_mer.index(pais)
        frij_mer_values.append(Count_frij_mer[idx])

    frij_mip_values = []
    for pais in paises_comunes_frij:
        idx = Country_frij_mip.index(pais)
        frij_mip_values.append(Count_frij_mip[idx])

    arroz_mer_values = []
    for pais in paises_comunes_arroz:
        idx = Country_arroz_mer.index(pais)
        arroz_mer_values.append(Count_arroz_mer[idx])

    arroz_mip_values = []
    for pais in paises_comunes_arroz:
        idx = Country_arroz_mip.index(pais)
        arroz_mip_values.append(Count_arroz_mip[idx])

    frijoles_data = []
    i = 0
    for pais in paises_comunes_frij:
        frijoles_data.append({
            'pais': pais,
            'mercatoria': frij_mer_values[i],
            'mipymes': frij_mip_values[i]
        })

    arroz_data = []
    i = 0

    for pais in paises_comunes_arroz:
        arroz_data.append({
            'pais': pais,
            'mercatoria': arroz_mer_values[i],
            'mipymes': arroz_mip_values[i]
        })
        i += 1

    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=("Frijoles", "Arroz"),
        horizontal_spacing=0.15
    )

    if paises_comunes_frij:
        paises_frij = [item['pais'] for item in frijoles_data]
        valores_mer_frij = [item['mercatoria'] for item in frijoles_data]
        valores_mip_frij = [item['mipymes'] for item in frijoles_data]
        
        fig.add_trace(
            go.Bar(
                name='Mercatoria',
                x=paises_frij,
                y=valores_mer_frij,
                marker_color='#E2725B',
                text=valores_mer_frij,
                textposition='auto',
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                name='MIPYMES',
                x=paises_frij,
                y=valores_mip_frij,
                marker_color='#CF9B7A',
                text=valores_mip_frij,
                textposition='auto'
            ),
            row=1, col=1
        )

    if paises_comunes_arroz:
        paises_arroz = [item['pais'] for item in arroz_data]
        valores_mer_arroz = [item['mercatoria'] for item in arroz_data]
        valores_mip_arroz = [item['mipymes'] for item in arroz_data]
        

        fig.add_trace(
            go.Bar(
                name='Mercatoria',
                x=paises_arroz,
                y=valores_mer_arroz,
                marker_color='#E2725B',
                text=valores_mer_arroz,
                textposition='auto',
                showlegend=False
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Bar(
                name='MIPYMES',
                x=paises_arroz,
                y=valores_mip_arroz,
                marker_color='#CF9B7A',
                text=valores_mip_arroz,
                textposition='auto',
                showlegend=False
            ),
            row=1, col=2
        )

    fig.update_layout(
        title=dict(
            text='Comparación de Productos por País: Mercatoria vs MIPYMES',
            font=dict(size=20, color='#EBCB6A')
        ),

        paper_bgcolor="#111C15",
        plot_bgcolor="#111C15",
        
        legend=dict(
            font=dict(color="#EBCB6A", size=13),
            bordercolor="#F4DDB8",
            borderwidth=1,
            orientation="v",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    )

    fig.update_xaxes(
        tickangle=-45,
        tickfont=dict(color='#EBCB6A', size=12),
        title_font=dict(color='#EBCB6A', size=14),
        row=1, col=1
    )

    fig.update_xaxes(
        tickangle=-45,
        tickfont=dict(color='#EBCB6A', size=12),
        title_font=dict(color='#EBCB6A', size=14),
        row=1, col=2
    )

    fig.update_yaxes(
        tickfont=dict(color='#EBCB6A', size=12),
        title_font=dict(color='#EBCB6A', size=14),
        row=1, col=1
    )

    fig.update_yaxes(
        tickfont=dict(color='#EBCB6A', size=12),
        title_font=dict(color='#EBCB6A', size=14),
        row=1, col=2
    )

    fig.update_annotations(
        font=dict(color="#EBCB6A", size=16)
    )

    return fig



import plotly.graph_objects as go

def grafica_promedio_basica(datos_completos):
    producto, media = promedio_canasta_basica(datos_completos)

    max_idx = media.index(max(media))
    
    colores = []
    for i in range(len(producto)):
        if i == max_idx:
            colores.append('#800020') 
        else:
            colores.append("#301816")  
    

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=producto,
        y=media,
        marker_color=colores,
        text= media
    ))
    
    fig.update_layout(
        title=dict(
            text='Precios Promedio de Productos Básicos',
            font=dict(size=20, color='#EBCB6A')
        ),
        paper_bgcolor="#111C15",
        plot_bgcolor="#111C15",
        xaxis=dict(
            title='Productos',
            title_font=dict(color='#EBCB6A', size=14),
            tickfont=dict(color='#EBCB6A', size=12),
            tickangle=-45
        ),
        yaxis=dict(
            title='Precio Promedio ($)',
            title_font=dict(color='#EBCB6A', size=14),
            tickfont=dict(color='#EBCB6A', size=12)
        ),
        height=500
    )
    
    return fig

import plotly.graph_objects as go

def grafica_heatmap(data_mercatoria):

    table = heatmap_tabla(data_mercatoria)

    columns = ["Negros", "Blancos", "Pintos", "Colorados", "Lentejas", "Chicharos", "Garbanzos", "Chicharos verdes", "Chicharos amarillos"]
    rows = ["USA", "Brasil", "Argentina", "Cuba", "Mexico", "España", "Canada"]
    
    fig = go.Figure(data=go.Heatmap(
        z=table,
        x=columns,
        y=rows,
        colorscale='RdBu_r',  
        text=table,
        texttemplate='%{text:.2f}',
        textfont=dict(color='black', size=12)
    ))
    

    fig.update_layout(
        title=dict(
            text='Precio por Gramo de Frijoles por Tipo y País',
            font=dict(size=20, color='#EBCB6A')
        ),
        paper_bgcolor="#111C15",
        plot_bgcolor="#111C15",
        xaxis=dict(
            title='Tipo de Frijol',
            title_font=dict(color='#EBCB6A', size=14),
            tickfont=dict(color='#EBCB6A', size=12)
        ),
        yaxis=dict(
            title='País de Origen',
            title_font=dict(color='#EBCB6A', size=14),
            tickfont=dict(color='#EBCB6A', size=12)
        ),
        height=500
    )
    
    return fig

def yogurt_flavor_bar(yogurt_flavor):
    categorias = list(yogurt_flavor.keys())
    frecuencias = list(yogurt_flavor.values())
    
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categorias,
        y=frecuencias,
        marker_color='#808080',
        text=frecuencias,
        textposition='auto',
        textfont=dict(color='white', size=12)
    ))
    
    fig.update_layout(
        title=dict(
            text="Frecuencia Absoluta de Sabores de Yogurt",
            font=dict(size=20, color='#EBCB6A')
        ),
        paper_bgcolor="#111C15",
        plot_bgcolor="#111C15",
        xaxis=dict(
            title='Categorías',
            title_font=dict(color='#EBCB6A', size=14),
            tickfont=dict(color='#EBCB6A', size=12),
            tickangle=-45 if len(categorias) > 5 else 0
        ),
        yaxis=dict(
            title='Frecuencia',
            title_font=dict(color='#EBCB6A', size=14),
            tickfont=dict(color='#EBCB6A', size=12),
            gridcolor='rgba(235, 203, 106, 0.2)'
        ),
        height=500,
        margin=dict(t=80, l=80, r=40, b=120)
    )
    
    return fig

def yogurt_type_pie(yogurt_type):
    categorias = list(yogurt_type.keys())
    frecuencias = list(yogurt_type.values())
    
    colores_paleta = [
        '#F7E7CE', '#FBCEB1', '#E2725B', '#D2691E',
        '#CF9B7A', '#E6B8A2', '#DEB887', '#C19A6B'
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=categorias,
        values=frecuencias,
        textinfo='label+percent',
        marker=dict(
            colors=colores_paleta[:len(categorias)] if len(categorias) <= len(colores_paleta) 
            else colores_paleta * (len(categorias) // len(colores_paleta) + 1),
            line=dict(color='#000000', width=1)
        ),
        hole=0.3
    ))
    
    fig.update_layout(
        title=dict(
            text="Tipos de Yogurt en Mercatoria",
            font=dict(size=20, color='#EBCB6A')
        ),
        paper_bgcolor="#111C15",
        plot_bgcolor="#111C15",
        legend=dict(
            font=dict(color="#EBCB6A", size=12),
            bordercolor="#F4DDB8",
            borderwidth=1
        ),
        height=500
    )
    
    return fig
