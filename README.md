![flake8](https://github.com/JeeEssEm/todo-backend/actions/workflows/lint.yml/badge.svg)
# Backend for TO-DO app

# Quick start

## 1. Docker
#### 1. Clone repo
```git clone https://github.com/JeeEssEm/todo-backend```  
```cd todo-backend```

#### 2. Create image
```docker build -t fastapi_image```

#### 3. Run container 
```docker run -d --name fastapi_container -p 80:80 fastapi_image```

## 2. Manually
> Required: [python 3.10](https://www.python.org/downloads/release/python-3100/) 

#### 1. Clone repo
```git clone https://github.com/JeeEssEm/todo-backend```  
```cd todo-backend```
#### 2. Create virtual environment (venv)
```python -m venv .venv```
#### 3. Venv activation
> **Note:** in example venv activates in Windows using Powershell.  
> Solution for **Unix or MacOS** using **bash**:  
> ```source .venv/bin/activate```

```.\venv\Scripts\Activate.ps1```

#### 4. Install dependencies (using pip)
```pip install -r requirements.txt```

#### 5. Environment variables
Example of **.env**:
```
DB_URL=sqlite:///./app.db      # url for your database
SECRET_KEY=jk-asd23asd-asd231  # secret key
REFRESH_TOKEN_EXPIRE_DAYS=30   # time after which access token will expire
ACCESS_TOKEN_EXPIRE_MINUTES=30 # time after which access token will expire
STATIC_PATH=static             # path for static files (images, etc)
```
#### 6. Run project
```uvicorn main:app --reload --host 0.0.0.0 --port 8000```


# Team

### 1. [Frontend](https://github.com/TheMerret/todoshlyop)
#### Харитонов Максим
### 2. [Mobile](https://github.com/DaniilSukhanov/DevTimeHack_MI-HS-EM_iOS)
#### Суханов Даниил
### 3. Backend (this repo)
#### Морозов Григорий
