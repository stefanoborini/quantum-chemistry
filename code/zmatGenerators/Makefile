PACKAGE_NAME=zmatGenerators
PACKAGE_VERSION=2.0.1

.PHONY: package package-install package-clean deps nutz nutz-install

EXECUTABLES=    Executables/noarch/polyacetylenes_h-h_subst_generator.py    \
				Executables/noarch/polyacetylenes_h-cn_subst_generator.py      \
				Executables/noarch/polyacetylenes_h-oh_subst_generator.py  \
				Executables/noarch/polyacetylenes_h-no2_subst_generator.py     \
				Executables/noarch/polyacetylenes_h-nh2_subst_generator.py     \
				Executables/noarch/polyacetylenes_cn-cn_subst_generator.py     \
				Executables/noarch/polyacetylenes_cn-oh_subst_generator.py  \
				Executables/noarch/polyacetylenes_cn-no2_subst_generator.py \
				Executables/noarch/polyacetylenes_cn-nh2_subst_generator.py   \
				Executables/noarch/polyacetylenes_oh-oh_subst_generator.py\
				Executables/noarch/polyacetylenes_oh-no2_subst_generator.py\
				Executables/noarch/polyacetylenes_oh-nh2_subst_generator.py\
				Executables/noarch/polyacetylenes_no2-no2_subst_generator.py   \
				Executables/noarch/polyacetylenes_no2-nh2_subst_generator.py   \
				Executables/noarch/polyacetylenes_nh2-nh2_subst_generator.py   \
				Executables/noarch/polyacetylenes_generator.sh  \
				Executables/noarch/lateral_subst_full.py \
				Executables/noarch/lateral_subst_one.py \
				Executables/noarch/lateral_subst_two.py


nutz: $(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz
package: $(PACKAGE_NAME)-$(PACKAGE_VERSION).package

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

$(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz: $(PACKAGE_NAME)-$(PACKAGE_VERSION).package
	cd $(PACKAGE_NAME)-$(PACKAGE_VERSION).package; zip -r ../$(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz .

$(PACKAGE_NAME)-$(PACKAGE_VERSION).package: manifest.xml $(EXECUTABLES) 
	-mkdir $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/
	cp manifest.xml $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/manifest.xml
	cp -r Executables $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/
	chmod 755 $(PACKAGE_NAME)-$(PACKAGE_VERSION).package/Executables/noarch/*

package-clean:
	-rm -rf $(PACKAGE_NAME)-$(PACKAGE_VERSION).package $(PACKAGE_NAME)-$(PACKAGE_VERSION).nutz

clean: package-clean

veryclean: clean
