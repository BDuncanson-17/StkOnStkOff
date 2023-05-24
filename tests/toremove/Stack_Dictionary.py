import stkonstkoff.UserAuthentication
import stkonstkoff.cloudformations.CloudFormationStacks as cft
import os

# Testing User Authorization

stk = stkonstkoff.UserAuthentication.UserAccess

cft(stk.session)
cft.current_stacks()
