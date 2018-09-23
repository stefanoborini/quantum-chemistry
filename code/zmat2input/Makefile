PACKAGE_NAME=zmat2input
PACKAGE_VERSION=1.1.0

.PHONY: package package-install package-clean deps nutz nutz-install

nutz: $(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz
package: $(PACKAGE_NAME)-$(PACKAGE_VERSION).package

$(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz: $(PACKAGE_NAME)-$(PACKAGE_VERSION).package
	cd $(PACKAGE_NAME)-$(PACKAGE_VERSION).package; zip -r ../$(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz .

$(PACKAGE_NAME)-$(PACKAGE_VERSION).package: manifest.xml Executables/noarch/zmat2input.py deps
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
	cp -r /Users/sbo/Work/Programs/theochempy/tags/0.14.2 dependencies/theochempy-0.14.1
	cd dependencies/theochempy-0.14.1 && python setup.py install --home=../../$(PACKAGE_NAME)-$(PACKAGE_VERSION).package/Libraries/noarch/python

package-clean:
	-rm -rf $(PACKAGE_NAME)-$(PACKAGE_VERSION).package

clean: package-clean

veryclean: clean
	-rm -rf dependencies
