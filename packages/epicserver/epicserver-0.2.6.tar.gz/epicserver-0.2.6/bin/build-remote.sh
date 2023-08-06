#!/bin/bash

REMOTE_NAME=build

REMOTE_HOST=`hg path $REMOTE_NAME | cut -f 3 -d/`
REMOTE_PATH=`hg path $REMOTE_NAME | cut -f 4- -d/`


hg push $REMOTE_NAME
ssh $REMOTE_HOST -- \
    TMPDIR=\`mktemp -d\` \;\
    hg clone \$HOME/$REMOTE_PATH \$TMPDIR \;\
    cd \$TMPDIR \;\
    $@ \;\
    rm -rf \$TMPDIR \;
