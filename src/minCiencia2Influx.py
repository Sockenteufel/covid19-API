# de https://www.influxdata.com/blog/getting-started-writing-data-to-influxdb/
# leemos los outputs de MinCiencia y los escribimos al formato nativo de influx:
# <measurement>[,<tag-key>=<tag-value>...] <field-key>=<field-value>[,<field2-key>=<field2-value>...] [unix-nano-timestamp]
# Prueba 1: measurement = cada campo; tags = region o rango etareo y sexo, y hay que convertir los timestamps


import pandas as pd
import unidecode
import numpy as np
import time
from datetime import datetime

relevantCSVs = {
    'prod1': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19_std.csv',
    'prod2': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto6/bulk/data.csv', ## Prod 1
    'prod3': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo_std.csv',
    'prod4': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto11/bulk/producto4.csv', ## Prod 5
    'prod5': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales_std.csv',
    'prod6': '',  # this is prod 2
    'prod7': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto7/PCR_std.csv',
    'prod8': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto8/UCI_std.csv',
    'prod9': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto9/HospitalizadosUCIEtario_std.csv',
    'prod10': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario_std.csv',
    'prod11': '',  # this is prod 4
    'prod12': '',  # this is prod 7
    'prod13': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto13/CasosNuevosCumulativo_std.csv',
    'prod14': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo_std.csv',
    'prod15': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/FechaInicioSintomasHistorico_std.csv',
   # 'prod15.2': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/SemanasEpidemiologicas.csv',
    'prod16': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto16/CasosGeneroEtario_std.csv',
    'prod17': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto17/PCREstablecimiento_std.csv',
    'prod18': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto18/TasaDeIncidencia_std.csv',
    'prod19': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna_std.csv',
    'prod20': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto20/NumeroVentiladores_std.csv',
    'prod21.1': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto21/SintomasCasosConfirmados_std.csv',
    'prod21.2': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto21/SintomasHospitalizados_std.csv',
    'prod22.1': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto22/HospitalizadosEtario_Acumulado_std.csv',
    'prod22.2': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto22/HospitalizadosUCI_Acumulado_std.csv',
    'prod23': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto23/PacientesCriticos_std.csv',
    'prod24': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto24/CamasHospital_Diario_std.csv',
    'prod25': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto25/CasosActualesPorComuna_std.csv',
    'prod26': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto26/CasosNuevosConSintomas_std.csv',
    'prod27': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto27/CasosNuevosSinSintomas_std.csv',
    'prod28': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto28/FechaInicioSintomas_reportadosSEREMIHistorico_std.csv',
    'prod29': '', #geo product
    'prod30': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto30/PacientesVMI_std.csv',
    'prod31': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto31/Nacimientos_std.csv',
    'prod32': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto32/Defunciones_std.csv',
    'prod33': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto33/IndiceDeMovilidad_std.csv',
    'prod34': '', #geo product
    'prod35': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto35/Comorbilidad_std.csv',
    'prod36': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto36/ResidenciasSanitarias_std.csv',
    'prod37': ''

}


def fileWriter(path, lines):
    thefile = open(path, 'w')
    header = ['# DML', '# CONTEXT-DATABASE: covid19']
    for line in header:
        thefile.write("%s\n" % line)
    for item in lines:
        thefile.write("%s\n" % item)


def prod1ToLine(df, path):
    lines = []
    for d in range(len(df)):
        lines.append('Casos_confirmados_comunal,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_region="' + str(df['Codigo region'][d]) + '",'
                     + 'Comuna="' + unidecode.unidecode(str(df['Comuna'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_comuna="' + str(df['Codigo comuna'][d]) + '"'
                     + ' '
                     # Fields

                     + 'Poblacion=' + str(df['Poblacion'][d]) + ","
                     + 'Casos_confirmados=' + str(df['Casos confirmados'][d])
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod3ToLine(df, path):
    lines = []
    for d in range(len(df)):
        lines.append('Casos_acumulados_regional,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Casos_acumulados=' + str(df['Total'][d])
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod5ToLine(df, path):
    lines = []
    for d in range(len(df)):
        lines.append('Totales_nacionales,'
                     # TAGS are used to check if measurements are the same
                     + 'Serie="' + unidecode.unidecode(str(df['Dato'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['Total'][d])
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod7ToLine(df, path):
    lines = []
    for d in range(len(df)):
        lines.append('PCR_Regional,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_region="' + str(df['Codigo region'][d]) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['numero'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod8ToLine(df, path):
    lines = []
    for d in range(len(df)):
        lines.append('UCI_Regional,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_region="' + str(df['Codigo region'][d]) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['numero'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod9ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('UCI_Etario,'
                     # TAGS are used to check if measurements are the same
                     + 'Grupo_de_edad="' + unidecode.unidecode(str(df['Grupo de edad'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['Casos confirmados'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["fecha"][d]).value)
                     )
    fileWriter(path, lines)

def prod10ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('Fallecidos_Etario,'
                     # TAGS are used to check if measurements are the same
                     + 'Grupo_de_edad="' + unidecode.unidecode(str(df['Grupo de edad'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['Casos confirmados'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod13ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('Casos_nuevos_cumulativo_regional,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['Total'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)

def prod14ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('Fallecidos_cumulativo_regional,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['Total'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod15ToLine(df, path):
    lines = []
    df2 = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/SemanasEpidemiologicas.csv')
    for d in range(len(df)):
        lines.append('Inicio_sintomas_comunal,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_region="' + str(df['Codigo region'][d]) + '",'
                     + 'Comuna="' + unidecode.unidecode(str(df['Comuna'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_comuna="' + str(df['Codigo comuna'][d]) + '",'
                     + 'Publicacion="' + str(df['Publicacion'][d]) + '"'
                     + ' '
                     # Fields
                     + 'Poblacion=' + str(df['Poblacion'][d]) + ","
                     + 'Casos_confirmados=' + str(df['Casos confirmados'][d])
                     + ' '
                     + str(pd.to_datetime(df2.loc[[0], df["Semana Epidemiologica"][d]][0]).value)
                     )
    fileWriter(path, lines)


def prod16ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('Casos_genero_Etario,'
                     # TAGS are used to check if measurements are the same
                     + 'Grupo_de_edad="' + unidecode.unidecode(str(df['Grupo de edad'][d]).replace(' ', '_')) + '",'
                     + 'Sexo="' + unidecode.unidecode(str(df['Sexo'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['Casos confirmados'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod17ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('PCR_tipo_establecimiento,'
                     # TAGS are used to check if measurements are the same
                     + 'Establecimiento="' + unidecode.unidecode(str(df['Establecimiento'][d]).replace(' ', '_')) + '",'
                     + 'Examenes="' + unidecode.unidecode(str(df['Examenes'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['Numero de PCR'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod18ToLine(df, path):
    lines = []
    for d in range(len(df)):
        lines.append('Tasa_de_incidencia_comunal,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_region="' + str(df['Codigo region'][d]) + '",'
                     + 'Comuna="' + unidecode.unidecode(str(df['Comuna'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_comuna="' + str(df['Codigo comuna'][d]) + '"'
                     + ' '
                     # Fields

                     + 'Poblacion=' + str(df['Poblacion'][d]) + ","
                     + 'Tasa_de_incidencia=' + str(df['Tasa de incidencia'][d])
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)

def prod19ToLine(df, path):
    lines = []
    for d in range(len(df)):
        lines.append('Casos_activos_comunal,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_region="' + str(df['Codigo region'][d]) + '",'
                     + 'Comuna="' + unidecode.unidecode(str(df['Comuna'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_comuna="' + str(df['Codigo comuna'][d]) + '"'
                     + ' '
                     # Fields

                     + 'Poblacion=' + str(df['Poblacion'][d]) + ","
                     + 'Casos_activos=' + str(df['Casos activos'][d])
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)

def prod20ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('Ventiladores_nacional,'
                     # TAGS are used to check if measurements are the same
                     + 'Ventiladores="' + unidecode.unidecode(str(df['Ventiladores'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['numero'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["fecha"][d]).value)
                     )
    fileWriter(path, lines)

def prod21_1ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('Sintomas_casos_confirmados,'
                     # TAGS are used to check if measurements are the same
                     + 'Sintomas="' + unidecode.unidecode(str(df['Sintomas'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['numero'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod21_2ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('Sintomas_hospitalizados,'
                     # TAGS are used to check if measurements are the same
                     + 'Sintomas="' + unidecode.unidecode(str(df['Sintomas'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['numero'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod22_1ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('Hospitalizados_etario,'
                     # TAGS are used to check if measurements are the same
                     + 'Grupo_de_edad="' + unidecode.unidecode(str(df['Grupo de edad'][d]).replace(' ', '_')) + '",'
                     + 'Sexo="' + unidecode.unidecode(str(df['Sexo'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['numero'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod22_2ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('Hospitalizados_UCI_etario,'
                     # TAGS are used to check if measurements are the same
                     + 'Grupo_de_edad="' + unidecode.unidecode(str(df['Grupo de edad'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['numero'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["fecha"][d]).value)
                     )
    fileWriter(path, lines)

def prod23ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('Pacientes_criticos'
                     # TAGS are used to check if measurements are the same
                     #+ 'Pacientes_criticos="' + unidecode.unidecode(str(df['Sintomas'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['Casos confirmados'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod24ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('Camas_hospital,'
                     # TAGS are used to check if measurements are the same
                     + 'Tipo_de_cama="' + unidecode.unidecode(str(df['Tipo de cama'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['Casos confirmados'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod25ToLine(df, path):
    lines = []
    for d in range(len(df)):
        lines.append('Casos_actuales_comunal,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_region="' + str(df['Codigo region'][d]) + '",'
                     + 'Comuna="' + unidecode.unidecode(str(df['Comuna'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_comuna="' + str(df['Codigo comuna'][d]) + '"'
                     + ' '
                     # Fields

                     + 'Poblacion=' + str(df['Poblacion'][d]) + ","
                     + 'Casos_actuales=' + str(df['Casos actuales'][d])
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)

def prod28ToLine(df,path):
    lines = []
    df2 = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/SemanasEpidemiologicas.csv')
    for d in range(len(df)):
        lines.append('Inicio_sintomas_reportados,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_region="' + str(df['Codigo region'][d]) + '",'
                     + 'Publicacion="' + str(df['Publicacion'][d]) + '"'
                     + ' '
                     # Fields
                     + 'Casos_confirmados=' + str(df['Casos confirmados'][d])
                     + ' '
                     + str(pd.to_datetime(df2.loc[[0], df["Semana Epidemiologica"][d]][0]).value)
                     )
    fileWriter(path, lines)

def prod30ToLine(df, path):
    lines = []
    df = df.replace('<=', 'menor que ', regex=True)
    df = df.replace('>=', 'mayor que ', regex=True)
    for d in range(len(df)):
        lines.append('Pacientes_VMI'
                     # TAGS are used to check if measurements are the same
                     #+ 'Pacientes_criticos="' + unidecode.unidecode(str(df['Sintomas'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['Casos confirmados'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod31ToLine(df, path):
    lines = []
    for d in range(len(df)):
        lines.append('Nacimientos_comunal,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_region="' + str(df['Codigo region'][d]) + '",'
                     + 'Comuna="' + unidecode.unidecode(str(df['Comuna'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_comuna="' + str(df['Codigo comuna'][d]) + '"'
                     + ' '
                     # Fields
                     + 'Nacimientos=' + str(df['Nacimientos'][d])
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod32ToLine(df, path):
    lines = []
    for d in range(len(df)):
        lines.append('Defunciones_comunal,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_region="' + str(df['Codigo region'][d]) + '",'
                     + 'Comuna="' + unidecode.unidecode(str(df['Comuna'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_comuna="' + str(df['Codigo comuna'][d]) + '"'
                     + ' '
                     # Fields
                     + 'Defunciones=' + str(df['Defunciones'][d])
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod33ToLine(df, path):
    lines = []
    #Region,Codigo region,Comuna,Codigo comuna,Superficie_km2,Poblacion,Fecha,variable,value
    for d in range(len(df)):
        lines.append('Indice_de_movilidad,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_region="' + str(df['Codigo region'][d]) + '",'
                     + 'Comuna="' + unidecode.unidecode(str(df['Comuna'][d]).replace(' ', '_')) + '",'
                     + 'Codigo_comuna="' + str(df['Codigo comuna'][d]) + '",'
                     + 'Serie="' + unidecode.unidecode(str(df['variable'][d])) + '"'
                     + ' '
                     # Fields
                     + 'Poblacion=' + str(df['Poblacion'][d]) + ","
                     + 'Superficie_km2=' + str(df['Superficie_km2'][d]) + ","
                     + 'Indice=' + str(df['value'][d])
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)

def prod35ToLine(df, path):
    lines = []
    for d in range(len(df)):
        lines.append('Comorbilidad,'
                     # TAGS are used to check if measurements are the same
                     + 'Comorbilidad="' + unidecode.unidecode(str(df['Comorbilidad'][d]).replace(' ', '_')) + '",'
                     + 'Hospitalización="' + unidecode.unidecode(str(df['Hospitalización'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['Casos confirmados'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)


def prod36ToLine(df, path):
    lines = []
    for d in range(len(df)):
        lines.append('Residencias_sanitarias,'
                     # TAGS are used to check if measurements are the same
                     + 'Region="' + unidecode.unidecode(str(df['Region'][d]).replace(' ', '_')) + '",'
                     + 'Categoria="' + unidecode.unidecode(str(df['Categoria'][d]).replace(' ', '_')) + '"'
                     + ' '
                     # Fields
                     + 'Total=' + str(df['Numero'][d]).replace('-', '0')
                     + ' '
                     + str(pd.to_datetime(df["Fecha"][d]).value)
                     )
    fileWriter(path, lines)


def csv2line(input):
    if input != '':
        df = pd.read_csv(input)
        df = df.fillna(0)
        print((list(df)))
        if 'producto1/Covid-19_std.csv' in input:
            prod1ToLine(df, '../output/p1-chronograf.txt')
        if 'producto3/' in input:
            prod3ToLine(df, '../output/p3-chronograf.txt')
        if 'producto5' in input:
            prod5ToLine(df, '../output/p5-chronograf.txt')
        if 'producto7' in input:
            prod7ToLine(df, '../output/p7-chronograf.txt')
        if 'producto8' in input:
            prod8ToLine(df, '../output/p8-chronograf.txt')
        if 'producto9' in input:
            prod9ToLine(df, '../output/p9-chronograf.txt')
        if 'producto10' in input:
            prod10ToLine(df, '../output/p10-chronograf.txt')
        if 'producto13' in input:
            prod13ToLine(df, '../output/p13-chronograf.txt')
        if 'producto14' in input:
            prod14ToLine(df, '../output/p14-chronograf.txt')
        if 'producto15' in input:
            prod15ToLine(df, '../output/p15-chronograf.txt')
        if 'producto16' in input:
            prod16ToLine(df, '../output/p16-chronograf.txt')
        if 'producto17' in input:
            prod17ToLine(df, '../output/p17-chronograf.txt')
        if 'producto18' in input:
            prod18ToLine(df, '../output/p18-chronograf.txt')
        if 'producto19' in input:
            prod19ToLine(df, '../output/p19-chronograf.txt')
        if 'producto20' in input:
            prod20ToLine(df, '../output/p20-chronograf.txt')
        #prod 21
        if 'SintomasCasosConfirmados' in input:
            prod21_1ToLine(df, '../output/p21_1-chronograf.txt')
        if 'SintomasHospitalizados' in input:
        #prod 22
            prod21_2ToLine(df, '../output/p21_2-chronograf.txt')
        if 'HospitalizadosEtario_Acumulado' in input:
            prod22_1ToLine(df, '../output/p22_1-chronograf.txt')
        if 'HospitalizadosUCI_Acumulado' in input:
            prod22_2ToLine(df, '../output/p22_2-chronograf.txt')
        if 'producto23' in input:
            prod23ToLine(df, '../output/p23-chronograf.txt')
        if 'producto24' in input:
            prod24ToLine(df, '../output/p24-chronograf.txt')
        if 'producto25' in input:
            prod25ToLine(df, '../output/p25-chronograf.txt')
        if 'producto28' in input:
            prod28ToLine(df, '../output/p28-chronograf.txt')
        if 'producto30' in input:
            prod30ToLine(df, '../output/p30-chronograf.txt')
        if 'producto31' in input:
            prod31ToLine(df, '../output/p31-chronograf.txt')
        if 'producto32' in input:
            prod32ToLine(df, '../output/p32-chronograf.txt')
        if 'producto33' in input:
            prod33ToLine(df, '../output/p33-chronograf.txt')
        if 'producto35' in input:
            prod35ToLine(df, '../output/p35-chronograf.txt')
        if 'producto36' in input:
            prod36ToLine(df, '../output/p36-chronograf.txt')




if __name__ == '__main__':

    for k in relevantCSVs:
        print('Checking ' + k + ': ' + relevantCSVs[k])
        df = csv2line(relevantCSVs[k])
