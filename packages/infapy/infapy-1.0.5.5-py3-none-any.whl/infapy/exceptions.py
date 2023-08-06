import infapy
import sys
import traceback

# All exceptions should subclass from InfapyError in this module.
class InfapyError(Exception):
    """Base class for all infapy errors."""
    

# Will be called when we are providing an invalid region
class InvalidRegionError(InfapyError):
    def __init__(self, region):
    
        msg = (
            "The region '%s' is not a valid region \n"
            "Valid regions are: us, em, ap"
            % (region)
        )
        
        InfapyError.__init__(self,msg)

class DummyInfapyErrorWithNoMessage(InfapyError):
    pass

class ConfigFileReadError(InfapyError):
    def __init__(self, region):
        
        msg = (
            "Review documentation for config file format"
        )
        
        InfapyError.__init__(self,msg)

class CredentialFileReadError(InfapyError):
    def __init__(self, region):
        
        msg = (
            "Review documentation for config file format"
        )
        
        InfapyError.__init__(self,msg)

class LimitExceededError(InfapyError):
    def __init__(self, limit):
        
        msg = (
            "Limit provided exceeds max allowed: \n"  
            "Value Currently Provided: " + str(limit)
        )
        
        InfapyError.__init__(self,msg)
