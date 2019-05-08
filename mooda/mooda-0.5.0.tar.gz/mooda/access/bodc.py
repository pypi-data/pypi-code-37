"""
Module to open data from the NetCDF files from https://www.bodc.ac.uk/
"""
from datetime import datetime
import pandas as pd
from mooda import WaterFrame


class Bodc:
    """
    Class to import nc files from https://www.bodc.ac.uk/.
    """

    @staticmethod
    def from_nc_to_waterframe(path):
        """
        It reads a nc file and parses its content into a WaterFrame.

        Parameters
        ----------
            path: str
                Path where the nc files is.

        Returns
        -------
            wf: WaterFrame
        """

        def change2metadata(wf_in, keys2change):
            keys = wf_in.data.keys()

            for key in keys2change:
                if key in keys:
                    wf_in.metadata[key] = wf_in[key][0]
                    del wf_in.data[key]

            return wf_in

        wf = WaterFrame()
        wf.from_netcdf(path)
        # wf.data.reset_index(inplace=True)
        # Here we have something into wf.data, but the wf is not well formated
        
        # Create the mean of the values of the group MAXZ
        wf.data = wf.data.groupby('MAXZ').mean()

        # Do not know what to do with the folloowing data keys
        unknown_word = ['POSITION_SEADATANET_QC', 'TIME_SEADATANET_QC', 'ACYCAA01',
                        'ACYCAA01_SEADATANET_QC']
        for unknown in unknown_word:
            del wf.data[unknown]
            try:
                del wf.meaning[unknown]
            except KeyError:
                pass
        
        # Change values of QC (48 is 0)
        # Change name from {parameter}_SEADATANET_QC to {parameter}_QC
        for key in wf.data.keys():
            if "_QC" in key:
                wf.data[key] = wf.data[key] - 48
                parameter = key.split("_")[0]
                new_key = parameter + "_QC"
                wf.data.rename(columns={key: new_key}, inplace=True)
                wf.meaning[parameter]['ancillary_variable'] = new_key

        # Some data keys seems to be always the same value, we are going to add this
        # info to the metadata
        change_words = ['SDN_CRUISE', 'SDN_EDMO_CODE', 'SDN_STATION', 'SDN_LOCAL_CDI_ID',
                        'SDN_BOT_DEPTH']
        wf = change2metadata(wf, change_words)

        # Rename parameters
        for parameter in wf.parameters():
            if "PSAL" in parameter:
                wf.rename(parameter, "PSAL")
            elif "TEMP" in parameter:
                wf.rename(parameter, "TEMP")

        # Set index
        keys = wf.data.keys()
        if "TIME" in keys:
            wf.data.reset_index(inplace=True)
            del wf.data['MAXZ']
            wf.data.set_index(['TIME'], inplace=True)
        elif "PRES" in keys:
            wf.data.reset_index(inplace=True)
            del wf.data['MAXZ']
            wf.data.set_index(['PRES'], inplace=True)
        
        return wf
