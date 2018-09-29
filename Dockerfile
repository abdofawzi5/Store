 FROM python:2
 RUN apt-get update -qq && apt-get install -y wkhtmltopdf xvfb && apt-get install -f

 # configure wkhtmltopdf
 RUN printf '#!/bin/bash\nxvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf -q $*' > /usr/bin/wkhtmltopdf.sh
 RUN chmod a+x /usr/bin/wkhtmltopdf.sh
 RUN ln -s /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf

 # configure the app
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD . /code/
