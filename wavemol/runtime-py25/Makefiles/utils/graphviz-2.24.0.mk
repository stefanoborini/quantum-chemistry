GRAPHVIZ_VERSION=2.24.0
GRAPHVIZ_TARGET=$(BUILD_FLAGS_DIR)/graphviz
GRAPHVIZ_PACKAGE=graphviz-$(GRAPHVIZ_VERSION).tar.gz
GRAPHVIZ_PACKAGE_URL=http://www.graphviz.org/pub/graphviz/stable/SOURCES/$(GRAPHVIZ_PACKAGE)

graphviz: $(GRAPHVIZ_TARGET)
graphviz-download: $(DOWNLOAD_DIR)/$(GRAPHVIZ_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)
$(GRAPHVIZ_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(GRAPHVIZ_PACKAGE) 
	-rm -rf $(UNPACK_DIR)/graphviz-$(GRAPHVIZ_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(GRAPHVIZ_PACKAGE)
	cd $(UNPACK_DIR)/graphviz-$(GRAPHVIZ_VERSION); export PATH=$(RUNTIME_DIR)/bin:$$PATH; $(UNPACK_DIR)/graphviz-$(GRAPHVIZ_VERSION)/configure --prefix=$(RUNTIME_DIR) --disable-swig --disable-sharp --disable-guile    --disable-java --disable-lua --disable-ocaml   --disable-perl     --disable-php    --disable-python  --disable-python23 --disable-python24 --disable-python25 --disable-python26 --disable-r      --disable-ruby --disable-tcl; make -j 2; make install
	touch $(GRAPHVIZ_TARGET)
endif


ifeq ($(ARCH),x86_64-redhat-linux)
$(GRAPHVIZ_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(GRAPHVIZ_PACKAGE) 
	-rm -rf $(UNPACK_DIR)/graphviz-$(GRAPHVIZ_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(GRAPHVIZ_PACKAGE)
	cd $(UNPACK_DIR)/graphviz-$(GRAPHVIZ_VERSION); export CC="gcc -m64" FC="g95 -m64" CFLAGS="$$CFLAGS -m64 -I$(INCLUDES)" CPPFLAGS="$$CPPFLAGS -I$(INCLUDES)" LDFLAGS="-L$(RUNTIME_DIR)/lib64 -L$(RUNTIME_DIR)/lib -m64 $$LDFLAGS" LD_LIBRARY_PATH=$(RUNTIME_DIR)/lib64:$(RUNTIME_DIR)/lib:$$LD_LIBRARY_PATH PATH=$(RUNTIME_DIR)/bin:$$PATH; $(UNPACK_DIR)/graphviz-$(GRAPHVIZ_VERSION)/configure --prefix=$(RUNTIME_DIR); make -j 2; make install
	touch $(GRAPHVIZ_TARGET)
endif


$(DOWNLOAD_DIR)/$(GRAPHVIZ_PACKAGE): $(INIT_TARGET)
	for package in $(GRAPHVIZ_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(GRAPHVIZ_TARGET) 
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(GRAPHVIZ_PACKAGE)

