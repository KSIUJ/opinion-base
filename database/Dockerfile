FROM python:3.12-slim 
WORKDIR /app 
# Skopiuj listę zależności i zainstaluj je 
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt 
# Skopiuj kod aplikacji 
COPY . . 
# Flask będzie nasłuchiwał na porcie 5000 EXPOSE 5000 CMD ["python", "app.py"]
EXPOSE 5000 
CMD ["python", "app_test.py"]
