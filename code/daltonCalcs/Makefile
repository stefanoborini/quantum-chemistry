PACKAGE_NAME=daltonCalcs
PACKAGE_VERSION=1.6.0

.PHONY: package package-install package-clean deps nutz nutz-install

nutz: $(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz
package: $(PACKAGE_NAME)-$(PACKAGE_VERSION).package

$(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz: $(PACKAGE_NAME)-$(PACKAGE_VERSION).package
	cd $(PACKAGE_NAME)-$(PACKAGE_VERSION).package; zip -r ../$(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz .

$(PACKAGE_NAME)-$(PACKAGE_VERSION).package: manifest.xml \
											Executables/noarch/computeFirstHyperpol20090203.py \
											Executables/noarch/computeSecondHyperpol20090203.py \
											Executables/noarch/optimizeGeometryCAMB3LYP20090307.py \
											Executables/noarch/optimizeGeometryCAMB3LYP20090717.py \
											Executables/noarch/vibanaCAMB3LYP20090818.py \
											Executables/noarch/linearResponseExcitationCAMB3LYP20090903.py
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

package-clean:
	-rm -rf $(PACKAGE_NAME)-$(PACKAGE_VERSION).package $(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz

clean: package-clean
