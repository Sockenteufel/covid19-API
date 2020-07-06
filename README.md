# Que es este repositorio
Este repo tiene el código necesario para tomar los productos publicados por el Ministerio de Ciencia 
en su [repositorio](https://github.com/MinCiencia/Datos-COVID19) y convertirlos en formato line, que es el nativo de 
[InfluxDB](https://www.influxdata.com/), para ofrecer una API y un dashboard para explorar los datos
y/o construir soluciones.


## Donde están los recursos?

Puedes acceder al dashboard [aca](http://covid19.dataobservatory.net/grafana). Corresponde a una 
instancia de [grafana](https://grafana.com/), que permite visualizar los datos.

Si necesitas hacer consultas mas avanzadas, puedes usar la API que expone influx [acá](http://covid19.dataobservatory.net:85)

Se requiere autenticacion para extraer datos, `anonymous:anonymous` sirve.

Cada uno de los productos estandard ofrecidos por el MinCiencia corresponden a una serie 

Algunos ejemplos:

Para ver las series disponibles:

`curl -u anonymous:anonymous 'http://covid19.dataobservatory.net:85/query?db=covid19' --data-urlencode "q=show series"
`

Para obtener los datos de las camas:

`curl -u anonymous:anonymous 'http://covid19.dataobservatory.net:85/query?db=covid19' --data-urlencode "q=SELECT "Total" FROM "autogen"."Camas_hospital" "`


## Como funciona?
Cada vez que se actualiza un producto en el repo del [MinCiencia](https://github.com/MinCiencia/Datos-COVID19)
se gatilla un [github action](https://github.com/features/actions) que nos notifica mediante un dispatch, 
gatillando a su vez un github action acá que genera los archivos para influx. Cada 30 minutos,
la base de datos ingesta las nuevas series.

## Que representa cada serie de tiempo?

La asociación entre productos y series es:

* [producto 1](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19_std.csv) Casos_confirmados_comunal:
    * [Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST(*)%20FROM%20%22Casos_confirmados_comunal%22)
    * [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_acumulados_regional%22)
    * [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_acumulados_regional%22)
* [producto 2](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto6/bulk/data.csv) Tasa_de_incidencia:
    * [Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST(*)%20FROM%20%22Tasa_de_incidencia%22)
    * [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Tasa_de_incidencia%22)
    * [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Tasa_de_incidencia%22)
* [producto 3](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo_std.csv) Casos_acumulados_regional:
    * [Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST(*)%20FROM%20%22Casos_acumulados_regional%22)
    * [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_acumulados_regional%22)
    * [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_acumulados_regional%22)
* [producto 4](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto11/bulk/producto4.csv)
    * Pendiente
* [producto 5](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales_std.csv) Totales_nacionales:
    * [Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST(*)%20FROM%20%22Totales_nacionales%22)
    * [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Totales_nacionales%22)
    * [Tag values](http://covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Totales_nacionales%22%20WITH%20KEY=%22Serie%22)
    * [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Totales_nacionales%22)
* producto 6 Corresponde al std del producto 2
* [producto 7](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto7/PCR_std.csv) PCR_Regional:
    * [Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST(*)%20FROM%20%22PCR_Regional%22)
    * [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22PCR_Regional%22)
    * [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22PCR_Regional%22)
* [producto 8](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto8/UCI_std.csv) UCI_Regional:
    * [Ultimo registro]
    * [Tag keys]
    * [Field keys]
* [producto 9](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto9/HospitalizadosUCIEtario_std.csv) UCI_Etario
    * [Ultimo registro]
    * [Tag keys]
    * [Field keys]
* [producto 10](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario_std.csv) Fallecidos_Etario
    * [Ultimo registro]
    * [Tag keys]
    * [Field keys]
* [producto 13](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto13/CasosNuevosCumulativo_std.csv) Casos_nuevos_cumulativo_regional
* [producto 14](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo_std.csv) Fallecidos_cumulativo_regional
* [producto 15](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/FechaInicioSintomasHistorico_std.csv) Inicio_sintomas_comunal
* [producto 16](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto16/CasosGeneroEtario_std.csv) Casos_genero_Etario
* [producto 17](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto17/PCREstablecimiento_std.csv) PCR_tipo_establecimiento
* [producto 18](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto18/TasaDeIncidencia_std.csv) Tasa_de_incidencia_comunal
* [producto 19](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna_std.csv) Casos_activos_comunal
* [producto 20](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto20/NumeroVentiladores_std.csv) Ventiladores_nacional
* [producto 21_1](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto21/SintomasCasosConfirmados_std.csv) Sintomas_casos_confirmados
* [producto 21_2](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto21/SintomasHospitalizados_std.csv) Sintomas_hospitalizados
* [producto 22_1](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto22/HospitalizadosEtario_Acumulado_std.csv) Hospitalizados_etario
* [producto 22_2](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto22/HospitalizadosUCI_Acumulado_std.csv) Hospitalizados_UCI_etario
* [producto 23](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto23/PacientesCriticos_std.csv) Pacientes_criticos
* [producto 24](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto24/CamasHospital_Diario_std.csv) Camas_hospital
* [producto 25](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto25/CasosActualesPorComuna_std.csv) Casos_actuales_comunal
* [producto 28](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto28/FechaInicioSintomas_reportadosSEREMIHistorico_std.csv) Inicio_sintomas_reportados
* [producto 30](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto30/PacientesVMI_std.csv) Pacientes_VMI
* [producto 31](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto31/Nacimientos_std.csv) Nacimientos_comunal
* [producto 32](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto32/Defunciones_std.csv) Defunciones_comunal
* [producto 33](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto33/IndiceDeMovilidad_std.csv) Indice_de_Movilidad
* [producto 35](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto35/Comorbilidad_std.csv) Comorbilidad
* [producto 36](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto36/ResidenciasSanitarias_std.csv) Residencias_sanitarias
* [producto 37](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto37/Defunciones_std.csv) Defunciones_nueva_definicion
* [producto 38](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto38/CasosFallecidosPorComuna_std.csv) Defunciones_comunales
* [producto 39](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto39/NotificacionInicioSintomas_std.csv) Notificacion_inicio_sintomas
* [producto 40](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto40/TransporteAereo_std.csv) Transporte_aereo
* [producto 41_1](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto41/BIPTotal_std.csv) BIP_total
* [producto 41_2](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto41/BIPComuna_std.csv) BIP_comunal
* [producto 42](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto42/ViajesComunas_std.csv) Viajes_comunas
* [producto 43](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto43/ViajesComunas_std.csv) Datos del Ministario del Medio Ambiente, una serie para cada contaminante:
   1. CO
   2. MP10
   3. MP2.5
   4. NO2
   5. O3
   6. SO2
