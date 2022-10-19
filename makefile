SHELL = bash
all:
	@echo -e "Ljinux package builder.\n\nUsage:\n\tmake package\n\tmake clean"
package:
	@python3 -u scripts/generate_package.py
clean:
	@if [ -e "package.jpk" ]; then rm package.jpk; fi
