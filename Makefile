.PHONY: help install uninstall test

help:
	@echo "make install    symlink skills into ~/.agents/skills and ~/.claude/skills (TARGET=dir to override)"
	@echo "make uninstall  remove the symlinks this repo created"
	@echo "make test       validate every skill"

install:
	./setup.sh $(if $(TARGET),--target $(TARGET))

uninstall:
	./setup.sh --uninstall $(if $(TARGET),--target $(TARGET))

test:
	./test.sh
