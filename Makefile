run:
	- python main.py 

type_hints:
	- mypy main.py


.DEFAULT_GOAL:=help
help:
	@echo "***********	AVAILABLE COMMANDS	***********\n"
	@echo " - run      : Runs the program "
	@echo " - type_hints     : Runs type checking"

