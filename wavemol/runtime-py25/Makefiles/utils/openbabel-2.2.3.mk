OPENBABEL_VERSION=2.2.3
OPENBABEL_TARGET=$(BUILD_FLAGS_DIR)/openbabel
OPENBABEL_PACKAGE=openbabel-$(OPENBABEL_VERSION).tar.gz
OPENBABEL_PACKAGE_URL=http://switch.dl.sourceforge.net/project/openbabel/openbabel/$(OPENBABEL_VERSION)/$(OPENBABEL_PACKAGE)

openbabel: $(OPENBABEL_TARGET)
openbabel-download: $(DOWNLOAD_DIR)/$(OPENBABEL_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)
$(OPENBABEL_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(OPENBABEL_PACKAGE) 
	-rm -rf $(UNPACK_DIR)/openbabel-$(OPENBABEL_VERSION)/
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(OPENBABEL_PACKAGE)
	cd $(UNPACK_DIR)/openbabel-$(OPENBABEL_VERSION); export PATH=$(RUNTIME_DIR)/bin:$$PATH; ./configure --prefix=$(RUNTIME_DIR); make -j2; make install
	cd $(UNPACK_DIR)/openbabel-$(OPENBABEL_VERSION)/scripts/python; export PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.5/site-packages/; $(RUNTIME_DIR)/bin/python2.5 setup.py install --prefix=$(RUNTIME_DIR)
	touch $(OPENBABEL_TARGET)
endif

ifeq ($(ARCH),x86_64-redhat-linux)
$(OPENBABEL_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(OPENBABEL_PACKAGE) 
	-rm -rf $(UNPACK_DIR)/openbabel-$(OPENBABEL_VERSION)/
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(OPENBABEL_PACKAGE)
	cd $(UNPACK_DIR)/openbabel-$(OPENBABEL_VERSION); export CFLAGS="$$CFLAGS -m64" FC="g95 -m64" FCFLAGS="$$FCFLAGS -m64" LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.5/site-packages/; ./configure --prefix=$(RUNTIME_DIR); make -j2; make install
	cd $(UNPACK_DIR)/openbabel-$(OPENBABEL_VERSION)/scripts/python; export CFLAGS="$$CFLAGS -m64" FC="g95 -m64" FCFLAGS="$$FCFLAGS -m64" LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.5/site-packages/; $(RUNTIME_DIR)/bin/python2.5 setup.py install --prefix=$(RUNTIME_DIR)
	touch $(OPENBABEL_TARGET)
endif

$(DOWNLOAD_DIR)/$(OPENBABEL_PACKAGE): $(INIT_TARGET)
	for package in $(OPENBABEL_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(OPENBABEL_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(OPENBABEL_PACKAGE)
