FROM python:3.9

RUN curl -sSL https://install.python-poetry.org/ | python -
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
ENV PATH /root/.local/bin:$PATH
COPY . /landing
RUN rm /landing/.venv -d -r
WORKDIR /landing 
RUN poetry install

EXPOSE 9000

RUN poetry run python manage.py findstatic .
RUN poetry run python manage.py collectstatic --noinput

CMD poetry run python manage.py migrate && poetry run gunicorn landing.wsgi:application --bind 0.0.0.0:$PORT