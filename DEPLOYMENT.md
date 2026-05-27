# Guía de Despliegue - Huffman Compressor Pro

## Tabla de Contenidos

1. [Despliegue Local](#despliegue-local)
2. [Despliegue Docker](#despliegue-docker)
3. [Despliegue en Vercel (Frontend)](#despliegue-en-vercel-frontend)
4. [Despliegue en Heroku (Backend)](#despliegue-en-heroku-backend)
5. [Despliegue en AWS](#despliegue-en-aws)
6. [Despliegue en DigitalOcean](#despliegue-en-digitalocean)
7. [Configuración en Producción](#configuración-en-producción)

## Despliegue Local

### Requisitos
- Python 3.11+
- Node.js 18+
- npm o pnpm

### Pasos

```bash
# 1. Clonar repositorio
git clone https://github.com/usuario/huffman-compressor-pro.git
cd huffman-compressor-pro

# 2. Ejecutar setup
# Windows
setup.bat

# Linux/Mac
bash setup.sh

# 3. En Terminal 1: Backend
cd backend
source venv/bin/activate  # venv\Scripts\activate.bat en Windows
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. En Terminal 2: Frontend
cd frontend
npm run dev

# 5. Acceder
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

## Despliegue Docker

### Requisitos
- Docker 20.10+
- Docker Compose 2.0+

### Pasos

```bash
# 1. Clonar repositorio
git clone https://github.com/usuario/huffman-compressor-pro.git
cd huffman-compressor-pro

# 2. Crear archivo .env
cp .env.example .env
# Editar .env si es necesario

# 3. Construir e iniciar
docker-compose up --build

# 4. Acceder
# Frontend: http://localhost:3000
# API: http://localhost:8000

# 5. Detener
docker-compose down

# Limpiar volúmenes
docker-compose down -v
```

### Logs

```bash
# Ver logs
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

## Despliegue en Vercel (Frontend)

### Requisitos
- Cuenta en [Vercel](https://vercel.com)
- Repositorio en GitHub

### Pasos

1. **Conectar Repositorio**
   - Ir a https://vercel.com/new
   - Seleccionar repositorio GitHub
   - Vercel detectará automáticamente Next.js

2. **Configurar Variables de Entorno**
   ```
   NEXT_PUBLIC_API_URL=https://tu-backend-api.com
   ```

3. **Desplegar**
   - Vercel despliega automáticamente en cada push a main
   - URL: `https://tu-proyecto.vercel.app`

4. **Dominio Personalizado** (Opcional)
   - En Project Settings > Domains
   - Agregar dominio y configurar DNS

## Despliegue en Heroku (Backend)

### Requisitos
- Cuenta en [Heroku](https://www.heroku.com)
- Heroku CLI instalado

### Pasos

```bash
# 1. Login en Heroku
heroku login

# 2. Crear aplicación
heroku create huffman-compressor-api

# 3. Crear archivo Procfile en raíz del backend
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > backend/Procfile

# 4. Crear archivo runtime.txt
echo "python-3.11.0" > backend/runtime.txt

# 5. Desplegar
git push heroku main

# 6. Verificar logs
heroku logs --tail

# 7. Obtener URL
heroku apps:info
# URL será: https://huffman-compressor-api.herokuapp.com
```

### Configuración de Variables en Heroku

```bash
heroku config:set BACKEND_DEBUG=False
heroku config:set CORS_ORIGINS=["https://tu-frontend.vercel.app"]
```

## Despliegue en AWS

### Opción 1: EC2

```bash
# 1. Conectar a instancia EC2
ssh -i tu-key.pem ec2-user@tu-ip

# 2. Instalar dependencias
sudo yum update -y
sudo yum install python3.11 nodejs npm git -y

# 3. Clonar y configurar
git clone https://github.com/usuario/huffman-compressor-pro.git
cd huffman-compressor-pro

# 4. Backend con systemd
sudo tee /etc/systemd/system/huffman-backend.service > /dev/null <<EOF
[Unit]
Description=Huffman Compressor Backend
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/huffman-compressor-pro/backend
ExecStart=/home/ec2-user/huffman-compressor-pro/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 5. Iniciar servicio
sudo systemctl start huffman-backend
sudo systemctl enable huffman-backend

# 6. Verificar
sudo systemctl status huffman-backend
```

### Opción 2: Elastic Beanstalk

```bash
# 1. Instalar EB CLI
pip install awsebcli

# 2. Inicializar
eb init -p python-3.11 huffman-backend

# 3. Crear entorno
eb create huffman-production

# 4. Desplegar
eb deploy

# 5. Ver logs
eb logs

# 6. Abrir en navegador
eb open
```

## Despliegue en DigitalOcean

### Opción 1: App Platform

1. Conectar repositorio GitHub
2. Seleccionar rama `main`
3. Configurar Build & Run:
   - Backend: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Frontend: `npm run build && npm start`
4. Agregar variables de entorno
5. Desplegar

### Opción 2: Droplet + Docker

```bash
# 1. Crear droplet con Docker preinstalado

# 2. Conectar
ssh root@tu-ip

# 3. Clonar repositorio
git clone https://github.com/usuario/huffman-compressor-pro.git
cd huffman-compressor-pro

# 4. Crear archivo .env
nano .env

# 5. Desplegar con Docker Compose
docker-compose up -d

# 6. Verificar
docker-compose ps

# 7. Configurar Nginx (reverso proxy)
# Ver nginx.conf en raíz del proyecto
```

## Configuración en Producción

### Variables de Entorno

```bash
# .env.production
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://api.tu-dominio.com

BACKEND_DEBUG=False
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=["https://tu-dominio.com"]
```

### Seguridad

1. **HTTPS/TLS**
   ```bash
   # Con Certbot
   sudo certbot certonly --standalone -d tu-dominio.com
   ```

2. **Rate Limiting**
   - Implementar con Redis en producción
   - Usar middleware en FastAPI

3. **Autenticación** (Futuro)
   - JWT para sesiones
   - OAuth2 para terceros

4. **CORS Restringido**
   ```python
   CORS_ORIGINS = ["https://tu-dominio.com"]
   ```

### Monitoreo

1. **Logs**
   - Usar CloudWatch (AWS), Stackdriver (GCP), etc.
   - Centralizar logs con ELK Stack

2. **Métricas**
   - CPU, memoria, latencia
   - Errores 4xx y 5xx
   - Tiempo de respuesta

3. **Alertas**
   - CPU > 80%
   - Errores > 1%
   - Downtime

### Base de Datos (Futuro)

Para guardar historial de compresiones:

```python
# PostgreSQL con SQLAlchemy
DATABASE_URL=postgresql://user:password@localhost/huffman
```

### Caché (Futuro)

Para optimizar compresiones repetidas:

```python
# Redis
REDIS_URL=redis://localhost:6379
```

## Solución de Problemas

### Backend no inicia
```bash
# Verificar puerto
lsof -i :8000
kill -9 <PID>

# Verificar dependencias
pip install -r requirements.txt
```

### Frontend no conecta con backend
```bash
# Verificar CORS
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     http://localhost:8000/api/health

# Verificar variable de entorno
echo $NEXT_PUBLIC_API_URL
```

### Problemas de memoria
```bash
# Monitorear uso
docker-compose stats

# Limitar recursos en docker-compose.yml
services:
  backend:
    mem_limit: 512m
```

## Checklist de Despliegue

- [ ] Clonar repositorio
- [ ] Crear archivo .env
- [ ] Instalar dependencias
- [ ] Ejecutar tests
- [ ] Compilar frontend
- [ ] Configurar dominio/DNS
- [ ] Habilitar HTTPS
- [ ] Verificar CORS
- [ ] Configurar rate limiting
- [ ] Configurar logging
- [ ] Hacer backup de base de datos
- [ ] Crear proceso de rollback
- [ ] Documentar proceso
- [ ] Monitorear después del despliegue

## Soporte

Para problemas de despliegue:
- 📧 Email: tu-email@example.com
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
