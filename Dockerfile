#
# update history:
# 08/20/20 - changed to nvidia base for DL methods
 
FROM nvidia/cuda

RUN apt-get update -y
RUN apt-get install -y lsof

# setup python environment for scripts 
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --no-cache-dir pillow
RUN pip3 install torch
RUN pip3 install monai

ADD setup.sh /tmp/setup.sh
ADD snapshot.sh /tmp/snapshot.sh
ADD script.py /tmp/script.py
RUN chmod 0755 /tmp/snapshot.sh
RUN chmod 0755 /tmp/setup.sh

# Give execution rights on the setup
RUN chmod 0755 /tmp/setup.sh

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#Install Cron && Start Cron service
RUN apt-get -y install cron
RUN service cron start

# Run the command on container startup
ENTRYPOINT service cron start && /tmp/setup.sh
