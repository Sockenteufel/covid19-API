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
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Casos_confirmados")%20FROM%20%22Casos_confirmados_comunal%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_confirmados_comunal%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_confirmados_comunal%22)

* [producto 2](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto6/bulk/data.csv) Tasa_de_incidencia:
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Tasa")%20FROM%20%22Tasa_de_incidencia%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Tasa_de_incidencia%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Tasa_de_incidencia%22)

* [producto 3](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo_std.csv) Casos_acumulados_regional:
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Casos_acumulados")%20FROM%20%22Casos_acumulados_regional%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_acumulados_regional%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_acumulados_regional%22)

* [producto 4](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto11/bulk/producto4.csv)
Pendiente

* [producto 5](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales_std.csv) Totales_nacionales:
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Totales_nacionales%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Totales_nacionales%22)
, [Tag values "Serie"](http://covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Totales_nacionales%22%20WITH%20KEY=%22Serie%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Totales_nacionales%22)

* producto 6: Corresponde al  producto _std del producto 2

* [producto 7](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto7/PCR_std.csv) PCR_Regional:
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22PCR_Regional%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22PCR_Regional%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22PCR_Regional%22)

* [producto 8](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto8/UCI_std.csv) UCI_Regional:
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22UCI_Regional%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22UCI_Regional%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22UCI_Regional%22)

* [producto 9](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto9/HospitalizadosUCIEtario_std.csv) UCI_Etario
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22UCI_Etario%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22UCI_Etario%22)
, [Tag values "Grupo_de_edad"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22UCI_Etario%22%20WITH%20KEY=%22Grupo_de_edad%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22UCI_Etario%22)

* [producto 10](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario_std.csv) Fallecidos_Etario
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Fallecidos_Etario%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Fallecidos_Etario%22)
, [Tag values "Grupo_de_edad"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Fallecidos_Etario%22%20WITH%20KEY=%22Grupo_de_edad%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Fallecidos_Etario%22)

* producto 11: Corresponde al  producto _std del producto 4

* producto 12: Corresponde al  producto _std del producto 7

* [producto 13](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto13/CasosNuevosCumulativo_std.csv) Casos_nuevos_cumulativo_regional
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Casos_nuevos_cumulativo_regional%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_nuevos_cumulativo_regional%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_nuevos_cumulativo_regional%22)

* [producto 14](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo_std.csv) Fallecidos_cumulativo_regional
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Fallecidos_cumulativo_regional%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Fallecidos_cumulativo_regional%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Fallecidos_cumulativo_regional%22)

* [producto 15](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/FechaInicioSintomasHistorico_std.csv) Inicio_sintomas_comunal
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Casos_confirmados")%20FROM%20%22Inicio_sintomas_comunal%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Inicio_sintomas_comunal%22)
, [Tag values "Publicacion"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Inicio_sintomas_comunal%22%20WITH%20KEY=%22Publicacion%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Inicio_sintomas_comunal%22)

* [producto 16](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto16/CasosGeneroEtario_std.csv) Casos_genero_Etario
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Casos_genero_Etario%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_genero_Etario%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_genero_Etario%22)

* [producto 17](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto17/PCREstablecimiento_std.csv) PCR_tipo_establecimiento
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22PCR_tipo_establecimiento%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22PCR_tipo_establecimiento%22)
, [Tag values "Establecimiento"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22PCR_tipo_establecimiento%22%20WITH%20KEY=%22Establecimiento%22)
, [Tag values "Examenes"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22PCR_tipo_establecimiento%22%20WITH%20KEY=%22Examenes%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22PCR_tipo_establecimiento%22)

* [producto 18](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto18/TasaDeIncidencia_std.csv) Tasa_de_incidencia_comunal
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Tasa_de_incidencia")%20FROM%20%22Tasa_de_incidencia_comunal%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Tasa_de_incidencia_comunal%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Tasa_de_incidencia_comunal%22)

* [producto 19](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna_std.csv) Casos_activos_comunal
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Casos_activos")%20FROM%20%22Casos_activos_comunal%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_activos_comunal%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_activos_comunal%22)
    
* [producto 20](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto20/NumeroVentiladores_std.csv) Ventiladores_nacional
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Ventiladores_nacional%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Ventiladores_nacional%22)  
, [Tag values](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Ventiladores_nacional%22%20WITH%20KEY=%22Ventiladores%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Ventiladores_nacional%22)

* [producto 21_1](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto21/SintomasCasosConfirmados_std.csv) Sintomas_casos_confirmados
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Sintomas_casos_confirmados%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Sintomas_casos_confirmados%22)  
, [Tag values "Sintomas"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Sintomas_casos_confirmados%22%20WITH%20KEY=%22Sintomas%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Sintomas_casos_confirmados%22)
    
* [producto 21_2](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto21/SintomasHospitalizados_std.csv) Sintomas_hospitalizados
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Sintomas_hospitalizados%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Sintomas_hospitalizados%22)  
, [Tag values "Sintomas"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Sintomas_hospitalizados%22%20WITH%20KEY=%22Sintomas%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Sintomas_hospitalizados%22)
    
* [producto 22_1](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto22/HospitalizadosEtario_Acumulado_std.csv) Hospitalizados_etario
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Hospitalizados_etario%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Hospitalizados_etario%22)  
, [Tag values "Grupo_de_edad"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Hospitalizados_etario%22%20WITH%20KEY=%22Grupo_de_edad%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Hospitalizados_etario%22)
    
* [producto 22_2](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto22/HospitalizadosUCI_Acumulado_std.csv) Hospitalizados_UCI_etario
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Hospitalizados_UCI_etario%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Hospitalizados_UCI_etario%22)  
, [Tag values "Grupo_de_edad"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Hospitalizados_UCI_etario%22%20WITH%20KEY=%22Grupo_de_edad%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Hospitalizados_UCI_etario%22)

* [producto 23](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto23/PacientesCriticos_std.csv) Pacientes_criticos
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Pacientes_criticos%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Pacientes_criticos%22)
    
* [producto 24](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto24/CamasHospital_Diario_std.csv) Camas_hospital
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Camas_hospital%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Camas_hospital%22)  
, [Tag values "Tipo_de_cama"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Camas_hospital%22%20WITH%20KEY=%22Tipo_de_cama%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Camas_hospital%22)
    
* [producto 25](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto25/CasosActualesPorComuna_std.csv) Casos_actuales_comunal
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Casos_actuales")%20FROM%20%22Casos_actuales_comunal%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_actuales_comunal%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_actuales_comunal%22)

* [producto 26](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto26/CasosNuevosConSintomas_std.csv) Casos_nuevos_con_sintomas_regional
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Casos")%20FROM%20%22Casos_nuevos_con_sintomas_regional%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_nuevos_con_sintomas_regional%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_nuevos_con_sintomas_regional%22)
 
* [producto 27](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto26/CasosNuevosSinSintomas_std.csv) Casos_nuevos_sin_sintomas_regional
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Casos")%20FROM%20%22Casos_nuevos_sin_sintomas_regional%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_nuevos_sin_sintomas_regional%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_nuevos_sin_sintomas_regional%22)
     

* [producto 28](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto28/FechaInicioSintomas_reportadosSEREMIHistorico_std.csv) Inicio_sintomas_reportados
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Casos_confirmados")%20FROM%20%22Inicio_sintomas_reportados%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Inicio_sintomas_reportados%22)  
, [Tag values "Publicacion"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Inicio_sintomas_reportados%22%20WITH%20KEY=%22Publicacion%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Inicio_sintomas_reportados%22)

* producto 29: Corresponde a un geojson

* [producto 30](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto30/PacientesVMI_std.csv) Pacientes_VMI
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Pacientes_VMI%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Pacientes_VMI%22)
    
* [producto 31](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto31/Nacimientos_std.csv) Nacimientos_comunal
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Nacimientos")%20FROM%20%22Nacimientos_comunal%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Nacimientos_comunal%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Nacimientos_comunal%22)

* [producto 32](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto32/Defunciones_std.csv) Defunciones_comunal
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Defunciones")%20FROM%20%22Defunciones_comunal%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Defunciones_comunal%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Defunciones_comunal%22)

* [producto 33](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto33/IndiceDeMovilidad_std.csv) Indice_de_movilidad
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Indice")%20FROM%20%22Indice_de_movilidad%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Indice_de_movilidad%22)  
, [Tag values "Serie"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Indice_de_movilidad%22%20WITH%20KEY=%22Serie%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Indice_de_movilidad%22)

* producto 34: Corresponde a un geojson

* [producto 35](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto35/Comorbilidad_std.csv) Comorbilidad
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Comorbilidad%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Comorbilidad%22)  
, [Tag values "Comorbilidad"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Comorbilidad%22%20WITH%20KEY=%22Comorbilidad%22)
, [Tag values "Hospitalizacion"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Comorbilidad%22%20WITH%20KEY=%22Hospitalizacion%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Comorbilidad%22)
    
* [producto 36](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto36/ResidenciasSanitarias_std.csv) Residencias_sanitarias
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Residencias_sanitarias%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Residencias_sanitarias%22)  
, [Tag values "Categoria"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Residencias_sanitarias%22%20WITH%20KEY=%22Categoria%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Residencias_sanitarias%22)
    
* [producto 37](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto37/Defunciones_std.csv) Defunciones_nueva_definicion
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Defunciones_nueva_definicion%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Defunciones_nueva_definicion%22)  
, [Tag values "Publicacion"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Defunciones_nueva_definicion%22%20WITH%20KEY=%22Publicacion%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Defunciones_nueva_definicion%22)
    
* [producto 38](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto38/CasosFallecidosPorComuna_std.csv) Defunciones_comunales
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Defunciones_comunales%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Defunciones_comunales%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Defunciones_comunales%22)
    
* [producto 39](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto39/NotificacionInicioSintomas_std.csv) Notificacion_inicio_sintomas
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Notificacion_inicio_sintomas%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Notificacion_inicio_sintomas%22)  
, [Tag values "Serie"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Notificacion_inicio_sintomas%22%20WITH%20KEY=%22Serie%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Notificacion_inicio_sintomas%22)
    
* [producto 40](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto40/TransporteAereo_std.csv) Transporte_aereo
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Pasajeros")%20FROM%20%22Transporte_aereo%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Transporte_aereo%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Transporte_aereo%22)
    
* [producto 41_1](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto41/BIPTotal_std.csv) BIP_total
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Transacciones")%20FROM%20%22BIP_total%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22BIP_total%22)
    
* [producto 41_2](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto41/BIPComuna_std.csv) BIP_comunal
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Transacciones")%20FROM%20%22BIP_comunal%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22BIP_comunal%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22BIP_comunal%22)
    
* [producto 42](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto42/ViajesComunas_std.csv) Viajes_comunas
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Viajes")%20FROM%20%22Viajes_comunas%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Viajes_comunas%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Viajes_comunas%22)
    
* [producto 43](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto43) Datos del Ministario del Medio Ambiente, una serie para cada contaminante:
    1. CO:
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Medicion")%20FROM%20%22CO%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22CO%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22CO%22)
    2. MP10:
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Medicion")%20FROM%20%22MP10%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22MP10%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22MP10%22)   
    3. MP2.5:
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Medicion")%20FROM%20%22MP2.5%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22MP2.5%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22MP2.5%22) 
    4. NO2:
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Medicion")%20FROM%20%22NO2%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22NO2%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22NO2%22)    
    5. O3:
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Medicion")%20FROM%20%22O3%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22O3%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22O3%22)    
    6. SO2:
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Medicion")%20FROM%20%22SO2%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22SO2%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22SO2%22)
            
* [producto 44](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto44/EgresosHospitalarios_std.csv) Egresos_semanales
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Egresos")%20FROM%20%22Egresos_semanales%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Egresos_semanales%22)  
, [Tag values "Publicacion"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Egresos_semanales%22%20WITH%20KEY=%22Publicacion%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Egresos_semanales%22)
    
* [producto45_1](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto45/CasosConfirmadosPorComuna_std.csv) Casos_confirmados_comunal_FIS
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Casos_confirmados")%20FROM%20%22Casos_confirmados_comunal_FIS%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_confirmados_comunal_FIS%22)  
, [Tag values "Publicacion"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Casos_confirmados_comunal_FIS%22%20WITH%20KEY=%22Publicacion%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_confirmados_comunal_FIS%22)
   
* [producto45_2](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto45/CasosNoNotificadosPorComunaHistorico_std.csv) Casos_no_notificados_comunal_FIS
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Casos_confirmados")%20FROM%20%22Casos_no_notificados_comunal_FIS%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_no_notificados_comunal_FIS%22)  
, [Tag values "Publicacion"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Casos_no_notificados_comunal_FIS%22%20WITH%20KEY=%22Publicacion%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_no_notificados_comunal_FIS%22)
   
* [producto45_3](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto45/CasosProbablesPorComuna_std.csv) Casos_probables_comunal_FIS
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Casos_confirmados")%20FROM%20%22Casos_probables_comunal_FIS%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Casos_probables_comunal_FIS%22)  
, [Tag values "Publicacion"](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20VALUES%20FROM%20%22Casos_probables_comunal_FIS%22%20WITH%20KEY=%22Publicacion%22)
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Casos_probables_comunal_FIS%22)

* [producto46](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto46/activos_vs_recuperados_std.csv) Activos_vs_recuperados
[Ultimo registro](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SELECT%20LAST("Total")%20FROM%20%22Activos_vs_recuperados%22)
, [Tag keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20TAG%20KEYS%20FROM%20%22Activos_vs_recuperados%22)  
, [Field keys](http://anonymous:anonymous@covid19.dataobservatory.net:85/query?db=covid19&q=SHOW%20FIELD%20KEYS%20FROM%20%22Activos_vs_recuperados%22)


![Actualiza_productos_para influxdb](https://github.com/Data-Observatory/covid19-API/workflows/Actualiza_productos_para%20influxdb/badge.svg)