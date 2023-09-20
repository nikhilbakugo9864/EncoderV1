#Thanks To Col Serra
FROM colserra/light-encoder:libfdk-aac
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
