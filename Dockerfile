FROM python:3.12-slim

RUN groupadd -r viper && useradd -r -g viper viper

WORKDIR /home/viper

COPY pyproject.toml pdm.lock ./
RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false
RUN pdm install --check --prod --no-editable
ENV PATH="/home/viper/.venv/bin:$PATH"

COPY viper viper
COPY app.py docker-entrypoint.sh ./

RUN chown -R viper:viper .
USER viper

ENV FLASK_APP=app.py
ENV FLASK_CONFIG=production

EXPOSE 8848
ENTRYPOINT ["./docker-entrypoint.sh"]
