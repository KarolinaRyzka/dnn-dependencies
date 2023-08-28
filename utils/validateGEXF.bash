#!/bin/bash

helpMessage="Run ./validateGEXF.bash -h for command line arguments"

source ./optparse.bash

optparse.define short=f long=gexf-file desc="GEXF file to validate" variable=file

source $( optparse.build )

if [ -z $file ]
then
    echo "No input for -f | --gexf-file"
    echo $helpMessage
    exit 1
fi

wget -nc https://gexf.net/1.2/gexf.xsd
wget -nc https://gexf.net/1.2/data.xsd
wget -nc https://gexf.net/1.2/dynamics.xsd
wget -nc https://gexf.net/1.2/hierarchy.xsd
wget -nc https://gexf.net/1.2/phylogenics.xsd
wget -nc https://gexf.net/1.2/viz.xsd

xmllint --noout --schema gexf.xsd $file
