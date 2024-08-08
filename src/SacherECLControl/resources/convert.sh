#!/bin/bash

# Convert .ui files to .py files
for ui in *.ui; do
    pyside6-uic --from-imports $ui > ../view/Ui_${ui%.*}.py
done

pyside6-rcc  ./resources.qrc -o ../view/resources_rc.py
