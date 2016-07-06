FROM python:2-onbuild
CMD ["gunicorn", "votersearch.webapp:application", "-b", "0.0.0.0:8080", "--threads", "4"]
EXPOSE 8080
MAINTAINER Anand Chitipothu <anandology@gmail.com>
