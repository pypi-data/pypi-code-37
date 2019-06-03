"""
  Module defining the class Dataset to handle a 
  set of hits recorded as binary file from SAMPIC. 

"""
from __future__ import print_function 

import numpy as np 
import re

__DEBUG__ = False

default_properties = dict (
#      version =  r'\((.*?)\)'
      software =  r'VERSION: (.*?)  ==',
      unixTime =  r'UnixTime = (.*?) ',
      date =  r'date = (.*?) ',
      time =  r'time = (.*?) ',
      board = r'BOARD (.*?) ', 
      nChannels = r'CHANNELS IN SYSTEM (.*?) ', 
      firmware_ctrl = r'CTRL FPGA FIRMWARE VERSION (.*?) ', 
      firmware_fe = r'INDEX: [0-9] FIRMWARE VERSION (.*?) BASELINE', 
      baseline    = r'BASELINE VALUE: (.*?) ', 
      index_fe    = r'FRONT-END FPGA INDEX: (.*?) ',
      correction_INL = r'INL Correction: (.*?) ',
      correction_ADC = r'ADC Correction: (.*?) ', 
      frequency  = r'SAMPLING FREQUENCY (.*?) MS/s ', 
      channelMask  = r'Enabled Channels Mask: (.*?) ', 
      reduced  = r'REDUCED DATA TYPE: (.*?) ', 
)

from .datastructs import getDataStruct 


class Dataset:
  def __init__ ( self, filename, properties = default_properties ):
    """
      Load a binary file as a dataset 
    """
    self._filename  =  filename
    self._properties = properties 

    self._loadBinary    ( filename ) 
    self._parseHeader   ( properties ) 
    self._processBytes  ( ) 


  def _loadBinary  ( self, filename ) :
    """
      Internal. Creates the _header and _dataset properties. 

      Arguments.
        filename - string
          Complete name or path of the binary file to open. 
    """
    header = []
    currentField = b""
    isLastField = False 
    with open ( filename, 'rb' ) as f:
      while True:
        currentField += f.read ( 1 ) 

        ### DETECTED END OF FIELD
        if currentField.decode()[-3:] == '===': 
          buf = currentField.decode().replace ( "===", "" )
          if not buf in [ " "*i for i in range(30) ]:
            header.append(buf)
          currentField = b"" 
          if isLastField: break

        else:
          if "ADC Correction" in currentField.decode(): isLastField = True 


      f.read ( 1 ) ## Forward of 1
#      while True:

      beginning = f.tell() 

      self._header = header 
      self._bytes = f.read(-1)

      global __DEBUG__
      if __DEBUG__: 
        f.seek ( beginning )

        print ("\n".join(self._header)) 

        data_entries = getDataStruct ('', 63, True)
        struct = np.dtype (data_entries) 
        print ("Chunksize (expect 308):", struct.itemsize)

        for iChunk in range (1000):
          #if iChunk % (604/4) == 0: print ('='*40)
          newChunk = f.read(4)
          print ( " ".join(["%02X" % (np.frombuffer(newChunk[iChar],'u1')) for iChar in range ( 4 )] ))

        f.seek ( beginning )
        for iChunk in range(30):
          newChunk = f.read(struct.itemsize)
          if not newChunk: break 

          entry = np.frombuffer ( newChunk, dtype=struct)
          #print (entry['HitNumber'], entry['Channel'] )
          #print (entry['DataSamplesRaw'])

          for prop in data_entries:
            print ( prop[0], ": ", entry[prop[0]] )  


  def _processBytes ( self ):
    """
      Internal. Parse the binary part of the input file according to 
      the information collected from the header. 
    """

    struct0 = np.dtype ( getDataStruct ( version = self.software, reducedFmt = (self.reduced == 'YES'), datasize = 0) ) 
    firstEntry = np.frombuffer ( self._bytes[:struct0.itemsize], dtype=struct0 )

    struct = np.dtype ( getDataStruct ( version = self.software, reducedFmt = (self.reduced == 'YES'), datasize = firstEntry['DataSize']) ) 
    self._dataset = np.frombuffer ( self._bytes, dtype=struct )
    del self._bytes 



  def __str__ ( self ):
    """
      Format properties of the dataset in a human readable string. 
    """
    print (">> Dataset from file: %s" % self._filename) 
    print (">> Properties:") 
    ret = []
    for prop in sorted(self._properties.keys()):
      if  hasattr ( self, prop ): 
        ret.append ( "%20s : %s" % ( prop, getattr ( self, prop ) ) ) 

    return "\n".join ( ret )



  def _parseHeader ( self, properties ):
    """
      Internal. Parse properties. 
    """
    for propname, regexp in properties.items():
      for line in self._header: 
        values = re.findall ( regexp, line ) 
        if len ( values ) > 0: 
          setattr ( self, propname, ";".join(values) )
          break 



  def __getitem__ ( self, *args, **kwargs ):
    """
      Allows direct access to the elements of the dataset through [] operator 
    """
    return self._dataset.__getitem__ ( *args, **kwargs ) 


  def keys ( self ): 
    """
      Return a list of the names of the "columns" of the structured array. 

      For example: 
        ds = Dataset ( 'sample.bin' ) 
        keys = ds.keys()
        ds [ keys[ 0 ] ] 
    """
    return list(self._dataset.dtype.names)



if __name__ == '__main__':
  ds = Dataset ( "sample.bin" ) 
  print (ds)
  print (ds.keys()) 
  print (len ( ds['HitNumber'] ) ) 

  

