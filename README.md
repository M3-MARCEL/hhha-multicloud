----------------------------------------------------------------
MANUAL DE DESPLIEGUE — HHHA Multi Cloud
----------------------------------------------------------------

REQUISITOS PREVIOS
------------------
- Archivo hhha-key.pem
- Instancia EC2 "hhha-nube-computo" iniciada en la consola AWS
- IP pública actual (varía cada vez que se reinicia el laboratorio)

----------------------------------------------------------------
1. CONECTARSE AL SERVIDOR
----------------------------------------------------------------
Desde PowerShell:

ssh -i "C:\Users\marce\Desktop\Multi Cloud\hhha-key.pem" ubuntu@IP_PUBLICA

Si da error de conexión: ve a AWS → Security Groups →
hhha-sg-computo → Edit inbound rules → SSH → "My IP" → Save.

----------------------------------------------------------------
2. LEVANTAR LA APLICACIÓN
----------------------------------------------------------------
cd /home/ubuntu/hhha-app
docker-compose up -d

Verificar que los 3 contenedores estén corriendo:
docker ps

Resultado esperado:
- hhha-app_frontend_1   → 0.0.0.0:80
- hhha-app_backend_1    → (sin puertos públicos)
- hhha-app_db_1         → (healthy)

----------------------------------------------------------------
3. ACCEDER A LA APLICACIÓN
----------------------------------------------------------------
Abrir en el navegador:
http://IP_PUBLICA

----------------------------------------------------------------
4. DETENER LA APLICACIÓN
----------------------------------------------------------------
cd /home/ubuntu/hhha-app
docker-compose down

----------------------------------------------------------------
5. VER LOGS SI ALGO FALLA
----------------------------------------------------------------
docker logs hhha-app_backend_1
docker logs hhha-app_frontend_1

----------------------------------------------------------------
6. AZURE BLOB STORAGE
----------------------------------------------------------------
Portal: https://portal.azure.com
Storage Account: hhhastoragecloud
Containers: laboratorio | imagenologia
Región: Brazil South | Resource Group: hhha-rg

----------------------------------------------------------------
NOTAS IMPORTANTES
----------------------------------------------------------------
- La IP pública cambia cada vez que se reinicia el laboratorio AWS.
- Los archivos del proyecto están en /home/ubuntu/hhha-app/
- Los datos de PostgreSQL persisten aunque se detenga Docker.
- Las credenciales de Azure están en /home/ubuntu/hhha-app/.env
