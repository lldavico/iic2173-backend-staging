FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install appoptics-apm
RUN export APPOPTICS_SERVICE_KEY=xpKp_JPfTVCuETTRHANl30T7MiX0t_yGHB2iBJgd_5M9uPx0vudRv7JACY-nfGu09_wf9YY:gruponce-good
COPY . /code/