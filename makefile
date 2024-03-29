deploy-neo4j:
	@docker run \
	--restart always \
	--publish=7474:7474 \
	--publish=7687:7687 \
	--env NEO4J_AUTH=neo4j/password \
	--volume ./neo4j_volume/data:/data \
	--volume ./neo4j_volume/logs:/logs \
	neo4j:4.4.28

run-all:
	@python src/graph_qa.py --data_path all --write_to_neo4j yes

run-test:
	@python src/graph_qa.py --data_path test --write_to_neo4j yes

restart-all:
	@python src/graph_qa.py --data_path all --write_to_neo4j no

restart-test:
	@python src/graph_qa.py --data_path test --write_to_neo4j no

clean:
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

test:
	@python src/test.py
