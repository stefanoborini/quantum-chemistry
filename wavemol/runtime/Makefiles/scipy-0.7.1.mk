SCIPY_VERSION=0.7.1
SCIPY_TARGET=$(BUILD_FLAGS_DIR)/scipy
SCIPY_PACKAGE=scipy-$(SCIPY_VERSION).tar.gz
SCIPY_PACKAGE_URL=http://jaist.dl.sourceforge.net/sourceforge/scipy/$(SCIPY_PACKAGE)

scipy: $(SCIPY_TARGET)
scipy-download: $(DOWNLOAD_DIR)/$(SCIPY_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)
$(SCIPY_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(SCIPY_PACKAGE) 
	-rm -rf $(UNPACK_DIR)/scipy-$(SCIPY_VERSION)/
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(SCIPY_PACKAGE)
	cd $(UNPACK_DIR)/scipy-$(SCIPY_VERSION); export PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.4/site-packages/; $(RUNTIME_DIR)/bin/python2.4 setup.py install --prefix=$(RUNTIME_DIR)
	touch $(SCIPY_TARGET)
endif

ifeq ($(ARCH),x86_64-redhat-linux)
$(SCIPY_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(SCIPY_PACKAGE) 
	-rm -rf $(UNPACK_DIR)/scipy-$(SCIPY_VERSION)/
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(SCIPY_PACKAGE)
	cd $(UNPACK_DIR)/scipy-$(SCIPY_VERSION); export CC="gcc -m64" FC="g95 -m64" CPPFLAGS="-I$(RUNTIME_DIR)/include" CFLAGS="-m64 -I$(RUNTIME_DIR)/include" LD_LIBRARY_PATH=$(RUNTIME_DIR)/lib64:$(RUNTIME_DIR)/lib:$$LD_LIBRARY_PATH PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.4/site-packages/; $(RUNTIME_DIR)/bin/python2.4 setup.py install --prefix=$(RUNTIME_DIR)
	touch $(SCIPY_TARGET)
endif

$(DOWNLOAD_DIR)/$(SCIPY_PACKAGE): $(INIT_TARGET)
	for package in $(SCIPY_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(SCIPY_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(SCIPY_PACKAGE)
