deploy-neo4j:
	@docker run \
	--restart always \
	--publish=7474:7474 \
	--publish=7687:7687 \
	--env NEO4J_AUTH=neo4j/password \
	--volume ./neo4j_volume/data:/data \
	--volume ./neo4j_volume/logs:/logs \
	neo4j:4.4.28

import-data:
	@python ./src/build_knowledge_graph.py

clean:
	@find . -name "*.pyc" -exec rm -f {} \;
