local:
	- python main.py test_index "http://127.0.0.1:9200"

devnet:
	- python main.py d001_fa4_file_1 "https://admin:password@batch01-dev-search.aslead.cloud/es/"

runner:
	- python main.py d001_fa4_file_1 "https://admin:password@10.10.13.142/es"

.DEFAULT_GOAL:=help
help:
	@echo "***********	AVAILABLE COMMANDS	***********\n"
	@echo " - local      : Runs the program using data from the local ES server"
	@echo " - devnet     : Runs the program using data from the devnet server"

