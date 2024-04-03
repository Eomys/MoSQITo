# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

sphinx/html: links-stamp apidoc-stamp images-stamp rec-build-stamp

links-stamp:
	bin/ln-sphinx-subprojects
	touch $@

apidoc: apidoc-stamp
apidoc-stamp: links-stamp
	$(SPHINXAPIDOC) \
		--implicit-namespaces \
		--templatedir=../swh/docs/templates/ \
		--maxdepth=3 \
		$(APIDOC_OPTS) \
		-o $(APIDOC_DIR) \
		$(SWHPKGDIR) \
		$(APIDOC_SWH_EXCLUDES)
	touch $@

	images-stamp:
	$(MAKE) -C images
	$(MAKE) -C swh-deposit/images
	touch $@

# Build documentation recursively in all packages, to make sure that auxiliary,
# non-sphinx managed documentation artifacts (e.g., schema diagrams) are also
# built.
rec-build-stamp: $(wildcard ../../swh-*/docs/*.rst)
	$(MAKE) -C ../../ docs-assets
	touch $@

clean: sphinx/clean
	bin/ln-sphinx-subprojects --remove
	$(MAKE) -C images clean
	rm -f *-stamp
	rm -f $(APIDOC_DIR)/*

distclean: clean
	make -C ../../ docs-clean

help: sphinx/help

sphinx/clean:
	$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

sphinx/%:
	$(SPHINXBUILD) -b $* "$(SOURCEDIR)" "$(BUILDDIR)/$*" $(SPHINXOPTS)

install: html
	test -d $(HTMLDIR)
	rsync -rlvuz --delete $(BUILDDIR)/html/ $(INSTALL_HOST):$(INSTALL_DIR)/
	ssh $(INSTALL_HOST) \
		"find $(INSTALL_DIR) -not -group $(INSTALL_GROUP) -exec chgrp -v $(INSTALL_GROUP) {} + ; \
		 find $(INSTALL_DIR) -not -perm -ug=rw,o=r -exec chmod -v ug+rw,o+r {} + ; \
		 find $(INSTALL_DIR) -type d -not -perm -g=xs,ou=x -exec chmod -v g+xs,ou+x {} +"

.PHONY: help html clean distclean install images-stamp