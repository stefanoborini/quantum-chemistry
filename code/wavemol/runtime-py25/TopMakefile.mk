include config.mk
# collects all the runtime targets one by one.
ALL_RUNTIME_TARGETS=
ALL_DOWNLOAD_TARGETS=

default: all

include Makefiles/init.mk
# compiler suite
include Makefiles/compiler/gmp-4.2.4.mk
include Makefiles/compiler/mpfr-2.3.1.mk
include Makefiles/compiler/gcc-4.3.4.mk
# support C libs
#include Makefiles/libpng-1.2.40.mk
#include Makefiles/freetype-2.3.11.mk
# python core
include Makefiles/python-core/python-2.5.4.mk
include Makefiles/python-core/setuptools-0.6c11.mk

#python-libs
#include Makefiles/python-libs/numpy-1.3.0.mk
#include Makefiles/python-libs/scipy-0.7.1.mk
#include Makefiles/python-libs/matplotlib-0.99.0.mk
include Makefiles/python-libs/simplejson-2.0.9.mk
include Makefiles/python-libs/quantities-0.6.0.mk
include Makefiles/python-libs/mysqldb-1.2.3c1.mk
include Makefiles/python-libs/django-1.1.1.mk
include Makefiles/python-libs/rdflib-2.4.2.mk
#include Makefiles/python-libs/surf-1.0.0.mk

#other
include Makefiles/utils/openbabel-2.2.3.mk
#include Makefiles/utils/graphviz-2.24.0.mk

clean:
	-rm -rf $(TMP_DIR) $(UNPACK_DIR)

all: $(ALL_RUNTIME_TARGETS)
download-all: $(ALL_DOWNLOAD_TARGETS)

distclean: clean
	-rm -rf $(RUNTIME_DIR)
packageclean: 
	-rm -rf $(DOWNLOAD_DIR)
