# Documentación de Cache

Para esta entrega se realizó el requisito variable de cache del servidor. Para esto, se usó una instancia EC2 separada de aws en el mismo VPC que el servidor. Esta instancia está corriendo redis. Las 3 instancias de EC2 que están corriendo el backend son servidas por la misma instancia EC2 de cache.

La configuración de cache es tipo FIFO. A medida que van llegando las request, el servidor revisa el cache, y en caso de no encontrarse la key, esta es pedida a la base de datos y cacheada, según orden de llegada. El cache está implementado como un hash table, donde la key es el id del obejto en la request y el value es su data.

Los datos cacheados son los boards y los mensajes. Los mensajes tienen un tiempo de cacheado de 30 segundos. Por otro lado, la restricción de tiempo de los boards son 30 minutos. Esta diferencia se debe a que la creación de boards es mucho menos frecuente que la creación de mensajes, por lo que mantener el cache de los boards por más tiempo es beneficioso para la request y menos costoso debido a que hay que realizar menos llamadas a la database.
