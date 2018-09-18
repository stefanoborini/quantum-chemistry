LIBPNG_VERSION=1.2.40
LIBPNG_TARGET=$(BUILD_FLAGS_DIR)/libpng
LIBPNG_PACKAGE=libpng-$(LIBPNG_VERSION).tar.gz
LIBPNG_PACKAGE_URL=http://surfnet.dl.sourceforge.net/sourceforge/libpng/$(LIBPNG_PACKAGE)

.PHONY: libpng libpng-download
libpng: $(LIBPNG_TARGET)
libpng-download: $(DOWNLOAD_DIR)/$(LIBPNG_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)
$(LIBPNG_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(LIBPNG_PACKAGE)
	touch $(LIBPNG_TARGET)
endif

ifeq ($(ARCH),x86_64-redhat-linux)
$(LIBPNG_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(LIBPNG_PACKAGE)
	-rm -rf $(UNPACK_DIR)/libpng-$(LIBPNG_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(LIBPNG_PACKAGE)
	cd $(UNPACK_DIR)/libpng-$(LIBPNG_VERSION); export CC="gcc -m64" FC="g95 -m64" CFLAGS="$$CFLAGS -m64" LDFLAGS="-L$(RUNTIME_DIR)/lib64 -L$(RUNTIME_DIR)/lib -m64 $$LDFLAGS" LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib64:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin:$$PATH; ./configure --prefix=$(RUNTIME_DIR); make -j 2; make install
	touch $(LIBPNG_TARGET)
endif

$(DOWNLOAD_DIR)/$(LIBPNG_PACKAGE): $(INIT_TARGET)
	for package in $(LIBPNG_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(LIBPNG_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(LIBPNG_PACKAGE)


