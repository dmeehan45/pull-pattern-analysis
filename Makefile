.PHONY: validate index qa

validate:
	python3 scripts/validate_corpus.py --root .

index:
	python3 scripts/generate_index.py --root .

qa:
	python3 scripts/qa.py
