# Microservicio DevOps - Banco Pichincha

Este proyecto es un microservicio en FastAPI que expone el endpoint `/DevOps`, protegido por API Key y JWT, listo para ser desplegado y escalado con Docker, Kubernetes y AWS EKS. Incluye CI/CD, tests automáticos, gestión de API Keys y ejemplo de integración con Kong.

---

## ¿Qué hace este microservicio?

- Expone un endpoint `/DevOps` que recibe un mensaje y responde con un saludo personalizado.
- Protegido por API Key (en el header `X-Parse-REST-API-Key`).
- Genera un JWT único por cada transacción y lo devuelve en el header `X-JWT-KWY`.
- Solo acepta POST. Otros métodos devuelven `"ERROR"`.

---

## Estructura del proyecto

- **app/**: Código fuente del microservicio (FastAPI).
  - `main.py`: Endpoints y lógica principal.
  - `auth.py`: Validación de API Key y generación de JWT.
  - `models.py`: Esquema de datos (Pydantic).
- **tests/**: Tests automáticos con pytest.
- **k8s/**: Manifiestos de Kubernetes (deployment y service).
- **infra/**: Infraestructura como código (Terraform para AWS EKS).
- **Dockerfile** y **docker-compose.yml**: Contenerización y orquestación.
- **.github/workflows/ci.yml**: Pipeline CI/CD con GitHub Actions.

---

## ¿Cómo levantar el microservicio?

### 1. Modo local (desarrollo)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Prueba el endpoint:
```bash
curl -X POST \
  -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" \
  -H "Content-Type: application/json" \
  -d '{"message":"This is a test","to":"Juan Perez","from":"Rita Asturia","timeToLifeSec":45}' \
  http://localhost:8000/DevOps
```

---

### 2. Con Docker y Docker Compose
```bash
docker build -t devops-microservice:latest .
docker-compose up --scale app=2
```
Accede al servicio en:  
`http://localhost:8002/DevOps`

---

### 3. Con Kubernetes (local o cloud)
1. Sube la imagen a Docker Hub (o usa la que sube el pipeline):
   ```bash
   docker tag devops-microservice:latest tu_usuario_dockerhub/devops-microservice:latest
   docker push tu_usuario_dockerhub/devops-microservice:latest
   ```
2. Edita `k8s/deployment.yaml` y pon tu imagen.
3. Aplica los manifiestos:
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```
4. Busca la IP pública del servicio:
   ```bash
   kubectl get svc devops-microservice
   ```
5. Prueba el endpoint desde cualquier lugar.

---

### 4. CI/CD y despliegue automático
- El pipeline de GitHub Actions construye, testea, revisa el código y sube la imagen a Docker Hub en cada push a `main`.
- Configura los secretos `DOCKERHUB_USERNAME` y `DOCKERHUB_TOKEN` en tu repo.

---

### 5. API Key y JWT
- El microservicio valida la API Key (`X-Parse-REST-API-Key`) y genera un JWT único por transacción.
- El JWT se devuelve en el header `X-JWT-KWY` de la respuesta.

---

### 6. API Manager con Kong (opcional)
- El microservicio ya valida la API Key y genera JWT por sí mismo.
- Si quieres, puedes levantar Kong con Docker Compose para gestionar las API Keys de forma centralizada.
- Ejemplo de comandos para registrar el servicio y activar el plugin de API Key en Kong:
```bash
# Crea el servicio en Kong
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
  --data 'username=usuario'
curl -i -X POST --url http://localhost:8001/consumers/usuario/key-auth
```
- Si no quieres usar Kong, simplemente ignora esta sección: el microservicio funcionará igual de seguro.

---

### 7. Infraestructura como código (AWS EKS con Terraform)
1. Ve a la carpeta `infra/` y **abre el archivo `main.tf`**.  
   Allí verás comentarios como:
   ```hcl
   # IMPORTANTE: Reemplaza la siguiente línea con los IDs de tus subredes reales de AWS
   subnet_ids      = ["<subnet-ids>"]
   # IMPORTANTE: Reemplaza la siguiente línea con el ID real de tu VPC de AWS
   vpc_id          = "<vpc-id>"
   ```
   **Sustituye `<subnet-ids>` y `<vpc-id>` por los valores reales de tu cuenta de AWS.**
2. Inicializa y aplica Terraform:
   ```bash
   cd infra
   terraform init
   terraform apply
   ```
3. Configura kubectl:
   ```bash
   aws eks --region us-east-1 update-kubeconfig --name devops-cluster
   ```
4. Despliega el microservicio con los manifiestos de Kubernetes.

---

### 8. Testing y calidad
- Corre los tests:
  ```bash
  pytest
  ```
- Revisa el estilo del código:
  ```bash
  flake8 app tests
  ```

---

### 9. Problemas comunes
- Si Docker te da error de puerto ocupado (`Bind for 0.0.0.0:8001 failed`), reinicia Docker Desktop o tu máquina.

---

### 10. Contacto
¿Dudas o sugerencias?  
kevinarmashbk232@gmail.com

---

¡Listo! Así puedes levantar, probar y desplegar todo lo que ya está hecho en este proyecto. 