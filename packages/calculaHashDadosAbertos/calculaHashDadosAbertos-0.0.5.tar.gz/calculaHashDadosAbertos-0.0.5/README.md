# calculaHashDadosAbertos
The library can calculate hash files from dados abertos website in MD5 format.
So far it works with chamber of deputies data.
Example of PyPI package.
## Getting Started
#### Dependencies
You need Python 3.7 or later to use **calculaHashDadosAbertos**. You can find it at [python.org](https://www.python.org/).

```
Maybe you should need to import some of those libraries
import requests
import pandas as pd
from pandas.io.json import json_normalize
from datetime import date
import json
import io
import hashlib, os, sys
import shutil
```
#### Installation
Clone this repo to your local machine using:
```
git clone https://github.com/masuta16/calculaHash.git
```
## Features
This function example returns a csv file with HashMD5 from dados abertos website using API v2
Con3Prop function returns values with 3 input propositions on government and the fourth input is the number of days until today
and HashMD5Camara method returns the csv file
```
from calculaHashDadosAbertos import CalculaHashCamara
CalculaHashCamara.Con3Prop('PLP','PEC','PL', 3).HashMD5Camara
```
This function example returns a csv file with HashMD5 from dados abertos website using API v2 too
Con2Prop function returns values with 2 input propositions on government the third input is the number of days until today
```
from calculaHashDadosAbertos import CalculaHashCamara
CalculaHashCamara.Con2Prop('PLP','PEC', 3).HashMD5Camara
```
This function example returns a csv file with HashMD5 from dados abertos website using API v2 too
Con1Prop function returns values with only 1 input propositions on government the second input is the number of days until today
```
from calculaHashDadosAbertos import CalculaHashCamara
CalculaHashCamara.Con2Prop('PLP', 3).HashMD5Camara
```
diferenca1Prop function returns a string with the url with data consulting on dados abertos website with one input data
diferenca2Prop function returns -------------------------------------------------------------------with two input data
diferenca3Prop function returns ----- with three input data

```
from calculaHashDadosAbertos import CalculaHashCamara
CalculaHashCamara.Con1Prop('PLP', 3).diferenca1Prop
```