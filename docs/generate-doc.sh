#!/bin/sh

set -eu

err(){
    echo "error: $@"
    exit 1
}

# We assume
#   /path/to/package_name
#   ├── doc                     # <-- here
#   │   ├── generate-doc.sh
#   │   ├── Makefile
#   │   └── source
#   │       ├── conf.py
#   │       ├── _static
#   │       └── _templates
#   ├── setup.py
#   ...

# /path/to/package_name
package_dir=$(readlink -f ../)

# package_name
package_name=$(basename $package_dir)

# /path/to/package_name/source/index.rst
main_index_file=source/index.rst

##autodoc_extra_opts=--write-doc
autodoc_extra_opts=

autodoc=sphinx-autodoc
which $autodoc > /dev/null 2>&1 || err "executable $autodoc not found"

# ensure a clean generated tree, "make clean" only removes build/
rm -rf $(find $package_dir -name "*.pyc" -o -name "__pycache__")
rm -rf build/ source/generated/

# If main index doesn't exist, generate, else don't touch it, even though
# sphinx-autodoc's -i option creates a backup before overwriting, it
# would still be annoying. Thus use -i once to create an initial
# source/index.rst which can then be tweaked.
[ -f $main_index_file ] || autodoc_extra_opts="$autodoc_extra_opts -i"

# generate API doc rst files
$autodoc $autodoc_extra_opts -s source -a generated/api \
    -X 'test[s]*\.test_' $package_name

make html