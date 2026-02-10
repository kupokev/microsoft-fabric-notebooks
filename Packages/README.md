# Packages

This folder contains code to various packages.

## Instruction

1. Download the folder of code for the package you want to build.
2. Feel free to modify the packages to however you want. A shoutout in your code would be appreciated. 
3. Build the package with the code below. 

```
python -m build
```

This will create a subfolder called "dist" with two files in it. You should be able to upload either file to a custom Environment in Microsoft Fabric under the "Libraries" > "Custom" section.

### fabric-logger-package
Usage:
```
database = "Logging"
table = "NotebookLogging"
eventhouse_uri = "https://<your-kusto-cluster>.kusto.fabric.microsoft.com"

# Log without trace
from fabric_logger import FabricLogger

logger = FabricLogger(eventhouse_uri, database, table)

logger.log("Warning", "There was an error")

logger.write_to_eventhouse()


# Log with trace
from fabric_logger import FabricLogger
import traceback

logger = FabricLogger(eventhouse_uri, database, table)

try:
    1 / 0  # This raises a ZeroDivisionError
except Exception as e:
    log("Warning", str(e), traceback.format_exc())

logger.write_to_eventhouse()
```


## Feedback
If you have any issues or feedback, feel free to send me an email. My information can be found on my profile. 