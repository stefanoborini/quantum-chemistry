PACKAGE_NAME=computeSecondHyperpol
PACKAGE_VERSION=2.0.0


.PHONY: package package-install package-clean deps

package-install: package
	@if test "x$$PREFIX" == "x"; then \
		echo "Please specify PREFIX variable"; \
		exit 1; \
	fi
	-mkdir -p $$PREFIX
	cp -r $(PACKAGE_NAME)-$(PACKAGE_VERSION).package $$PREFIX


package: $(PACKAGE_NAME)-$(PACKAGE_VERSION).package

$(PACKAGE_NAME)-$(PACKAGE_VERSION).package: manifest.xml compute20090203.py
	-rm -rf $(PACKAGE_NAME)-$(PACKAGE_VERSION).package
	mkdir -p $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/Executables/noarch
	cp manifest.xml $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/manifest.xml
	cp compute20090203.py $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/Executables/noarch/ 
	chmod 755 $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/Executables/noarch/*

deps: 
	svn checkout https://stefanoborini@theochempy.svn.sourceforge.net/svnroot/theochempy/tags/0.11.0 dependencies/theochempy-0.11.0
	cd dependencies/theochempy-0.11.0 && python setup.py install --home=../../$(PACKAGE_NAME)-$(PACKAGE_VERSION).package/Libraries/noarch/python


package-clean:
	-rm -rf $(PACKAGE_NAME)-$(PACKAGE_VERSION).package

clean: package-clean
