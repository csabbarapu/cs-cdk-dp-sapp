FROM python:3-slim AS build-env
ADD ./app /app
WORKDIR /app
COPY ./app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --target .
FROM gcr.io/distroless/python3
COPY --from=build-env /app /app
WORKDIR /app
EXPOSE 5000
CMD [ "-m" , "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
