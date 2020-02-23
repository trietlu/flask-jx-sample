FROM python:onbuild
COPY requirements.txt .
COPY *.png .
COPY xss.html .
COPY flask_app.py .
ENV PORT 8080
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["/usr/src/app/flask_app.py"]
