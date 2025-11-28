# Azure Deployment Guide

## Option 1: Azure Container Apps (Recommended)

### Prerequisites
- Azure CLI installed
- Azure account with Container Apps enabled

### Steps

1. **Login to Azure**
```bash
az login
```

2. **Create Resource Group**
```bash
az group create --name rag-assistant-rg --location eastus
```

3. **Create Container Registry**
```bash
az acr create --resource-group rag-assistant-rg --name ragassistantacr --sku Basic
```

4. **Build and Push Docker Image**
```bash
# Login to ACR
az acr login --name ragassistantacr

# Build and push backend
cd backend
az acr build --registry ragassistantacr --image rag-backend:latest .

# Build and push frontend
cd ../frontend
az acr build --registry ragassistantacr --image rag-frontend:latest .
```

5. **Create Container App Environment**
```bash
az containerapp env create \
  --name rag-env \
  --resource-group rag-assistant-rg \
  --location eastus
```

6. **Deploy Backend**
```bash
az containerapp create \
  --name rag-backend \
  --resource-group rag-assistant-rg \
  --environment rag-env \
  --image ragassistantacr.azurecr.io/rag-backend:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars OPENAI_API_KEY=your_key_here
```

7. **Deploy Frontend**
```bash
az containerapp create \
  --name rag-frontend \
  --resource-group rag-assistant-rg \
  --environment rag-env \
  --image ragassistantacr.azurecr.io/rag-frontend:latest \
  --target-port 80 \
  --ingress external \
  --env-vars REACT_APP_API_URL=https://rag-backend.your-domain.azurecontainerapps.io
```

## Option 2: Azure App Service (Simpler)

1. **Install Azure CLI extension**
```bash
az extension add --name webapp
```

2. **Create App Service Plan**
```bash
az appservice plan create --name rag-plan --resource-group rag-assistant-rg --sku B1 --is-linux
```

3. **Create Web App**
```bash
az webapp create --resource-group rag-assistant-rg --plan rag-plan --name rag-assistant-backend --runtime "PYTHON:3.11"
```

4. **Deploy Code**
```bash
cd backend
az webapp up --name rag-assistant-backend --resource-group rag-assistant-rg --runtime "PYTHON:3.11"
```

5. **Set Environment Variables**
```bash
az webapp config appsettings set --resource-group rag-assistant-rg --name rag-assistant-backend --settings OPENAI_API_KEY=your_key_here
```

## Option 3: Azure VM (Most Control)

1. **Create VM**
```bash
az vm create --resource-group rag-assistant-rg --name rag-vm --image Ubuntu2204 --admin-username azureuser --generate-ssh-keys
```

2. **SSH into VM and install Docker**
```bash
ssh azureuser@<vm-ip>
sudo apt update
sudo apt install docker.io docker-compose -y
```

3. **Clone and deploy**
```bash
git clone <your-repo>
cd rag-assistant
docker-compose up -d
```


