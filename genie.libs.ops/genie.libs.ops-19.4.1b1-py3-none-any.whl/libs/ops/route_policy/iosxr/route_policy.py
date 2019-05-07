''' 
RoutePolicy Genie Ops Object for IOSXR - CLI.
'''

# Genie
from genie.ops.base import Base

# iosxr show_rpl
from genie.libs.parser.iosxr.show_rpl import ShowRplRoutePolicy


class RoutePolicy(Base):
    '''RoutePolicy Genie Ops Object'''

    def learn(self):
        '''Learn RoutePolicy Ops'''

        self.add_leaf(cmd=ShowRplRoutePolicy,
                      src='[(?P<policy>.*)][description]',
                      dest='info[(?P<policy>.*)][description]')

        #####################################################################
        #                        Statements section
        #####################################################################

        # Place holder to make it more readable
        src = '[(?P<policy>.*)][statements][(?P<statements>.*)]'
        dest = 'info[(?P<policy>.*)][statements][(?P<statements>.*)]'

        #####################################################################
        #                        Section "conditions"
        #####################################################################

        self.add_leaf(cmd=ShowRplRoutePolicy,
                      src=src+'[conditions]',
                      dest=dest+'[conditions]')

        #####################################################################
        #                        Section "actions"
        #####################################################################

        self.add_leaf(cmd=ShowRplRoutePolicy,
                      src=src+'[actions]',
                      dest=dest+'[actions]')

        self.make(final_call=True)
