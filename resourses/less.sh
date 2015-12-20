#!/bin/bash

lessc less/bootstrap.less css/bootstrap.css
yui-compressor -o css/bootstrap.min.css css/bootstrap.css
cp css/bootstrap.min.css ../bmd/static/css/
