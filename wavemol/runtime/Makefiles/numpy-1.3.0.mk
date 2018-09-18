NUMPY_VERSION=1.3.0
NUMPY_TARGET=$(BUILD_FLAGS_DIR)/numpy
NUMPY_PACKAGE=numpy-$(NUMPY_VERSION).tar.gz
NUMPY_PACKAGE_URL=http://switch.dl.sourceforge.net/sourceforge/numpy/$(NUMPY_PACKAGE)

numpy: $(NUMPY_TARGET)
numpy-download: $(DOWNLOAD_DIR)/$(NUMPY_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)
$(NUMPY_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(NUMPY_PACKAGE)
	export MACOSX_DEPLOYMENT_TARGET=10.6
	export CFLAGS="-arch i386 -arch x86_64"
	export FFLAGS="-arch i386 -arch x86_64"
	export LDFLAGS="-Wall -undefined dynamic_lookup -bundle -arch i386 -arch x86_64"
	-rm -rf $(UNPACK_DIR)/numpy-$(NUMPY_VERSION)/
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(NUMPY_PACKAGE)
	cd $(UNPACK_DIR)/numpy-$(NUMPY_VERSION); \
	 export PATH=$(RUNTIME_DIR)/bin:$$PATH LDFLAGS="$(LIBS):$(LDFLAGS)" CPPFLAGS="$(INCLUDES):$(CPPFLAGS)" PYTHONPATH=$(RUNTIME_DIR)/lib/python2.4/site-packages/; \
	 $(RUNTIME_DIR)/bin/python2.4 setup.py build --fcompiler=gnu95; \
	 $(RUNTIME_DIR)/bin/python2.4 setup.py install --prefix=$(RUNTIME_DIR)
	touch $(NUMPY_TARGET)
endif

ifeq ($(ARCH),x86_64-redhat-linux)
$(NUMPY_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(NUMPY_PACKAGE)
	-rm -rf $(UNPACK_DIR)/numpy-$(NUMPY_VERSION)/
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(NUMPY_PACKAGE)
	#cd $(UNPACK_DIR)/numpy-$(NUMPY_VERSION); export LDFLAGS="-Wl,-O1" LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin:$$PATH LDFLAGS="-Wl,-O1 -L$(RUNTIME_DIR)/lib -L$(RUNTIME_DIR)/lib64 $(LDFLAGS)" CPPFLAGS="-I$(RUNTIME_DIR)/include $(CPPFLAGS)" PYTHONPATH=$(RUNTIME_DIR)/lib/python2.4/site-packages/; $(RUNTIME_DIR)/bin/python2.4 setup.py build --fcompiler=gnu95; $(RUNTIME_DIR)/bin/python2.4 setup.py install --prefix=$(RUNTIME_DIR)
	-cd $(UNPACK_DIR)/numpy-$(NUMPY_VERSION); \
	for patch in $(PATCH_DIR)/numpy-$(NUMPY_VERSION)_$(ARCH)_*; \
		do patch -p1 < $$patch; \
	done
	# NB: DO NOT SET LDFLAGS. EVER. IT BREAKS THE BUILD
	cd $(UNPACK_DIR)/numpy-$(NUMPY_VERSION); export CPPFLAGS="-I$(RUNTIME_DIR)/include $$CPPFLAGS" CFLAGS="$$CFLAGS -I$(RUNTIME_DIR)/include -m64" FC="g95 -m64" FCFLAGS="$$FCFLAGS -m64" LD_LIBRARY_PATH=$(RUNTIME_DIR)/lib64:$(RUNTIME_DIR)/lib:$$LD_LIBRARY_PATH PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.4/site-packages/; $(RUNTIME_DIR)/bin/python2.4 setup.py build --fcompiler=gnu95; $(RUNTIME_DIR)/bin/python2.4 setup.py install --prefix=$(RUNTIME_DIR)
	touch $(NUMPY_TARGET)
endif

$(DOWNLOAD_DIR)/$(NUMPY_PACKAGE): $(INIT_TARGET)
	for package in $(NUMPY_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(NUMPY_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(NUMPY_PACKAGE)
