PACKAGE_NAME=daltonParsers
PACKAGE_VERSION=3.4.3

.PHONY: package package-install package-clean deps nutz nutz-install

nutz: $(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz
package: $(PACKAGE_NAME)-$(PACKAGE_VERSION).package

$(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz: $(PACKAGE_NAME)-$(PACKAGE_VERSION).package
	cd $(PACKAGE_NAME)-$(PACKAGE_VERSION).package; zip -r ../$(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz .

$(PACKAGE_NAME)-$(PACKAGE_VERSION).package: manifest.xml $(wildcard Executables/noarch/*.py) deps
	mkdir -p $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/Executables/noarch
	cp manifest.xml $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/manifest.xml
	cp -r Executables $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/
	chmod 755 $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/Executables/noarch/*

nutz-install: nutz
	@if test "x$$PREFIX" == "x"; then \
		echo "Please specify PREFIX variable"; \
		exit 1; \
	fi
	-mkdir -p $$PREFIX
	cp $(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz $$PREFIX

package-install: package
	@if test "x$$PREFIX" == "x"; then \
		echo "Please specify PREFIX variable"; \
		exit 1; \
	fi
	-mkdir -p $$PREFIX
	cp -r $(PACKAGE_NAME)-$(PACKAGE_VERSION).package $$PREFIX

deps: 
	-rm -rf dependencies
	-mkdir dependencies
	cp -r /Users/sbo/Work/Programs/theochempy/trunk dependencies/theochempy-0.15.0
	cd dependencies/theochempy-0.15.0 && python setup.py install --home=../../$(PACKAGE_NAME)-$(PACKAGE_VERSION).package/Libraries/noarch/python



package-clean:
	-rm -rf $(PACKAGE_NAME)-$(PACKAGE_VERSION).package

clean: package-clean
	rm $(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz

veryclean: clean
	-rm -rf dependencies
