import stkonstkoff.UserAuthentication
import tests.toremove.CloudFormationStacks as cft

# Testing User Authorization

stk = stkonstkoff.UserAuthentication.UserAccess

cft(stk.session)
cft.current_stacks()
