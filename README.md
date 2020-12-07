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

# Infraestructura Terraform

A continuación se describe de manera generar los modulos incluidos en el archivo `main.tf`, encargado de levantar una replica de la infraestructura utilizada en el proyecto semestral.

A partir de este diagrama de componentes adjunto, se incluyen los siguientes modulos de infraestructura:

## Security Group

El *Security Group* contiene diferentes componentes relevantes, que son descritos a continuación

### Oauth Server

Se incluye el servidor encargado de la autenticación en la aplicación, con la siguiente configuración

| Puerto | Protocolo | CIDR BLOCKS |
| ------ | --------- | ----------- |
| 443    | TCP       | 0.0.0.0/0   |
| 80     | TCP       | 0.0.0.0/0   |
| 22     | TCP       | 0.0.0.0/0   |
| 8000   | TCP       | 0.0.0.0/0   |
| 8001   | TCP       | 0.0.0.0/0   |

### Admin Server

Se incluye el servidor dedicado para los administradores de la plataforma, con la siguiente configuración

| Puerto    | Protocolo | CIDR BLOCKS     |
| --------- | --------- | --------------- |
| 443       | TCP       | 0.0.0.0/0, ::/0 |
| 80        | TCP       | 0.0.0.0/0, ::/0 |
| 22        | TCP       | 0.0.0.0/0, ::/0 |
| 8000:9000 | TCP       | 0.0.0.0/0, ::/0 |

## Database

Se incluye una configuración de la base de datos, con las siguientes caracteristicas

| Key                  | Value                            |
| -------------------- | -------------------------------- |
| Storage              | 20                               |
| Storage type         | ssd                              |
| Engine               | Postgres                         |
| Instance Class       | db.t2.micro                      |
| Name                 | mydb                             |
| username             | postgres                         |
| parameter_group_name | default.postgres12               |
| db_subnet_group_name | aws_db_subnet_group.default.name |

## Subnet Group

Se define un *subnet group* que contiene 6 *subnets*.

## Key Pair

Se incluye la referencia a las llaves publicas para realizar acciones, pero se incluye comentada para que cada usuario reemplace esto con su propio PATH

~~~yaml
public_key = ${file("/root/.ssh/id_rsa_pub")}
~~~

## Launch Template

Con el objetivo de definir el comportamiento correcto del *Autoscaling group*, se incluye una referencia en el archivo que indica los siguientes atributos

| Key           | Value                 |
| ------------- | --------------------- |
| name_prefix   | testing (modificable) |
| image_id      | ami-id                |
| instance_type | t2.micro              |

## Autoscaling Group

Se define el *autoscaling group* con los siguientes atributos

| Key                | Value                    |
| ------------------ | ------------------------ |
| availability zones | [us-east-1a, us-east-1c] |
| desired_capacity   | 2                        |
| max_size           | 3                        |
| min_size           | 1                        |

Aqui se incluye explicitamente la cantidad de instancias que se quieren manejar. Junto con esto, se incluye la relacion con el *launch_template* previamente definido.

~~~yaml
launch_template {
    id      = aws_launch_template.foobar.id
    version = "$Latest"
  }
~~~

## Instancias independientes

Dado que se cuenta con 2 instancias que no pertencen al autoscaling group, se declara de manera independiente

### Oauth Server

Definimos que este servidor encargado de la autenticacion no necesita escalar eventualmente, por lo que se declara de manera autonoma con la siguiente configuracion

| Key            | Value                                   |
| -------------- | --------------------------------------- |
| ami            | ami-id                                  |
| instance_type  | t2.micro                                |
| security_group | ["${aws_security_group.oauth-sg.name}"] |

### Admin Server

Definimos que este servidor, encargado de la plataforma para administradores, no necesita escalar eventualmente, por lo que se declara de manera autonoma con la siguiente configuracion

| Key            | Value                                   |
| -------------- | --------------------------------------- |
| ami            | ami-id                                  |
| instance_type  | t2.micro                                |
| security_group | ["${aws_security_group.admin-sg.name}"] |

## Elastic Load Balancer ELB

Se incluye un balanceador de carga que tiene puertos de entrada con la siguiente configuración

| Puerto | Protocolo | CIDR BLOCKS |
| ------ | --------- | ----------- |
| 443    | TCP       | 0.0.0.0/0   |
| 80     | TCP       | 0.0.0.0/0   |
| 6379   | TCP       | 0.0.0.0/0   |

Se declara el **id** del certificado utilizado para HTTPS en el puerto 443.

Tambien se incluye un *attachment* entre el *autoscaling group* y el *elb*.

## FrontEnd

Para la infraestructura del frontend, se utilizo un bucket S3 con un CDN Cloudfront, ambos se incluyeron en el archivo `main.tf`

El *bucket* requiere declara una politica en formato `.json`. Esta se incluyo con la siguiente declaracion:

~~~yaml
data "aws_iam_policy_document" "website_policy" {
  statement {
    actions = [
      "s3:GetObject"
    ]
    principals {
      identifiers = ["*"]
      type = "AWS"
    }
    resources = [
      "arn:aws:cloudfront::079534166449:distribution/E3L5LFQFHPYIDN"
    ]
  }
}
~~~

Para Cloudfront, se hizo un *attachment* al bucket S3 utilizado.





