UNUM_VERSION=4.0
UNUM_TARGET=$(BUILD_FLAGS_DIR)/unum
UNUM_PACKAGE=Unum-$(UNUM_VERSION).tar.gz
UNUM_PACKAGE_URL=http://switch.dl.sourceforge.net/sourceforge/unum/$(UNUM_PACKAGE)

.PHONY: unum unum-download
unum: $(UNUM_TARGET)
unum-download: $(DOWNLOAD_DIR)/$(UNUM_PACKAGE)

$(UNUM_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(UNUM_PACKAGE)
	-rm -rf $(UNPACK_DIR)/Unum-$(UNUM_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(UNUM_PACKAGE)
	-cd $(UNPACK_DIR)/Unum-$(UNUM_VERSION); \
	cd $(UNPACK_DIR)/Unum-$(UNUM_VERSION); export PYTHONPATH=$(RUNTIME_DIR)/lib/python2.4/site-packages/; $(RUNTIME_DIR)/bin/python2.4 setup.py install --prefix=$(RUNTIME_DIR)
	touch $(UNUM_TARGET)

$(DOWNLOAD_DIR)/$(UNUM_PACKAGE): $(INIT_TARGET)
	for package in $(UNUM_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(UNUM_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(UNUM_PACKAGE)
