FROM kbase/sdkbase2:python
MAINTAINER Drew Cross
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# RUN apt-get update


# -----------------------------------------

COPY ./ /kb/module

RUN chmod -R a+rw /kb/module

WORKDIR /kb/module
RUN  curl -L -O https://github.com/DrewCross/citHost/raw/master/cover  && \
	chmod +x /kb/module/cover
RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
