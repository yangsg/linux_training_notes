#!/bin/bash

export CATALINA_HOME=/app/apache-tomcat-8.5.39
export CATALINA_BASE=/app/tomcat_multi_instances/tomcat01

case $1 in
start)
  $CATALINA_HOME/bin/startup.sh
  ;;
stop)
  $CATALINA_HOME/bin/shutdown.sh
  ;;
restart)
  $CATALINA_HOME/bin/shutdown.sh
  sleep 3
  $CATALINA_HOME/bin/startup.sh
  ;;
esac


