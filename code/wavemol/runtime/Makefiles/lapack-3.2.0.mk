LAPACK_VERSION=3.2.0
LAPACK_TARGET=$(BUILD_FLAGS_DIR)/lapack
LAPACK_PACKAGE=lapack-$(LAPACK_VERSION).tgz
LAPACK_PACKAGE_URL=http://www.netlib.org/lapack/$(LAPACK_PACKAGE)

.PHONY: lapack lapack-download

lapack: $(LAPACK_TARGET)
lapack-download: $(DOWNLOAD_DIR)/$(LAPACK_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)
$(LAPACK_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(LAPACK_PACKAGE)
	# blas already present on OSX
	touch $(LAPACK_TARGET)
endif

ifeq ($(ARCH),x86_64-redhat-linux)
$(LAPACK_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(LAPACK_PACKAGE)
	-rm -rf $(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(LAPACK_PACKAGE)
	mv $(UNPACK_DIR)/lapack-3.2 $(UNPACK_DIR)/lapack-$(LAPACK_VERSION)
	#
	-cd $(UNPACK_DIR)/lapack-$(LAPACK_VERSION); \
	for patch in $(PATCH_DIR)/lapack-$(LAPACK_VERSION)_$(ARCH)_*; \
		do patch -p1 < $$patch; \
	done
	echo 'SHELL = /bin/sh' >$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'PLAT = _LINUX' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'FORTRAN  = g95 -m64' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'OPTS     = -fPIC' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'DRVOPTS  = $$(OPTS)' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'NOOPT    = -fPIC' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'LOADER   = g95 -m64' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'LOADOPTS =' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'TIMER    = INT_CPU_TIME' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'ARCH     = ar' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'ARCHFLAGS= cr' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'RANLIB   = ranlib' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'BLASLIB      = ../../blas$$(PLAT).a' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'XBLASLIB     =' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'LAPACKLIB    = lapack$$(PLAT).a' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'TMGLIB       = tmglib$$(PLAT).a' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'EIGSRCLIB    = eigsrc$$(PLAT).a' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	echo 'LINSRCLIB    = linsrc$$(PLAT).a' >>$(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/make.inc
	
	cd $(UNPACK_DIR)/lapack-$(LAPACK_VERSION); export LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin:$$PATH && make blaslib lapacklib tmglib
	cp $(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/blas_LINUX.a $(RUNTIME_DIR)/lib/libblas.a
	cp $(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/lapack_LINUX.a $(RUNTIME_DIR)/lib/liblapack.a
	cp $(UNPACK_DIR)/lapack-$(LAPACK_VERSION)/tmglib_LINUX.a $(RUNTIME_DIR)/lib/libtmglib.a
	touch $(LAPACK_TARGET)
endif

$(DOWNLOAD_DIR)/$(LAPACK_PACKAGE): $(INIT_TARGET)
	-mkdir $(DOWNLOAD_DIR)
	for package in $(LAPACK_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@
	
ALL_RUNTIME_TARGETS+=$(LAPACK_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(LAPACK_PACKAGE)

