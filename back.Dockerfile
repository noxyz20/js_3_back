FROM python:3.8
RUN mkdir /opt/app
WORKDIR /opt/app
RUN apt-get update
RUN apt-get upgrade
RUN ["apt-get", "install", "-y", "libsm6", "libxext6", "libxrender-dev", "ffmpeg"]
COPY . .
RUN ls
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["export", "FLASK_APP=app"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD ["python3", "app.py"]
