# de https://www.influxdata.com/blog/getting-started-writing-data-to-influxdb/
# leemos los outputs de MinCiencia y los escribimos al formato nativo de influx:
# <measurement>[,<tag-key>=<tag-value>...] <field-key>=<field-value>[,<field2-key>=<field2-value>...] [unix-nano-timestamp]
# Prueba 1: measurement = cada campo; tags = region o rango etareo y sexo, y hay que convertir los timestamps


import pandas as pd
import unidecode

relevantCSVs = {
    'prod1': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19_std.csv',
    'prod2': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto6/bulk/data.csv',
    'prod3': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo_std.csv',
    'prod4': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto11/bulk/producto4.csv',
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
    'prod15.1': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/FechaInicioSintomas_std.csv',
    'prod15.2': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/SemanasEpidemiologicas.csv',
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
    'prod28': 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto28/FechaInicioSintomas_reportadosSEREMI_std.csv',
    }


def csv2line(input):
    if input != '':
        df = pd.read_csv(input)
        if 'fecha' in df.columns.str.lower():
            print(input + ' is time-series')
            print(list(df))
            if 'producto1/Covid-19_std.csv' in input:
                lines = ['"Casos confirmados comunal"'
                         + ' '
                         + 'Region=' + unidecode.unidecode(str(df['Region'][d])) + ","
                         + '"Codigo region"=' + str(df['Codigo region'][d]) + ","
                         + 'Comuna=' + unidecode.unidecode(str(df['Comuna'][d])) + ","
                         + '"Codigo comuna"=' + str(df['Codigo comuna'][d]) + ","
                         + 'Poblacion=' + str(df['Poblacion'][d]) + ","
                         + '"Casos confirmados"=' + str(df['Casos confirmados'][d])
                         + " " + str(df["Fecha"][d]) for d in range(len(df))
                         ]

                thefile = open('../output/p1-chronograf.txt', 'w')
                for item in lines:
                    thefile.write("%s\n" % item)

        else:
            print('check ' + input + ' for is not a time series')
            print(list(df))


if __name__ == '__main__':

    for k in relevantCSVs:
        print('Checking ' + k + ': ' + relevantCSVs[k])
        df = csv2line(relevantCSVs[k])

"""
#convert csv's to line protocol

#convert sample output to line protocol (with nanosecond precision)
df = pd.read_csv("output/BTC_sm_ns.csv")
lines = [“price”
         + ",type=BTC"
         + " "
         + "close=" + str(df["close"][d]) + ","
         + "high=" + str(df["high"][d]) + ","
         + "low=" + str(df["low"][d]) + ","
         + "open=" + str(df["open"][d]) + ","
         + "volume=" + str(df["volume"][d])
         + " " + str(df["time"][d]) for d in range(len(df))]
thefile = open('output/chronograf.txt', 'w')
for item in lines:
    thefile.write("%s\n" % item)
    """
