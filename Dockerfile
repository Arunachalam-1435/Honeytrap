#Use lightweight python image
FROM python:3.11-slim

#Set working directory
WORKDIR /app

#Copy project files inside container
COPY . .

#Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod u+x start-up.sh

#Expose ports
EXPOSE 2222
EXPOSE 8080

#Run honeypot
CMD ["./start-up.sh"]