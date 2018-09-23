GMP_VERSION=4.2.4
GMP_TARGET=$(BUILD_FLAGS_DIR)/gmp
GMP_PACKAGE=gmp-$(GMP_VERSION).tar.bz2
GMP_PACKAGE_URL=ftp://ftp.gnu.org/gnu/gmp/$(GMP_PACKAGE)

gmp: $(GMP_TARGET)
gmp-download: $(DOWNLOAD_DIR)/$(GMP_PACKAGE)
	
$(GMP_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(GMP_PACKAGE) 
	-rm -rf $(UNPACK_DIR)/gmp-$(GMP_VERSION)
	
	tar -m -C $(UNPACK_DIR) -xjvf $(DOWNLOAD_DIR)/$(GMP_PACKAGE) 
	cd $(UNPACK_DIR)/gmp-$(GMP_VERSION)/; ./configure --prefix=$(RUNTIME_DIR) --enable-cxx 
	cd $(UNPACK_DIR)/gmp-$(GMP_VERSION)/; make -j2 && make install 
	touch $(GMP_TARGET)


$(DOWNLOAD_DIR)/$(GMP_PACKAGE): $(INIT_TARGET)
	cd $(DOWNLOAD_DIR); curl -L -O $(GMP_PACKAGE_URL)
	touch $@
	
ALL_RUNTIME_TARGETS+=$(GMP_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(GMP_PACKAGE)

