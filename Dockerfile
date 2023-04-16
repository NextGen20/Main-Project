        FROM python:3.8-slim-buster
	
	# Create app directory
	WORKDIR /app
	
	
	COPY requirements.txt ./
	
	#upgrade pip+install flask
	RUN pip install --upgrade pip
	RUN pip install -r requirements.txt
	
	# Bundle app source
	COPY . .
	
	#port expose for web app
	EXPOSE 5000
	
	#run on command line with param
	CMD ["python3.8", "app.py"]
