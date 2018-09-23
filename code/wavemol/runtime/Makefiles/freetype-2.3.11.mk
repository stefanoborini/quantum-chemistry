FREETYPE_VERSION=2.3.11
FREETYPE_TARGET=$(BUILD_FLAGS_DIR)/freetype
FREETYPE_PACKAGE=freetype-$(FREETYPE_VERSION).tar.gz
FREETYPE_PACKAGE_URL=http://surfnet.dl.sourceforge.net/sourceforge/freetype/$(FREETYPE_PACKAGE)

.PHONY: freetype freetype-download

freetype: $(FREETYPE_TARGET)
freetype-download: $(DOWNLOAD_DIR)/$(FREETYPE_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)
$(FREETYPE_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(FREETYPE_PACKAGE)
	-rm -rf $(UNPACK_DIR)/freetype-$(FREETYPE_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(FREETYPE_PACKAGE)
	cd $(UNPACK_DIR)/freetype-$(FREETYPE_VERSION); export LD_LIBRARY_PATH=$(RUNTIME_DIR)/lib:$$LD_LIBRARY_PATH PATH=$(RUNTIME_DIR)/bin:$(PATH); ./configure --prefix=$(RUNTIME_DIR); make; make install
	touch $(FREETYPE_TARGET)
endif

ifeq ($(ARCH),x86_64-redhat-linux)
$(FREETYPE_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(FREETYPE_PACKAGE)
	-rm -rf $(UNPACK_DIR)/freetype-$(FREETYPE_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(FREETYPE_PACKAGE)
	cd $(UNPACK_DIR)/freetype-$(FREETYPE_VERSION); export CC="gcc -m64" LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin:$(PATH); ./configure --prefix=$(RUNTIME_DIR); make; make install
	touch $(FREETYPE_TARGET)
endif



$(DOWNLOAD_DIR)/$(FREETYPE_PACKAGE): $(INIT_TARGET)
	for package in $(FREETYPE_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(FREETYPE_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(FREETYPE_PACKAGE)
# <<fold

