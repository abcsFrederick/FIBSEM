# FROM ubuntu:latest
FROM  python:3

RUN apt-get update -y
RUN apt-get install -y lsof

RUN pip install --upgrade pip && \
    pip install --no-cache-dir pillow

# Add crontab file in the cron directory
# ADD crontab /etc/cron.d/snapshot-cron
# ADD snapshot.sh /tmp/snapshot.sh
# ADD script.py /tmp/script.py
# RUN chmod 0755 /tmp/snapshot.sh

ADD setup.sh /tmp/setup.sh
ADD snapshot.sh /tmp/snapshot.sh
ADD script.py /tmp/script.py
RUN chmod 0755 /tmp/snapshot.sh
RUN chmod 0755 /tmp/setup.sh

# Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/snapshot-cron
RUN chmod 0755 /tmp/setup.sh

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#Install Cron && Start Cron service
RUN apt-get -y install cron
RUN service cron start

# Run the command on container startup
#CMD cron && tail -f /var/log/cron.log
#ENTRYPOINT ["/tmp/snapshot.sh"]
ENTRYPOINT service cron start && /tmp/setup.sh
#CMD ["/tmp/snapshot.sh"]
