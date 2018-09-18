READLINE_VERSION=5.2
READLINE_TARGET=$(BUILD_FLAGS_DIR)/readline
READLINE_PACKAGE=readline-$(READLINE_VERSION).tar.gz
READLINE_PACKAGE_URL=http://ftp.gnu.org/gnu/readline/$(READLINE_PACKAGE)

.PHONY: readline readline-download
readline: $(READLINE_TARGET)
readline-download: $(DOWNLOAD_DIR)/$(READLINE_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)
$(READLINE_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(READLINE_PACKAGE) 
	-rm -rf $(UNPACK_DIR)/readline-$(READLINE_VERSION)/
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(READLINE_PACKAGE)
	cd $(UNPACK_DIR)/readline-$(READLINE_VERSION); \
	for patch in $(PATCH_DIR)/readline-$(READLINE_VERSION)_$(ARCH)_*; \
		do patch -p1 < $$patch; \
	done
	cd $(UNPACK_DIR)/readline-$(READLINE_VERSION)/; export PATH=$(RUNTIME_DIR)/bin:$$PATH; ./configure --build=x86_64-apple-darwin10 --prefix=$(RUNTIME_DIR);
	cd $(UNPACK_DIR)/readline-$(READLINE_VERSION)/; export PATH=$(RUNTIME_DIR)/bin:$$PATH; make -j 2 && make install
	touch $(READLINE_TARGET)
endif

ifeq ($(ARCH),x86_64-redhat-linux)
$(READLINE_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(READLINE_PACKAGE) 
	-rm -rf $(UNPACK_DIR)/readline-$(READLINE_VERSION)/
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(READLINE_PACKAGE)
	cd $(UNPACK_DIR)/readline-$(READLINE_VERSION)/; export CC="gcc -m64" FC="g95 -m64" LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin:$$PATH; ./configure --prefix=$(RUNTIME_DIR);
	cd $(UNPACK_DIR)/readline-$(READLINE_VERSION)/; export CC="gcc -m64" FC="g95 -m64" LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin:$$PATH; make -j 2 && make install
	touch $(READLINE_TARGET)
endif

$(DOWNLOAD_DIR)/$(READLINE_PACKAGE): $(INIT_TARGET)
	for package in $(READLINE_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(READLINE_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(READLINE_PACKAGE)

