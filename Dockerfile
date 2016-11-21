FROM centos:7

RUN yum install -y epel-release
RUN yum install -y supervisor
RUN curl https://bootstrap.pypa.io/get-pip.py | python
RUN pip install flask lxml 

COPY bin /opt/hatebu_with_ng/bin
COPY supervisord.conf /etc/supervisord.conf

CMD python /opt/hatebu_with_ng/bin/createdb.py && /usr/bin/supervisord -c /etc/supervisord.conf
