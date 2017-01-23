#!/bin/bash

date=`date "+%Y%m%d-%H%M%S"`

extention=.png

~/dropbox/Dropbox-Uploader/dropbox_uploader.sh upload ./test.png IntelMap_$date$extention

exit 0
