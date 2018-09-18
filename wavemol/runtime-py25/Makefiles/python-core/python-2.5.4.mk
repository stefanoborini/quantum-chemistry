PYTHON_VERSION=2.5.4
PYTHON_TARGET=$(BUILD_FLAGS_DIR)/python
PYTHON_PACKAGE=Python-$(PYTHON_VERSION).tar.bz2
PYTHON_PACKAGE_URL=http://www.python.org/ftp/python/$(PYTHON_VERSION)/$(PYTHON_PACKAGE)

python25: $(PYTHON_TARGET)
python25-download: $(DOWNLOAD_DIR)/$(PYTHON_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)
$(PYTHON_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(PYTHON_PACKAGE) 
	-rm -rf $(UNPACK_DIR)/Python-$(PYTHON_VERSION)
	tar -m -C $(UNPACK_DIR) -xjvf $(DOWNLOAD_DIR)/$(PYTHON_PACKAGE)
	-cd $(UNPACK_DIR)/Python-$(PYTHON_VERSION); \
	for patch in $(PATCH_DIR)/Python-$(PYTHON_VERSION)_$(ARCH)_*; \
		do patch -p1 < $$patch; \
	done
	A=`echo "$(RUNTIME_DIR)"|sed "s/\//\\\\\\\\\//g"`; \
	  cd $(UNPACK_DIR)/Python-$(PYTHON_VERSION); \
	  cat Lib/cgi.py | sed "s/__PREFIX__/$$A/g" >Lib/cgi.py.new; \
	  cat Lib/site.py | sed "s/__PREFIX__/$$A/g" >Lib/site.py.new; \
	  cat setup.py | sed "s/__PREFIX__/$$A/g" >setup.py.new; \
	  cp Lib/cgi.py.new Lib/cgi.py; \
	  cp Lib/site.py.new Lib/site.py; \
	  cp setup.py.new setup.py; \
	  cat Mac/Makefile.in | sed "s/__FRAMEWORKS_DIR__/$$A/g" >Mac/Makefile.in.new; \
	  cp Mac/Makefile.in.new  Mac/Makefile.in; \
	  cat Mac/IDLE/Makefile.in  | sed "s/__APPLICATIONS_DIR__/$$A/g" >Mac/IDLE/Makefile.in.new; \
	  cat Mac/Makefile.in  | sed "s/__APPLICATIONS_DIR__/$$A/g" >Mac/Makefile.in.new; \
	  cat Mac/PythonLauncher/Makefile.in  | sed "s/__APPLICATIONS_DIR__/$$A/g" >Mac/PythonLauncher/Makefile.in.new; \
	  cp Mac/IDLE/Makefile.in.new Mac/IDLE/Makefile.in; \
	  cp Mac/Makefile.in.new Mac/Makefile.in; \
	  cp Mac/PythonLauncher/Makefile.in.new Mac/PythonLauncher/Makefile.in
	cd $(UNPACK_DIR)/Python-$(PYTHON_VERSION); export PATH=$(RUNTIME_DIR)/bin:$$PATH; $(UNPACK_DIR)/Python-$(PYTHON_VERSION)/configure --enable-shared --disable-tk --enable-ipv6  --disable-toolbox-glue --prefix=$(RUNTIME_DIR) MACOSX_DEPLOYMENT_TARGET=10.6 
	cd $(UNPACK_DIR)/Python-$(PYTHON_VERSION); ed - pyconfig.h < $(PATCH_DIR)/pyconfig-2.5.4_x86_64-apple-darwin10.ed
	cd $(UNPACK_DIR)/Python-$(PYTHON_VERSION); echo "#undef _POSIX_C_SOURCE" >>pyconfig.h 
	cd $(UNPACK_DIR)/Python-$(PYTHON_VERSION); echo "#undef _XOPEN_SOURCE" >>pyconfig.h 
	cd $(UNPACK_DIR)/Python-$(PYTHON_VERSION); echo "#define HAVE_BROKEN_POSIX_SEMAPHORES" >>pyconfig.h 
	cd $(UNPACK_DIR)/Python-$(PYTHON_VERSION); export PATH=$(RUNTIME_DIR)/bin:$$PATH CPPFLAGS="$$CPPFLAGS -D__DARWIN_UNIX03"; make -j 2 && make install
	touch $(PYTHON_TARGET)
endif

ifeq ($(ARCH),x86_64-redhat-linux)
$(PYTHON_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(PYTHON_PACKAGE) 
	-rm -rf $(UNPACK_DIR)/Python-$(PYTHON_VERSION)
	tar -m -C $(UNPACK_DIR) -xjvf $(DOWNLOAD_DIR)/$(PYTHON_PACKAGE)
	cd $(UNPACK_DIR)/Python-$(PYTHON_VERSION); export CC="gcc -m64" FC="g95 -m64" CFLAGS="$$CFLAGS -m64" LDFLAGS="$$LDFLAGS -m64" LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin:$$PATH; $(UNPACK_DIR)/Python-$(PYTHON_VERSION)/configure --enable-shared --disable-tk --enable-ipv6 --disable-toolbox-glue --prefix=$(RUNTIME_DIR)
	cd $(UNPACK_DIR)/Python-$(PYTHON_VERSION); export CC="gcc -m64" FC="g95 -m64" CFLAGS="$$CFLAGS -m64" LDFLAGS="$$LDFLAGS -m64" LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin:$$PATH; make -j 2 && make install
	touch $(PYTHON_TARGET)
endif

$(DOWNLOAD_DIR)/$(PYTHON_PACKAGE): $(INIT_TARGET)
	for package in $(PYTHON_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(PYTHON_TARGET) 
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(PYTHON_PACKAGE)

