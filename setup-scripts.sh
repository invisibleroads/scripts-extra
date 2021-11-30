#!/bin/bash
cd $(dirname "$0")

SCRIPTS=~/.scripts
if [ ! -e $SCRIPTS ]; then
    mkdir $SCRIPTS
fi

for filename in .gvimrc
do
    cp $filename ~
    echo 'cp '$filename ~
done

for filename in boot-windows browse-photos clean-folders clean-notebooks clip-file disable-backlight disable-wakeup encrypt-password rank-sizes refresh-assets see-tree update-projects *.py
do
    cp $filename $SCRIPTS
    chmod a+x $SCRIPTS/$filename
    echo 'cp '$filename $SCRIPTS
done

mkdir ~/.config/bleachbit -p
cp bleachbit.ini ~/.config/bleachbit
