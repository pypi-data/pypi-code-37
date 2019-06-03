"""
  Data structures 
"""



def getDataStruct ( version, datasize, reducedFmt=False ):
  full = dict()
  reduced = dict() 

  full['V3.2.12'] = [
    ('HitNumber',                     'u4'),
    ('UnixTime',                      'f8'),
    ('Channel',                       'u4'),
    ('CellInfoForOrderedData',        'u4'),
    ('SampicTimeStampA',              'u4'),
    ('SampicTimeStampB',              'u4'),
    ('FPGATimeStamp',                 'u8'),
    ('StartOfADCRamp',                'u4'),
    ('RawTOTValue',                   'i4'),
    ('TOTValue',                      'f4'),
    ('PhysicalCell0Time',             'f8'),
    ('OrderCell0Time',                'f8'),
    ('Time',                          'f8'),
    ('Baseline',                      'f4'),
    ('RawPeak',                       'f4'),
    ('Amplitude',                     'f4'),
    ('ADCCounterLatched',             'u4'),
    ('DataSize',                      'u4'),
    ('TriggerPosition',               'u4', int(datasize)),
    ('DataSamplesRaw',                'f4', int(datasize)),
    ]

 ## Ch (int) Cell0Time (double in ns)  RawTOTValue (int in ADC Count) TOTValue (float in ns) Time (double in ns) Baseline (in ADC or Volts) RawPeak (in ADC or Volts) Amplitude ((RawPeak - Baseline) in ADC ot Volts) DataSize(int) 

  reduced['V3.2.12'] = [
    ('HitNumber',                     'u4'),
    ('UnixTime',                      'f8'),
    ('Channel',                       'u4'),
    ('OrderCell0Time',                'f8'),
    ('RawTOTValue',                   'i4'),
    ('TOTValue',                      'f4'),
    ('Time',                          'f8'),
    ('Baseline',                      'f4'),
    ('RawPeak',                       'f4'),
    ('Amplitude',                     'f4'),
    ('DataSize',                      'u4'),
    ('DataSamplesRaw',                'f4', int(datasize)), 
    ]


  if reducedFmt:
    try: 
      return reduced [ version ]
    except KeyError:
      lastVersion = sorted(reduced.keys())[-1] 
      print ( " ERROR! "*10 ) 
      print ( "Software Version %s is unknown. Using %s instead." % (version, lastVersion) )
      return reduced [ lastVersion ] 
  else: 
    try: 
      return full [ version ]
    except KeyError:
      lastVersion = sorted(full.keys())[-1] 
      print ( " ERROR! "*10 ) 
      print ( "Software Version %s is unknown. Using %s instead." % (version, lastVersion) )
      return full [ lastVersion ] 

  


