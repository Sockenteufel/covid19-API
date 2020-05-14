# Que es este repositorio
Este repo tiene el código necesario para tomar los productos publicados por el Ministerio de Ciencia 
en su [repositorio](https://github.com/MinCiencia/Datos-COVID19) en formato line, que es el nativo de 
[InfluxDB](https://www.influxdata.com/), para ofrecer una API y un dashboard para explorar los datos
y/o construir soluciones.


## Donde está?

Puedes acceder al dashboard [aca](http://covid19.dataobservatory.net/grafana). Corresponde a una 
instancia de [grafana](https://grafana.com/), que permite explorar los datos.

Si necesitas hacer consultas mas avanzadas, puedes usar la API que expone influx [acá](http://covid19.dataobservatory.net:85)

Se requiere autenticacion para extraer datos, `anonymous:anonymous` sirve.

Cada uno de los productos estandard ofrecidos por el MinCiencia corresponden a una serie 

Algunos ejemplos:

Para ver las series disponibles:

`curl -u anonymous:anonymous 'http://covid19.dataobservatory.net:85/query?db=covid19' --data-urlencode "q=show series"
`

Para obtener los datos de las camas:

`curl -u anonymous:anonymous 'http://covid19.dataobservatory.net:85/query?db=covid19' --data-urlencode "q=SELECT "Total" FROM "autogen"."Camas_hospital" "`