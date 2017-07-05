# smart-moskito
A very simple and handful Web Picture Viewer

This aims at quickly deploy a simple HTTP server exposing a photos gallery. To
achieve this goal, Moskito does not need any database: it only needs the path
to the root folder of all the pictures you want to expose. Sub-folders will be
exposed as albums.

## Installation

Required tools: python 3, yarn
Required libs: libmagick++-dev

```
yarn install --modules-folder moskito/static/node_modules
```


## Running moskito

```
git clone 
FLASK_APP=moskito FLASK_DEBUG=true flask run
```
