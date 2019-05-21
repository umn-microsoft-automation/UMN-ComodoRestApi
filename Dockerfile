FROM python:3
WORKDIR /usr/src/app
RUN git clone  https://github.com/umn-microsoft-automation/UMN-ComodoRestApi.git /usr/src/app
COPY cert.py .
CMD mkdir out 
RUN pip install requests