FROM python:3
WORKDIR /usr/src/app
RUN pip install requests
#RUN git clone  https://github.com/umn-microsoft-automation/UMN-ComodoRestApi.git /usr/src/app
#COPY Examples/cert.py .
COPY . /usr/src/app
CMD mkdir out 