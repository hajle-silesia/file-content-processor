# Use build image that allows to match Python version between build stage and runtime stage.
# "Distroless" images usually don't support the latest Python version. Instead, they follow the version allowed by distribution they use.
# Therefore, for consistency, it's reasonable to use the same distribution in the build stage.
FROM debian:12.10 AS build
ARG WORKDIR="/project"
WORKDIR "${WORKDIR}"
ARG VENV_DIR=".venv"
ENV PATH="${WORKDIR}/${VENV_DIR}/bin:${PATH}"
# Install python3-venv for built-in Python 3 venv module (not installed by default).
# Install gcc, libpython3-dev to compile CPython modules.
RUN apt-get update && \
    apt-get install \
      --yes \
      --no-install-suggests \
      --no-install-recommends \
      python3-venv \
      gcc libpython3-dev
# Install and upgrade pip, setuptools, wheel to build and distribute Python packages.
RUN python3 -m venv "${VENV_DIR}" && \
    python3 -m pip install --upgrade pip setuptools wheel

FROM build AS build-venv
ARG REQUIREMENTS_FILE="requirements.txt"
COPY "${REQUIREMENTS_FILE}" .
RUN if [ -f "${REQUIREMENTS_FILE}" ]; then python3 -m pip install -r "${REQUIREMENTS_FILE}"; fi

FROM gcr.io/distroless/python3-debian12@sha256:7729c7979e1097d2b60fffb0af904a59e16af241b7c8eef4c613013ef1504ff8 AS runtime
ARG WORKDIR="/project"
WORKDIR "${WORKDIR}"
ENV PATH="${WORKDIR}/.venv/bin:${PATH}"
COPY --from=build-venv "${WORKDIR}" "${WORKDIR}"
ARG APP_DIR="src/file_content_processor"
COPY "${APP_DIR}" "${APP_DIR}"
ENTRYPOINT ["python3", "src/file_content_processor/main.py"]
