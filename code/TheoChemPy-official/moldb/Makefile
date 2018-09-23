PACKAGE_NAME=moldb
PACKAGE_VERSION=2.0.0

.PHONY: package package-install package-clean deps nutz nutz-install

nutz: $(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz
package: $(PACKAGE_NAME)-$(PACKAGE_VERSION).package 

$(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz: $(PACKAGE_NAME)-$(PACKAGE_VERSION).package 
	cd $(PACKAGE_NAME)-$(PACKAGE_VERSION).package; zip -r ../$(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz .

$(PACKAGE_NAME)-$(PACKAGE_VERSION).package: manifest.xml $(wildcard Executables/noarch/*.py) deps
	mkdir -p $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/
	cp manifest.xml $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/manifest.xml
	tar -cv --exclude=.svn Executables | tar -x -C $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/
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
	cp -r /Users/sbo/Work/Programs/theochempy/trunk dependencies/theochempy-trunk
	cd dependencies/theochempy-trunk && python setup.py install --home=../../$(PACKAGE_NAME)-$(PACKAGE_VERSION).package/Libraries/noarch/python

package-clean:
	-rm -rf $(PACKAGE_NAME)-$(PACKAGE_VERSION).package $(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz

clean: package-clean
	-rm -rf dependencies
