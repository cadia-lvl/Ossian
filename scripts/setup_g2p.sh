#!/bin/bash 

## Location of this script:-
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
OSSIAN=$SCRIPTPATH/../

rm -rf $OSSIAN/tools/g2p/ 

# Sequitur G2P
cd $OSSIAN/tools/
wget https://www-i6.informatik.rwth-aachen.de/web/Software/g2p-r1668-r3.tar.gz
tar xvf g2p-r1668-r3.tar.gz
rm -r g2p-r1668-r3.tar.gz
cd g2p

if [ `uname -s` == Darwin ] ; then
    # Patch to avoid compilation problems on Mac OS relating to tr1 libraries like this:
    #
    # In file included from ./Multigram.hh:33:
    # ./UnorderedMap.hh:26:10: fatal error: 'tr1/unordered_map' file not found
    # #include <tr1/unordered_map>     
    echo 'Apply patch to sequitur for compilation on Mac OS...'
    patch -p1 -d . < ../patch/sequitur_compilation.patch
fi

## Compile:
python setup.py install --prefix  $OSSIAN/tools

## Port all python files to python 3 syntax
# futurize -0 -w ./*.py
# futurize -0 -w ../lib/python3.5/site-packages/*.py
