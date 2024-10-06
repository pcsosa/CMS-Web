	#!/bin/bash

	# Script para iniciar Keycloak con PostgreSQL
	bin/kc.sh start-dev \
	  --http-port 8080 \
	  --db=postgres \
	  --db-username=postgres \
	  --db-password=postgres \
	  --db-url=jdbc:postgresql://127.0.0.1:5432/dbkeycloak
