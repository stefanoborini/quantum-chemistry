IPYTHON_VERSION=0.10
IPYTHON_TARGET=$(BUILD_FLAGS_DIR)/ipython
IPYTHON_PACKAGE=ipython-$(IPYTHON_VERSION).tar.gz
IPYTHON_PACKAGE_URL=http://ipython.scipy.org/dist/$(IPYTHON_PACKAGE)

ipython: $(IPYTHON_TARGET)
ipython-download: $(DOWNLOAD_DIR)/$(IPYTHON_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)
$(IPYTHON_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(IPYTHON_PACKAGE)
	-rm -rf $(UNPACK_DIR)/ipython-$(IPYTHON_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(IPYTHON_PACKAGE)
	cd $(UNPACK_DIR)/ipython-$(IPYTHON_VERSION); export PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.4/site-packages/; $(RUNTIME_DIR)/bin/python2.4 setup.py install --prefix=$(RUNTIME_DIR)
	touch $(IPYTHON_TARGET)
endif

ifeq ($(ARCH),x86_64-redhat-linux)
$(IPYTHON_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(IPYTHON_PACKAGE)
	-rm -rf $(UNPACK_DIR)/ipython-$(IPYTHON_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(IPYTHON_PACKAGE)
	cd $(UNPACK_DIR)/ipython-$(IPYTHON_VERSION); export LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.4/site-packages/; $(RUNTIME_DIR)/bin/python2.4 setup.py install --prefix=$(RUNTIME_DIR)
	touch $(IPYTHON_TARGET)
endif

$(DOWNLOAD_DIR)/$(IPYTHON_PACKAGE): $(INIT_TARGET)
	for package in $(IPYTHON_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(IPYTHON_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(IPYTHON_PACKAGE)
