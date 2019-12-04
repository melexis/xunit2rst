# Makefile for building example of robot2rst output in Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build
PYTHON		  = python3
XUNIT2RST     = $(PYTHON) -m mlx.xunit2rst
ROBOT2RST	  = $(PYTHON) -m mlx.robot2rst
ROBOT         = $(PYTHON) -m robot

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	-@$(ROBOT) --xunit source/input/report.xml -d source/robot/ source/robot/example.robot
	@$(XUNIT2RST) -v
	@$(XUNIT2RST) -i source/input/report.xml -o source/itest_report.rst -p ITEST_- --trim-suffix
	@$(ROBOT2RST) --robot source/robot/example.robot --rst source/itest_plan.rst --tags ^RQT-$
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
