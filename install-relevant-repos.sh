#!/bin/bash

mkdir -p outside_repos
cd outside_repos

git clone https://github.com/illinois-or-research-analytics/network_evaluation.git
git clone https://github.com/illinois-or-research-analytics/network-analysis-code.git
git clone https://github.com/MinhyukPark/constrained-clustering             

cd constrained-clustering
./setup.sh
./easy_build_and_compile.sh
cp constrained_clustering ../
cd ../..