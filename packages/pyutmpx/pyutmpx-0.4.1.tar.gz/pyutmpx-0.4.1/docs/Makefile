# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.

PE            = pipenv run
SPHINXOPTS    =
SPHINXBUILD   = $(PE) sphinx-build
SPHINXWATCH   = $(PE) sphinx-autobuild
SPHINXPROJ    = textoutpc
SOURCEDIR     = .
BUILDDIR      = _build
WEBROOT       = hercule:pyutmpx

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Send the website content.

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Livehtml build.
livehtml:
	$(SPHINXWATCH) $(SPHINXOPTS) . $(BUILDDIR)/html \
		--ignore "**/.*.kate-swp"

.PHONY: livehtml

# Send the website content (Linux-only).
show: html
	find _build/html -type f -exec chmod 644 {} \;
	rsync -Prlt --delete _build/html/ "$(WEBROOT)"

.PHONY: show
