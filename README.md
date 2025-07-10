# DevOps Microservicio - Banco Pichincha Assessment

## Descripción
Este proyecto es un microservicio desarrollado en FastAPI para el assessment técnico de DevOps. Expone un endpoint `/DevOps` protegido por API Key y JWT, cumple con buenas prácticas de CI/CD, testing, contenerización, escalabilidad y gestión de APIs.

---

## Requisitos
- Docker y Docker Compose
- Python 3.11+
- (Opcional) Kubernetes (minikube, kind, GKE, EKS, etc.)
- (Opcional) GitHub Actions (para CI/CD)

---

## Uso local
1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el microservicio:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Prueba el endpoint:
   ```bash
   curl -X POST \
     -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" \
     -H "Content-Type: application/json" \
     -d '{"message":"This is a test","to":"Juan Perez","from":"Rita Asturia","timeToLifeSec":45}' \
     http://localhost:8000/DevOps
   ```

---

## Uso con Docker
1. Construye la imagen:
   ```bash
   docker build -t devops-microservice:latest .
   ```
2. Levanta el servicio:
   ```bash
   docker-compose up --scale app=2
   ```
3. Accede en: `http://localhost:8002/DevOps`

---

## Uso con Kubernetes
1. Sube la imagen a Docker Hub (o usa la que sube el pipeline):
   ```bash
   docker tag devops-microservice:latest <usuario_dockerhub>/devops-microservice:latest
   docker push <usuario_dockerhub>/devops-microservice:latest
   ```
2. Edita `k8s/deployment.yaml` para usar tu imagen de Docker Hub.
3. Aplica los manifiestos:
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```
4. Accede en: `http://<IP-del-nodo>:30080/DevOps`

---

## Pipeline CI/CD (GitHub Actions)
- El pipeline instala dependencias, ejecuta flake8, corre los tests y construye la imagen Docker.
- Cuando haces push a `main`, la imagen se sube automáticamente a Docker Hub con los tags `latest` y el SHA del commit.
- Configura los secretos `DOCKERHUB_USERNAME` y `DOCKERHUB_TOKEN` en tu repositorio de GitHub.

---

## API Manager con Kong
1. Levanta Kong y su base de datos con Docker Compose:
   ```bash
   docker-compose up -d kong-database
   docker-compose run --rm kong kong migrations bootstrap
   docker-compose up -d kong
   ```
2. Registra tu microservicio en Kong (ejemplo usando curl):
   ```bash
   # Crea el servicio
   curl -i -X POST --url http://localhost:8001/services/ \
     --data 'name=devops' \
     --data 'url=http://app:8000/DevOps'

   # Crea la ruta
   curl -i -X POST --url http://localhost:8001/services/devops/routes \
     --data 'paths[]=/DevOps'

   # Activa el plugin de API Key
   curl -i -X POST --url http://localhost:8001/services/devops/plugins \
     --data 'name=key-auth'

   # Crea un consumidor y una API Key
   curl -i -X POST --url http://localhost:8001/consumers/ \
     --data 'username=juanperez'
   curl -i -X POST --url http://localhost:8001/consumers/juanperez/key-auth
   ```
3. Usa la API Key generada en el header `apikey` para acceder al endpoint a través de Kong:
   ```bash
   curl -X POST \
     -H "apikey: <API_KEY_GENERADA>" \
     -H "Content-Type: application/json" \
     -d '{"message":"This is a test","to":"Juan Perez","from":"Rita Asturia","timeToLifeSec":45}' \
     http://localhost:8000/DevOps
   ```

---

## Despliegue automático
- El pipeline sube la imagen a Docker Hub automáticamente en cada push a `main`.
- Puedes usar la imagen en tu clúster Kubernetes o en cualquier servidor con Docker Compose.

---

## Testing y calidad
- Ejecuta los tests con:
  ```bash
  pytest
  ```
- Revisión estática con:
  ```bash
  flake8 app tests
  ```

---

## Contacto
Cualquier duda o consulta, contacta a: [Tu Nombre] <kevinarmashbk232@gmail.com> 

---

## Despliegue en AWS con Kubernetes (EKS) y Terraform

### 1. Pre-requisitos
- Cuenta de AWS y credenciales configuradas (`aws configure`).
- Terraform instalado.
- Docker Hub con tu imagen subida (el pipeline ya lo hace).
- (Opcional) kubectl instalado.

### 2. Infraestructura como código
En la carpeta `infra/` tienes los archivos:
- `provider.tf`: Define el proveedor AWS.
- `main.tf`: Usa el módulo oficial de EKS para crear el clúster y nodos.
- `variables.tf`: Variables para VPC y subredes.
- `outputs.tf`: Muestra el nombre y endpoint del clúster.

**Debes editar `main.tf` y/o crear un archivo `terraform.tfvars` con los IDs reales de tu VPC y subredes.**

### 3. Despliegue paso a paso
```bash
cd infra
terraform init
terraform apply
```
Esto creará el clúster EKS y los nodos en AWS.

### 4. Configura kubectl
```bash
aws eks --region us-east-1 update-kubeconfig --name devops-cluster
```

### 5. Despliega tu microservicio
1. Edita `k8s/deployment.yaml` para usar la imagen de Docker Hub.
2. Aplica los manifiestos:
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```
3. Obtén la IP pública del servicio:
   ```bash
   kubectl get svc devops-microservice
   ```

### 6. Accede a tu microservicio
- Usa la IP y el puerto mostrados para probar el endpoint `/DevOps` desde cualquier lugar.

---

## Nota sobre conflicto de puertos con Docker
Si al levantar los servicios con Docker Compose ves un error como:
```
Bind for 0.0.0.0:8001 failed: port is already allocated
```
Esto significa que el puerto 8001 ya está en uso (probablemente por Docker Desktop). Para solucionarlo:
1. Ejecuta `lsof -i :8001` para ver qué proceso lo usa.
2. Reinicia Docker Desktop para liberar el puerto.
3. Si el problema persiste, reinicia tu computadora.
4. Vuelve a intentar: `docker-compose up -d --build` 