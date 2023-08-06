# saptools

Python SAP integration. 


## VBS Conversion

SAPConverter.py takes SAP GUI scripts and converts to drag and drop py.


Usage:

```
from saptools import sap_converter

sap_converter.convert_file(Document="myVBSscript.vbs", out_file="converted.py")
```



## Connection to SAP

saptools.py handles the connection to SAP.

Connection defaults to session 0.

To connect to other sessions of SAP send session number as Argument:

```
from saptools import saptools


# Session 0
session = saptools.SAP_connect()

# Session 1
session = saptools.SAP_connect()(1)
```