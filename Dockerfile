# Imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto por el que correrá la aplicación
EXPOSE 8888

# Comando por defecto para arrancar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]

