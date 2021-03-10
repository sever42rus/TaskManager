#!/bin/sh
APP="$0"
COMMAND=$1
if [ $COMMAND ]; then
	shift
fi
ARGS=$@

if [ "$DOCKER_COMPOSE_MODE" = "PROD" ]; then
	echo "** PROD MODE using docker-compose.production.yml"
	COMPOSE="docker-compose -f docker-compose.production.yml"
else
	echo "** DEV MODE"
	COMPOSE="docker-compose"
fi


DJANGO="$COMPOSE exec backend"
MANAGE="$DJANGO python3 manage.py"

if [ "$COMMAND" = "ps" ]; then
    $COMPOSE ps $ARGS
elif [ "$COMMAND" = "exec" ]; then
    $COMPOSE exec $ARGS
elif [ "$COMMAND" = "update" ]; then
	git pull
	$MANAGE migrate
    $COMPOSE run frontend npm run build
    $COMPOSE restart django
elif [ "$COMMAND" = "build" ]; then
    $COMPOSE build $ARGS
elif [ "$COMMAND" = "start" ]; then
    $COMPOSE up -d $ARGS
elif [ "$COMMAND" = "logs" ]; then
    $COMPOSE logs $ARGS
elif [ "$COMMAND" = "stop" ]; then
    $COMPOSE stop $ARGS
elif [ "$COMMAND" = "dbshell" ]; then
    $COMPOSE exec postgres psql -U postgres
elif [ "$COMMAND" = "req" ]; then
    $COMPOSE exec django pip install -r requirements.txt
elif [ "$COMMAND" = "bash" ]; then
    $DJANGO bash $ARGS
elif [ "$COMMAND" = "runserver" ]; then
    $MANAGE runserver 0.0.0.0:8000
else
    $MANAGE $COMMAND $ARGS
fi

exit
