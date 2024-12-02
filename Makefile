YOUR_SESSION_COOKIE_VALUE = 53616c7465645f5fe813f9cf17cb97ef838a5143f062fe737c7768ef78931572e2c05a8835e8d3fd58ff8617104e29fe52c2e158f6bc5fb8e4bc97b68a254c64

env:
	python3 -m venv .venv
	. .venv/bin/activate
	

install:
	pip install -r requirements.txt

download-data:
	for day in {1..25}; do \
		curl -b "session=$(YOUR_SESSION_COOKIE_VALUE)" -o data/$$day "https://adventofcode.com/2024/day/$$day/input"; \
	done

test:
	pytest --doctest-modules -v

all: env install download-data test