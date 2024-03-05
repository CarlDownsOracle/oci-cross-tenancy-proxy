FROM fnproject/python:3.9-dev as build-stage
WORKDIR /function
ADD requirements.txt /function/

# The oci-cli package requires 'site-packages' be in its filepath in order to
# dynamically load itself at runtime (see oci_cli/dynamic_loader.py).

			RUN pip3 install --target /site-packages/  --no-cache --no-cache-dir -r requirements.txt &&\
			    rm -fr ~/.cache/pip /tmp* requirements.txt func.yaml Dockerfile .venv &&\
			    chmod -R o+r /site-packages
ADD . /function/
RUN rm -fr /function/.pip_cache
FROM fnproject/python:3.9
WORKDIR /function
COPY --from=build-stage /site-packages /site-packages
COPY --from=build-stage /function /function
RUN chmod -R o+r /function
ENV PYTHONPATH=/function:/site-packages
ENTRYPOINT ["/site-packages/bin/fdk", "/function/func.py", "handler"]


