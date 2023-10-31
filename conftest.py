import logging
import os

# set the DEBUG environ variable to enable verbose logging
if "DEBUG" in os.environ:
    logging.basicConfig()
    logging.getLogger("ravenpack").setLevel(logging.DEBUG)
