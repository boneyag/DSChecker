#!/bin/bash

for f in [0-9]*.py; do
    num=$(echo "$f" | grep -o '^[0-9]\+')
    rest=${f#${num}_}
    cf="${num}c_${rest}"
    if [[ -f "$cf" ]]; then
        out="../dl_patches/${num}_${rest%.py}_patch.txt"
        diff "$f" "$cf" > "$out"
        echo "Created $out"
    fi
done
