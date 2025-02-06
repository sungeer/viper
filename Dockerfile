FROM python:3.12-slim

RUN groupadd -r greybook && useradd -r -g greybook greybook

WORKDIR /home/greybook

COPY pyproject.toml pdm.lock ./
RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false
RUN pdm install --check --prod --no-editable
ENV PATH="/home/greybook/.venv/bin:$PATH"

COPY greybook greybook
COPY migrations migrations
COPY uploads uploads
COPY app.py docker-entrypoint.sh ./

RUN chown -R greybook:greybook .
USER greybook

ENV FLASK_APP=app.py
ENV FLASK_CONFIG=production
ENV GREYBOOK_LOGGING_PATH=stream

EXPOSE 5000
ENTRYPOINT ["./docker-entrypoint.sh"]
