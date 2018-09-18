GCC_VERSION=4.3.4
GCC_TARGET=$(BUILD_FLAGS_DIR)/gcc
GCC_CORE_PACKAGE=gcc-core-$(GCC_VERSION).tar.bz2      
GCC_CPLUSPLUS_PACKAGE=gcc-g++-$(GCC_VERSION).tar.bz2
GCC_OBJC_PACKAGE=gcc-objc-$(GCC_VERSION).tar.bz2
GCC_FORTRAN_PACKAGE=gcc-fortran-$(GCC_VERSION).tar.bz2

GCC_CORE_PACKAGE_URL=ftp://gcc.gnu.org/pub/gcc/releases/gcc-$(GCC_VERSION)/$(GCC_CORE_PACKAGE)
GCC_CPLUSPLUS_PACKAGE_URL=ftp://gcc.gnu.org/pub/gcc/releases/gcc-$(GCC_VERSION)/$(GCC_CPLUSPLUS_PACKAGE)
GCC_FORTRAN_PACKAGE_URL=ftp://gcc.gnu.org/pub/gcc/releases/gcc-$(GCC_VERSION)/$(GCC_FORTRAN_PACKAGE)
GCC_OBJC_PACKAGE_URL=ftp://gcc.gnu.org/pub/gcc/releases/gcc-$(GCC_VERSION)/$(GCC_OBJC_PACKAGE)

gcc: $(GCC_TARGET)
gcc-download: $(DOWNLOAD_DIR)/$(GCC_CORE_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_CPLUSPLUS_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_FORTRAN_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_OBJC_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)

$(GCC_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(GCC_CORE_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_CPLUSPLUS_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_FORTRAN_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_OBJC_PACKAGE)
	-rm -rf $(UNPACK_DIR)/gcc-$(GCC_VERSION)
	
	tar -m -C $(UNPACK_DIR) -xjvf $(DOWNLOAD_DIR)/$(GCC_CORE_PACKAGE)
	tar -m -C $(UNPACK_DIR) -xjvf $(DOWNLOAD_DIR)/$(GCC_CPLUSPLUS_PACKAGE)
	tar -m -C $(UNPACK_DIR) -xjvf $(DOWNLOAD_DIR)/$(GCC_OBJC_PACKAGE)
	tar -m -C $(UNPACK_DIR) -xjvf $(DOWNLOAD_DIR)/$(GCC_FORTRAN_PACKAGE)
	-cd $(UNPACK_DIR)/gcc-$(GCC_VERSION); \
	for patch in $(PATCH_DIR)/gcc-$(GCC_VERSION)_$(ARCH)_*; \
		do patch -p1 < $$patch; \
	done
	mkdir $(UNPACK_DIR)/gcc-$(GCC_VERSION)/g95/
	cd $(UNPACK_DIR)/gcc-$(GCC_VERSION)/g95/; export CC="gcc -m64" CFLAGS="-m64"; ../configure --with-mpfr=$(RUNTIME_DIR) --with-gmp=$(RUNTIME_DIR) --prefix=$(RUNTIME_DIR) --host=x86_64-apple-darwin10 --build=x86_64-apple-darwin10 --target=x86_64-apple-darwin10 --disable-multilib --enable-languages=c,c++,fortran,objc
	cd $(UNPACK_DIR)/gcc-$(GCC_VERSION)/g95/; export CC="gcc -m64" CFLAGS='-m64' LDFLAGS="-L$(RUNTIME_DIR)/lib:$(LDFLAGS)" CPPFLAGS="-I$(RUNTIME_DIR)/include:$(CPPFLAGS)" PATH=$(RUNTIME_DIR)/bin:$$PATH; make -j 2
	cd $(UNPACK_DIR)/gcc-$(GCC_VERSION)/g95/; make install
	cd $(RUNTIME_DIR)/bin/ && ln -sf gfortran g77
	cd $(RUNTIME_DIR)/bin/ && ln -sf gfortran g95
	touch $(GCC_TARGET)
endif

ifeq ($(ARCH),x86_64-redhat-linux)

$(GCC_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(GCC_CORE_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_CPLUSPLUS_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_FORTRAN_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_OBJC_PACKAGE)
	-rm -rf $(UNPACK_DIR)/gcc-$(GCC_VERSION)
	tar -m -C $(UNPACK_DIR) -xjvf $(DOWNLOAD_DIR)/$(GCC_CORE_PACKAGE)
	tar -m -C $(UNPACK_DIR) -xjvf $(DOWNLOAD_DIR)/$(GCC_CPLUSPLUS_PACKAGE)
	tar -m -C $(UNPACK_DIR) -xjvf $(DOWNLOAD_DIR)/$(GCC_OBJC_PACKAGE)
	tar -m -C $(UNPACK_DIR) -xjvf $(DOWNLOAD_DIR)/$(GCC_FORTRAN_PACKAGE)
	mkdir $(UNPACK_DIR)/gcc-$(GCC_VERSION)/g95/
	cd $(UNPACK_DIR)/gcc-$(GCC_VERSION)/g95/; ../configure --with-mpfr=$(RUNTIME_DIR) --with-gmp=$(RUNTIME_DIR) --prefix=$(RUNTIME_DIR) --host=x86_64-redhat-linux --build=x86_64-redhat-linux --target=x86_64-redhat-linux --enable-languages=c,c++,fortran,objc
	cd $(UNPACK_DIR)/gcc-$(GCC_VERSION)/g95/; export LD_LIBRARY_PATH="$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib" LDFLAGS="-L$(RUNTIME_DIR)/lib:$(LDFLAGS)" CPPFLAGS="-I$(RUNTIME_DIR)/include:$(CPPFLAGS)" PATH=$(RUNTIME_DIR)/bin:$$PATH; make -j 2
	cd $(UNPACK_DIR)/gcc-$(GCC_VERSION)/g95/; make install
	cd $(RUNTIME_DIR)/bin/ && ln -sf gfortran g77
	cd $(RUNTIME_DIR)/bin/ && ln -sf gfortran g95
	touch $(GCC_TARGET)
endif

$(DOWNLOAD_DIR)/$(GCC_CORE_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_CPLUSPLUS_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_FORTRAN_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_OBJC_PACKAGE): $(INIT_TARGET)
	for package in $(GCC_CORE_PACKAGE_URL) $(GCC_CPLUSPLUS_PACKAGE_URL) $(GCC_FORTRAN_PACKAGE_URL) $(GCC_OBJC_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@
	
ALL_RUNTIME_TARGETS+=$(GCC_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(GCC_CORE_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_CPLUSPLUS_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_FORTRAN_PACKAGE) $(DOWNLOAD_DIR)/$(GCC_OBJC_PACKAGE)

