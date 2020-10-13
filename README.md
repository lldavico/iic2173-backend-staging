# Gruponce App

## Nombre de Dominio

Se utilizó Name.com para generar el nombre de dominio. La página de app es [thechatproject.tk](http://www.thechatproject.tk) y el backend en [api-gruponce.tk](https://www.api-gruponce.tk/).

## Método de acceso al servidor

Para entrar al servidor se utilizó el método de ssh.
```
ssh -i /path/to/file.pem ubuntu@52.7.45.105
```
Se agregó el archivo.pem y comando exacto en el archivo.zip subido a canvas. 

## Requisitos logrados y no logrados

### Requisitos Mínimos
En esta entrega se cumplió con los requisitos mínimos. Más en detalle:

| Requisito | Cumplimiento |
| ---------: | -----------:|
| RF1 | Logrado :white_check_mark: |
| RF2 | Logrado :white_check_mark: |
| RF3  | Logrado :white_check_mark: |
| RF4  | Logrado :white_check_mark:|
| RF5  | Logrado :white_check_mark: |
| RF6  | Logrado :white_check_mark: |

Con respecto a los requisitos variables, se cumplió con los requisitos variables 1. Cache y 3. Trabajo delegado.
Más en detalle:

### Requisito Variable 1: Cache

| Requisito | Cumplimiento |
| ---------:| -----------:|
| RF1 | Logrado :white_check_mark: |
| RF2 | Logrado :white_check_mark: |
| RF3 | Logrado :white_check_mark: |

### Requisito Variable 2: Trabajo delegado

| Requisito | Cumplimiento |
| ---------:| -----------:|
| RF1 | Logrado :white_check_mark: |

Se logró hacer sentiment análisis en los mensajes de los usuarios a través de AWS Comprehend. Este fue considerado, según la indicación del enunciado, como requisito que cumple con todas las solicitudes de trabajo delegado.

## Tercer requisito variables

No se realizó el tercer requisito variable.


# Documentación de Cache

Para esta entrega se realizó el requisito variable de cache del servidor. Para esto, se usó una instancia EC2 separada de aws en el mismo VPC que el servidor. Esta instancia está corriendo redis. Las 3 instancias de EC2 que están corriendo el backend son servidas por la misma instancia EC2 de cache.

La configuración de cache es tipo FIFO. A medida que van llegando las request, el servidor revisa el cache, y en caso de no encontrarse la key, esta es pedida a la base de datos y cacheada, según orden de llegada. El cache está implementado como un hash table, donde la key es el id del obejto en la request y el value es su data.

Los datos cacheados son los boards y los mensajes. Los mensajes tienen un tiempo de cacheado de 30 segundos. Por otro lado, la restricción de tiempo de los boards son 30 minutos. Esta diferencia se debe a que la creación de boards es mucho menos frecuente que la creación de mensajes, por lo que mantener el cache de los boards por más tiempo es beneficioso para la request y menos costoso debido a que hay que realizar menos llamadas a la database.
