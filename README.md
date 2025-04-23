Esta aplicación es un sistema de monitoreo IP que está programada para monitorear todos los puertos que se conectan mediante una dirección IP. Siempre y cuando sea capaz de dar y recibir paquetes Y Este conectada a la misma red podrás ser monitoreada. 

 DB.

 Crear la Db como se ve en el archivo sql del repositorio. En esta DB las contraseñas se encuentran encriptadas para mayor seguridad.

Roles.
- Antes de iniciar la app primero tienes que crear un usuario con el Rol DM en la db, esto porque la app solo permitira poder completar el registro a aquellos usuarios que hayan sido aprobados por un DM o un Admin
  
- La aplicacion cuenta con un Login y un registro para registrar usuarios dependiendo de sus roles, asi cada usuario tendra ciertas restricciones, dependiendo de su rol
- ![image](https://github.com/user-attachments/assets/615486d6-6559-46f2-9bf1-44e6dd65fdd9)

- ![image](https://github.com/user-attachments/assets/93f0f90e-d2f0-4410-93b9-bcf5ddec7dc1)


 
- La aplicación está formada por 3 Roles que son viewer, administrador y DM los Viewers son capaces de ver en la base de datos y Todas las IPS que están conectados más no pueden interactuar con nada más. Los admin pueden. Ver las bases de datos pueden aceptar o denegar a los usuarios, pueden realizar casi todas las funciones excepto la aplicación ofrece. Y luego está la usted me que es exclusivo para Aquellos usuarios que tengan el acceso completo, la diferencia es que los DM me pueden eliminar y degradar a otros usuarios. Y los DM son los únicos que pueden recibir los mensajes de restricción de la base de datos y son capaces de poder degradar a otros DM. Y de interactuar full con la base de datos.

- Solo los admins y los DM pueden acceder a ciertas partes de la aplicacion, Los Viewers no podran pasar del area de monitoreo.

- Para poder mejorar la seguridad de la app se debe crear una variable de entorno y codificar el nombre de esta en el programa, esto para que aquellos roles con el rango de admin y DM sean capaces de poder editar y eliminar usuarios de la App

* Alerta

  - La app cuenta con un sistema de alerta en caso de que una IP haya caido repentinamente, este le mandara un correo electronico a todos los DM registrados informandoles el status de la ip y la hora en la que cayo



* Area de Monitoreo y administracion

  - Las Ips se dividen mediente 2 lineas  que mostraran si estan activas o si no, estas lineas mostraran las primeras 6 Ips programadas aunque tiene la capacidad de poder ampliarse, posee un buscador por el cual podremos buscar la IP que deseamos en caso de tener muchas mediante ya sea el nombre que le pongamos o el ID de la DB
    ![image](https://github.com/user-attachments/assets/44ee311d-2141-40e6-92bf-910af8ad174e)


- La aplicación cuenta con varias pestañas, como es el administrador de usuarios, que es donde se puede verificar todos los usuarios conectados, los correos electrónicos, etcétera. El estado de las IPS, que es donde se puede ver todas las IPS conectadas que estén activas o caídas, además de que esta es la única parte en las que los bebés pueden estar. y por Aprobación de usuario, que es la parte en la que se aprueban los usuarios que tengan que ingresar. Cada usuario que quiera ingresar a la base de datos tiene que iniciar sesión y tiene que esperar a que un admin o un DM lo apruebe.  

- Los usuarios una vez ingresados apareceran en el area de administracion en la cual se podra ver su nombre, correo electronico y Rol, solo los DM pueden editar los roles de los usuarios de su mismo rol, los demas pueden ser editados por los Admins ademas para poder eliminar un usuario tendras que ingresar tu contraseña y la de una variable de entorno. 
![image](https://github.com/user-attachments/assets/a4fad7d4-371c-42bf-9174-b19fef19b5e3)

Para ejecutar la aplicación, colocar en un archivo, todos los documentos puestos, Importar todas las librerias que se le pide y ejecutar el archivo App 

