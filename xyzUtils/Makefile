PACKAGE_NAME=xyzUtils
PACKAGE_VERSION=1.0.0

.PHONY: package package-install package-clean deps

package: $(PACKAGE_NAME)-$(PACKAGE_VERSION).package

$(PACKAGE_NAME)-$(PACKAGE_VERSION).package: manifest.xml Executables/noarch/center.py
	mkdir -p $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/
	cp manifest.xml $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/manifest.xml
	tar -cv --exclude=.svn Executables | tar -x -C $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/
	chmod 755 $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/Executables/noarch/*

package-install: package
	@if test "x$$PREFIX" == "x"; then \
		echo "Please specify PREFIX variable"; \
		exit 1; \
	fi
	-mkdir -p $$PREFIX
	cp -r $(PACKAGE_NAME)-$(PACKAGE_VERSION).package $$PREFIX

deps: 
	svn checkout https://stefanoborini@theochempy.svn.sourceforge.net/svnroot/theochempy/trunk dependencies/theochempy-trunk
	ln -s theochempy-trunk dependencies/theochempy
	cd dependencies/theochempy && python setup.py install --home=../../$(PACKAGE_NAME)-$(PACKAGE_VERSION).package/Libraries/noarch/python
	


package-clean:
	-rm -rf $(PACKAGE_NAME)-$(PACKAGE_VERSION).package

clean: package-clean
