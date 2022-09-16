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
ECHO          := echo
CP            := cp

ROBOT_XUNIT   = $(ROBOTDIR)/report.xml
ITEST_PLAN    = $(OUTDIR)/itest_plan.rst
LOG_FILE      = log.html
LAYER         ?= ""

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean:
	$(RM) $(BUILDDIR)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.
html: Makefile
	@$(RM) $(ROBOT_XUNIT)
	@$(RM) $(ITEST_PLAN)
	-@$(ROBOT) --xunit report.xml -d $(ROBOTDIR) $(ROBOTDIR)/example.robot
	@$(XUNIT2RST) -v
	@$(XUNIT2RST) -i $(ROBOT_XUNIT) -o $(OUTDIR)/itest_report.rst -p ITEST_- --trim-suffix -l ../$(LOG_FILE) --only $(LAYER) --links --failure-message
	@$(ROBOT2RST) --robot $(ROBOTDIR)/example.robot --rst $(ITEST_PLAN) --tags ^RQT-$
	@$(ECHO) -n $(LOG_FILE) | xargs -d ' ' -n 1 -I {} $(CP) $(ROBOTDIR)/{} $(OUTDIR)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
