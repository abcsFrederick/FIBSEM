#!/bin/bash
if [ -f "/repo/$1.py" ]; then
  ln -sf /repo /tmp
  export LC_COLLATE=C  # for sort
  cd /input
  find . -type f -a \! -name ".dirlist.*" -printf '%p\0' |
    while read -d '' file; do
      a="$(lsof "${file}")" 
      if [[ "${#a}" -eq 0 ]]; then
        printf "%q\n" "${file}"
        # else
        #   printf "opened %q\n" "${file}"
      fi
    done > /snapshot/.dirlist.new
  cd /snapshot
  [[ -f  .dirlist.old ]] && {
    comm -13 <(sort .dirlist.old) <(sort .dirlist.new) |
    while read -r file; do
      /usr/local/bin/python /tmp/script.py "-m $1" "-i /input" "-o /output" "${file}"
    done
  }
  mv .dirlist.new .dirlist.old  
else
  echo "$1.py does not exist"
fi


[[ -f  /snapshot/.dirlist.new ]]
comm -13 <(sort /snapshot/.dirlist.new) <(sort /snapshot/.dirlist.old)