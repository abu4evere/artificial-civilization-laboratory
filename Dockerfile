# Their world, as a container that never stops. Built for Fly.io, but plain
# enough to run anywhere that takes a Dockerfile.
#
# No dependencies: the simulation is standard-library Python.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY acl ./acl

# The world lives on the volume mounted at /data. It must NOT sit under /app:
# that directory is replaced on every deploy, which would end their world.
ENV ACL_HOME=/data/world \
    HOST=0.0.0.0 \
    PORT=8080

EXPOSE 8080
# --public: the page is watch-only and nothing can stop or speed up the world from outside.
CMD ["python", "-m", "acl", "live", "--public"]
