ifeq ($(ARCH),x86_64-apple-darwin10)

.PHONY: gfortran gfortran-download

GFORTRAN_VERSION=4.2.3
GFORTRAN_TARGET=/usr/local/bin/gfortran-4.2
GFORTRAN_PACKAGE=gfortran-$(GFORTRAN_VERSION).dmg
GFORTRAN_PACKAGE_URL=http://r.research.att.com/$(GFORTRAN_PACKAGE)

gfortran: $(GFORTRAN_TARGET)
gfortran-download: $(DOWNLOAD_DIR)/$(GFORTRAN_PACKAGE)

$(GFORTRAN_TARGET): $(INIT_TARGET) $(GFORTRAN_DEPS) $(DOWNLOAD_DIR)/$(GFORTRAN_PACKAGE) 
	cd $(DOWNLOAD_DIR); hdiutil attach $(GFORTRAN_PACKAGE)
	cd "/Volumes/GNU Fortran $(GFORTRAN_VERSION)/"; sudo installer -pkg gfortran.pkg -target "/"
	@echo "waiting for unmount"
	@sleep 5
	hdiutil detach "/Volumes/GNU Fortran $(GFORTRAN_VERSION)/"
	sudo touch $(GFORTRAN_TARGET)

$(DOWNLOAD_DIR)/$(GFORTRAN_PACKAGE): $(INIT_TARGET)
	for package in $(GFORTRAN_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(GFORTRAN_TARGET) 
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(GFORTRAN_PACKAGE)

else
GFORTRAN_VERSION=4.2.3
GFORTRAN_TARGET=$(BUILD_FLAGS_DIR)/gfortran
GFORTRAN_PACKAGE=gfortran-$(GFORTRAN_VERSION).dmg
GFORTRAN_PACKAGE_URL=http://r.research.att.com/$(GFORTRAN_PACKAGE)

gfortran: $(GFORTRAN_TARGET)
gfortran-download: $(DOWNLOAD_DIR)/$(GFORTRAN_PACKAGE)

$(GFORTRAN_TARGET): $(INIT_TARGET) $(GFORTRAN_DEPS) $(DOWNLOAD_DIR)/$(GFORTRAN_PACKAGE) 
	@echo "unsupported platform for gfortran $(ARCH)"
	@false

$(DOWNLOAD_DIR)/$(GFORTRAN_PACKAGE): $(INIT_TARGET)
	@echo "unsupported platform for gfortran $(ARCH)"
	@false

ALL_RUNTIME_TARGETS+=$(GFORTRAN_TARGET) 
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(GFORTRAN_PACKAGE)
endif

