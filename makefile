deploy-neo4j:
	@docker run \
	--restart always \
	--publish=7474:7474 \
	--publish=7687:7687 \
	--env NEO4J_AUTH=neo4j/password \
	--volume ./neo4j_volume/data:/data \
	--volume ./neo4j_volume/logs:/logs \
	neo4j:4.4.28

import-all-data:
	@python ./src/graph.py --data all

import-test-data:
	@python ./src/graph.py --data test

clean:
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

test:
	@python ./src/test.py
