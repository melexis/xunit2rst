# Makefile for building example of xunit2rst output in Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
ROBOTDIR      = $(SOURCEDIR)/robot
OUTDIR        = $(SOURCEDIR)/generated
BUILDDIR      = _build
PYTHON        = python3
XUNIT2RST     = $(PYTHON) -m mlx.xunit2rst
ROBOT2RST     = $(PYTHON) -m mlx.robot2rst
ROBOT         = $(PYTHON) -m robot
RM            := rm -rf
MKDIR         := mkdir -p

ROBOT_XUNIT = $(ROBOTDIR)/report.xml
ITEST_PLAN = $(OUTDIR)/itest_plan.rst

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	$(RM) $(BUILDDIR)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html: Makefile
	@$(RM) $(ROBOT_XUNIT)
	@$(RM) $(ITEST_PLAN)
	-@$(ROBOT) --xunit report.xml -d $(ROBOTDIR) $(ROBOTDIR)/example.robot
	@$(XUNIT2RST) -v
	@$(XUNIT2RST) -i $(ROBOT_XUNIT) -o $(OUTDIR)/itest_report.rst -p ITEST_- --trim-suffix
	@$(ROBOT2RST) --robot $(ROBOTDIR)/example.robot --rst $(ITEST_PLAN) --tags ^RQT-$
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
