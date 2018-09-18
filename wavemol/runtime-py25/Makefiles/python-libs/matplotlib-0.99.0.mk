MATPLOTLIB_VERSION=0.99.1.2
MATPLOTLIB_TARGET=$(BUILD_FLAGS_DIR)/matplotlib
MATPLOTLIB_PACKAGE=matplotlib-$(MATPLOTLIB_VERSION).tar.gz
MATPLOTLIB_PACKAGE_URL=http://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-0.99.1/matplotlib-0.99.1.2.tar.gz

.PHONY: matplotlib matplotlib-download
matplotlib: $(MATPLOTLIB_TARGET)
matplotlib-download: $(DOWNLOAD_DIR)/$(MATPLOTLIB_PACKAGE)

ifeq ($(ARCH),x86_64-apple-darwin10)
$(MATPLOTLIB_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(MATPLOTLIB_PACKAGE)
	-rm -rf $(UNPACK_DIR)/matplotlib-$(MATPLOTLIB_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(MATPLOTLIB_PACKAGE)
	mv $(UNPACK_DIR)/matplotlib-0.99.1.1 $(UNPACK_DIR)/matplotlib-$(MATPLOTLIB_VERSION);
	cd $(UNPACK_DIR)/matplotlib-$(MATPLOTLIB_VERSION); \
	echo "[egg_info]"  >>./setup.cfg; \
	echo "tag_svn_revision = 1"  >>./setup.cfg; \
	echo "[status]"  >>./setup.cfg; \
	echo "[provide_packages]"  >>./setup.cfg; \
	echo "[gui_support]"  >>./setup.cfg; \
	echo "gtk = False"  >>./setup.cfg; \
	echo "gtkagg = False"  >>./setup.cfg; \
	echo "tkagg = False"  >>./setup.cfg; \
	echo "wxagg = False"  >>./setup.cfg; \
	echo "macosx = False" >>./setup.cfg; \
	echo "[rc_options]" >>./setup.cfg; \
	echo "backend = Pdf" >>./setup.cfg;
	cd $(UNPACK_DIR)/matplotlib-$(MATPLOTLIB_VERSION); export PATH=$(RUNTIME_DIR)/bin:$$PATH LDFLAGS="$(LIBS):$(LDFLAGS)" CPPFLAGS="$(INCLUDES) -I$(RUNTIME_DIR)/include/freetype2/ $(CPPFLAGS)" PYTHONPATH=$(RUNTIME_DIR)/lib/python2.5/site-packages/; $(RUNTIME_DIR)/bin/python2.5 setup.py install --prefix=$(RUNTIME_DIR)
	touch $(MATPLOTLIB_TARGET)
endif

ifeq ($(ARCH),x86_64-redhat-linux)
#$(MATPLOTLIB_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(MATPLOTLIB_PACKAGE)
#	-rm -rf $(UNPACK_DIR)/matplotlib-$(MATPLOTLIB_VERSION)
#	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(MATPLOTLIB_PACKAGE)
#	cd $(UNPACK_DIR)/matplotlib-$(MATPLOTLIB_VERSION); \
#	echo "[egg_info]"  >>./setup.cfg; \
#	echo "tag_svn_revision = 1"  >>./setup.cfg; \
#	echo "[status]"  >>./setup.cfg; \
#	echo "[provide_packages]"  >>./setup.cfg; \
#	echo "[gui_support]"  >>./setup.cfg; \
#	echo "gtk = False"  >>./setup.cfg; \
#	echo "gtkagg = False"  >>./setup.cfg; \
#	echo "tkagg = False"  >>./setup.cfg; \
#	echo "wxagg = False"  >>./setup.cfg; \
#	echo "macosx = False" >>./setup.cfg; \
#	echo "[rc_options]" >>./setup.cfg; \
#	echo "backend = Pdf" >>./setup.cfg;
#	cd $(UNPACK_DIR)/matplotlib-$(MATPLOTLIB_VERSION); export PKG_CONFIG_PATH=$(RUNTIME_DIR)/lib/pkgconfig/ LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(RUNTIME_DIR)/lib64:$(RUNTIME_DIR)/lib PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.4/site-packages/ CFLAGS="-I$(RUNTIME_DIR)/include $$CFLAGS"; $(RUNTIME_DIR)/bin/python2.4 setup.py install --prefix=$(RUNTIME_DIR)
#	touch $(MATPLOTLIB_TARGET)
endif

$(DOWNLOAD_DIR)/$(MATPLOTLIB_PACKAGE): $(INIT_TARGET)
	for package in $(MATPLOTLIB_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(MATPLOTLIB_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(MATPLOTLIB_PACKAGE)
