SETUPTOOLS_VERSION=0.6c9
SETUPTOOLS_TARGET=$(BUILD_FLAGS_DIR)/setuptools
SETUPTOOLS_PACKAGE=setuptools-$(SETUPTOOLS_VERSION).tar.gz
SETUPTOOLS_PACKAGE_URL=http://pypi.python.org/packages/source/s/setuptools/$(SETUPTOOLS_PACKAGE)

setuptools: $(SETUPTOOLS_TARGET)
setuptools-download: $(DOWNLOAD_DIR)/$(SETUPTOOLS_PACKAGE)

$(SETUPTOOLS_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(SETUPTOOLS_PACKAGE)
	-rm -rf $(UNPACK_DIR)/setuptools-$(SETUPTOOLS_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(SETUPTOOLS_PACKAGE)
	cd $(UNPACK_DIR)/setuptools-$(SETUPTOOLS_VERSION); export PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.4/site-packages/; $(RUNTIME_DIR)/bin/python2.4 setup.py install --prefix=$(RUNTIME_DIR)
	touch $(SETUPTOOLS_TARGET)

$(DOWNLOAD_DIR)/$(SETUPTOOLS_PACKAGE): $(INIT_TARGET)
	for package in $(SETUPTOOLS_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(SETUPTOOLS_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(SETUPTOOLS_PACKAGE)

