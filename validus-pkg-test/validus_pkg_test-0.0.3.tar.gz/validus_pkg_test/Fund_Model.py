import numpy as np
import pandas as pd

class Fund():
    
    def __init__(self,cashflows,functional_ccy,ccy_curves):
        """
        FundModel should take a data frame consisting of three different
        Cash flows one for USD,GBP and EUR along with a dates index
        
        also takes ccy curves used to convert values into functional ccy should make CCY curves on the same date.
        """

        self.cashflows = cashflows
        self.functional_ccy = functional_ccy
        self.ccy_curves = ccy_curves
        
    def IRR(self,CCY):
        """
        return the IRR for a given Cashflow CCY
        """
        return np.irr(self.cashflows[CCY])
    
    def totalCF(self, curves):
        """
        calculate total CF based on the CCY curves and Cash flows fed in 
        """
        self.functional_total = self.cashflows[self.functional_ccy]
        for i in list(self.cashflows.columns.values):
            if i == self.functional_ccy:
                #if functional ccy no need to convert
                continue
            else:
                #create a CCY pair and check which way round it is and 
                # if rate needs to be inverted
                pair = i + self.functional_ccy
                if pair in list(self.ccy_curves.columns.values):
                    curve = curves[pair]

                else:
                    pair =  self.functional_ccy + i 
                    curve = 1/curves[pair]
             # sum up the total CFs      
            self.functional_total = self.functional_total + (self.cashflows[i].astype(float) * curve[0:len(self.cashflows[i])].values )
        return self.functional_total
    
    
    def scenario_analysis(self,scenario):
        """
        take a vector of volatilities for the given time vector and each CCY pair
        """

        ##store stressed curves
        stressed_curves = [ ]
        #loop through each cash flow to check for a scenario works
        # similar to totalCF function
        for i in list(self.cashflows.columns.values):
            if i == self.functional_ccy:
                continue
            else:
                pair = i + self.functional_ccy
                if pair in list(scenario.columns.values):
                    vol_curve = scenario[pair]
                    ccy_spot = self.ccy_curves[pair][0]

                else:
                    pair =  self.functional_ccy + i 
                    vol_curve = scenario[pair]
                    ccy_spot = 1/self.ccy_curves[pair][0]
            # multiply curve by percentage movements for relevant date        
            stressed_curves.append((vol_curve)*ccy_spot)
        # return stressed curves in a data fram format that can be used by a Fund instance    
        return pd.DataFrame(stressed_curves).transpose()
            
            
            
                
        
    
        