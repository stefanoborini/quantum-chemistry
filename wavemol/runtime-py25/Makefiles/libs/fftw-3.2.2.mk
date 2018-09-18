FFTW_VERSION=3.2.2
FFTW_TARGET=$(BUILD_FLAGS_DIR)/fftw
FFTW_PACKAGE=fftw-$(FFTW_VERSION).tar.gz
FFTW_PACKAGE_URL=ftp://ftp.fftw.org/pub/fftw/$(FFTW_PACKAGE)

.PHONY: fftw fftw-download
fftw: $(FFTW_TARGET)
fftw-download: $(DOWNLOAD_DIR)/$(FFTW_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)

$(FFTW_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(FFTW_PACKAGE)
	-rm -rf $(UNPACK_DIR)/fftw-$(FFTW_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(FFTW_PACKAGE)
	#-cd $(UNPACK_DIR)/fftw-$(FFTW_VERSION); export PATH=$(RUNTIME_DIR)/bin/:$$PATH; ./configure CC="gcc -arch i386 -arch x86_64" CXX="g++ -arch i386 -arch x86_64" CPP="gcc -E" CXXCPP="g++ -E" --prefix=$(RUNTIME_DIR); make; make install
	cd $(UNPACK_DIR)/fftw-$(FFTW_VERSION); export PATH=$(RUNTIME_DIR)/bin/:$$PATH; ./configure --prefix=$(RUNTIME_DIR)
	cd $(UNPACK_DIR)/fftw-$(FFTW_VERSION); export PATH=$(RUNTIME_DIR)/bin/:$$PATH; make -j2 && make install
	touch $(FFTW_TARGET)
endif

ifeq ($(ARCH),x86_64-redhat-linux)

$(FFTW_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(FFTW_PACKAGE)
	-rm -rf $(UNPACK_DIR)/fftw-$(FFTW_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(FFTW_PACKAGE)
	cd $(UNPACK_DIR)/fftw-$(FFTW_VERSION); export CC="gcc -m64" FC="g95 -m64" LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin/:$$PATH; ./configure --prefix=$(RUNTIME_DIR)
	cd $(UNPACK_DIR)/fftw-$(FFTW_VERSION); export CC="gcc -m64" FC="g95 -m64" LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin/:$$PATH; make -j2 && make install
	touch $(FFTW_TARGET)
endif

$(DOWNLOAD_DIR)/$(FFTW_PACKAGE): $(INIT_TARGET)
	for package in $(FFTW_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@


ALL_RUNTIME_TARGETS+=$(FFTW_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(FFTW_PACKAGE)

