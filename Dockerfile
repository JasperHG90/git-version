FROM python:3.11.9-slim-bookworm AS build

COPY --from=ghcr.io/astral-sh/uv:0.4.12 /uv /bin/uv

RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY src /

RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv sync --frozen --no-dev

ENV PATH="/.venv/bin:$PATH"

FROM python:3.11.9-slim-bookworm

COPY --from=build /.venv /.venv
COPY --from=build /git_version /git_version
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
