from .data import WARP
from .helpers import itemize

DEFAULT_FORMAT = 'text-orig-full'
DEFAULT_FORMAT_TYPE = '{}-default'
SEP = '-'
TYPE_FMT_SEP = '#'


class Text(object):

  def __init__(self, api):
    self.api = api
    self.languages = {}
    self.nameFromNode = {}
    self.nodeFromName = {}
    config = api.TF.features[WARP[2]].metaData if WARP[2] in api.TF.features else {}
    self.sectionTypes = itemize(config.get('sectionTypes', ''), ',')
    sectionFeats = itemize(config.get('sectionFeatures', ''), ',')
    self.sectionFeatures = []
    self.sectionFeatureTypes = []
    self.config = config
    self.defaultFormat = DEFAULT_FORMAT
    self.defaultFormats = {}
    otypeInfo = api.F.otype
    otype = otypeInfo.v

    good = True
    if len(sectionFeats) != 0 and len(self.sectionTypes) != 0:
      for (fName,
           fObj) in sorted(f for f in api.TF.features.items()
                           if f[0] == sectionFeats[0] or f[0].startswith(f'{sectionFeats[0]}@')):
        if not fObj.load(silent=True):
          good = False
          continue
        meta = fObj.metaData
        code = meta.get('languageCode', '')
        self.languages[code] = dict(((k, meta.get(k, 'default'))
                                     for k in ('language', 'languageEnglish')))
        self.nameFromNode[code] = fObj.data
        self.nodeFromName[code] = dict(
            ((otype(node), name), node)
            for (node, name) in fObj.data.items()
        )
      for fName in (sectionFeats):
        if not api.TF.features[fName].load(silent=True):
          good = False
          continue
        sectionFeature = api.TF.features[fName]
        self.sectionFeatures.append(sectionFeature.data)
        self.sectionFeatureTypes.append(sectionFeature.dataType)

      sec0 = self.sectionTypes[0]
      setattr(self, f'{sec0}Name', self._sec0Name)
      setattr(self, f'{sec0}Node', self._sec0Node)

    self._compileFormats()
    self.good = good

  def _sec0Name(self, n, lang='en'):
    sec0T = self.sectionTypes[0]
    otype = self.api.F.otype.v
    refNode = n if otype(n) == sec0T else self.api.L.u(n, sec0T)[0]
    lookup = (
        self.nameFromNode['' if lang not in self.languages else lang]
    )
    return lookup.get(refNode, f'not a {sec0T} node')

  def _sec0Node(self, name, lang='en'):
    sec0T = self.sectionTypes[0]
    return self.nodeFromName['' if lang not in self.languages else lang].get((sec0T, name), None)

  def sectionTuple(self, n, lastSlot=False, fillup=False):
    sTypes = self.sectionTypes
    lsTypes = len(sTypes)
    if lsTypes == 0:
      return ()
    F = self.api.F
    E = self.api.E
    L = self.api.L
    slotType = F.otype.slotType
    maxSlot = F.otype.maxSlot
    eoslots = E.oslots.data
    nType = F.otype.v(n)

    if nType == slotType:
      r = n
    else:
      slots = eoslots[n - maxSlot - 1]
      r = slots[-1 if lastSlot else 0]

    if nType == sTypes[0]:
      if fillup:
        r1 = L.u(r, otype=sTypes[1])
        r1 = r1[0] if r1 else ''
        if lsTypes > 2:
          r2 = L.u(r, otype=sTypes[2])
          r2 = r2[0] if r2 else ''
          return (n, r1, r2)
        return (n, r1)
      return (n,)

    r0s = L.u(r, sTypes[0])
    r0 = r0s[0] if r0s else None

    if nType == sTypes[1]:
      if fillup:
        if lsTypes > 2:
          r2 = L.u(r, otype=sTypes[2])
          r2 = r2[0] if r2 else ''
          return (r0, n, r2)
      return (r0, n)

    r1s = L.u(r, sTypes[1])
    r1 = r1s[0] if r1s else ''

    if lsTypes < 3:
      return (r0, r1)

    if nType == sTypes[2]:
      return (r0, r1, n)

    r2s = L.u(r, sTypes[2])
    r2 = r2s[0] if r2s else ''

    return (r0, r1, r2)

  def sectionFromNode(self, n, lastSlot=False, lang='en', fillup=False):
    sTuple = self.sectionTuple(n, lastSlot=lastSlot, fillup=fillup)
    if len(sTuple) == 0:
      return ()

    sFs = self.sectionFeatures

    return tuple(
        '' if n is None else
        self._sec0Name(n, lang=lang)
        if i == 0 else
        sFs[i].get(n, None)
        for (i, n) in enumerate(sTuple)
    )

  def nodeFromSection(self, section, lang='en'):
    sTypes = self.sectionTypes
    if len(sTypes) == 0:
      return None
    (sec1, sec2) = self.api.C.sections.data
    sec0node = self._sec0Node(section[0], lang=lang)
    if len(section) == 1:
      return sec0node
    elif len(section) == 2:
      return sec1.get(sec0node, {}).get(section[1], None)
    else:
      return sec2.get(sec0node, {}).get(section[1], {}).get(section[2], None)

  def text(self, nodes, fmt=None, descend=None, func=None, explain=False):
    api = self.api
    E = api.E
    F = api.F
    L = api.L
    error = api.error

    slotType = F.otype.slotType
    maxSlot = F.otype.maxSlot
    eoslots = E.oslots.data

    defaultFormats = self.defaultFormats
    xformats = self._xformats
    xdTypes = self._xdTypes

    if fmt and fmt not in xformats:
      error(f'Undefined format "{fmt}"', tm=False)
      return ''

    def rescue(n):
      return f'{F.otype.v(n)}{n}'

    single = type(nodes) is int
    material = []
    good = True

    if single:
      nodes = [nodes]
    else:
      nodes = list(nodes) if explain else nodes
    if explain:
      fmttStr = 'format target type'
      ntStr = 'node type'

      nRep = (
          'single node'
          if single else
          f'iterable of {len(nodes)} nodes'
      )
      fmtRep = (
          'implicit'
          if not fmt else
          f'{fmt} targeted at {xdTypes[fmt]}'
      )
      descendRep = (
          'implicit'
          if descend is None else
          'True'
          if descend else
          'False'
      )
      funcRep = f'{"" if func else "no "} custom format implementation'
      error(f'''
EXPLANATION: T.text) called with parameters:
\tnodes  : {nRep}
\tfmt    : {fmtRep}
\tdescend: {descendRep}
\tfunc   : {funcRep}
''', tm=False)

    for node in nodes:
      nType = F.otype.v(node)
      if explain:
        error(f'\tNODE: {nType} {node}', tm=False)
      if descend:
        if explain:
          downRep = fmttStr
        if fmt:
          repf = xformats[fmt]
          downType = xdTypes[fmt]
          if explain:
            fmtRep = f'explicit {fmt}'
            expandRep = f'{downType} {{}} (descend=True) ({downRep})'
        else:
          repf = xformats[DEFAULT_FORMAT]
          downType = xdTypes[DEFAULT_FORMAT]
          if explain:
            fmtRep = f'implicit {DEFAULT_FORMAT}'
            expandRep = f'{downType} {{}} (descend=True) ({downRep})'
      else:
        downType = nType
        if explain:
          downRep = ntStr
        if fmt:
          repf = xformats[fmt]
          if descend is None:
            downType = xdTypes[fmt]
            if explain:
              downRep = fmttStr
          if explain:
            fmtRep = f'explicit {fmt}'
            expandRep = f'{downType} {{}} (descend=None) ({downRep})'
        elif nType in defaultFormats:
          dfmt = defaultFormats[nType]
          repf = xformats[dfmt]
          if descend is None:
            downType = nType
            if explain:
              downRep = fmttStr
          if explain:
            fmtRep = f'implicit {dfmt}'
            expandRep = f'{downType} {{}} (descend=None) ({downRep})'
        else:
          repf = xformats[DEFAULT_FORMAT]
          if descend is None:
            downType = xdTypes[DEFAULT_FORMAT]
            if explain:
              downRep = fmttStr
          if explain:
            fmtRep = f'implicit {DEFAULT_FORMAT}'
            expandRep = f'{downType} {{}} (descend=None) ({downRep})'

      if explain:
        expandRep2 = ''
      if downType == nType:
        if explain:
          expandRep2 = f'(no expansion needed)'
        downType = None

      if explain:
        error(f'\t\tTARGET LEVEL: {expandRep.format(expandRep2)}', tm=False)

      if explain:
        plural = 's'
      if downType == slotType:
        xnodes = eoslots[node - maxSlot - 1]
      elif downType:
        xnodes = L.d(node, otype=downType)
      else:
        xnodes = [node]
        if explain:
          plural = ''
      if explain:
        nodeRep = f'{len(xnodes)} {downType or nType}{plural} {", ".join(str(x) for x in xnodes)}'
        error(f'\t\tEXPANSION: {nodeRep}', tm=False)

      if func:
        repf = func
        if explain:
          fmtRep += f' (overridden with the explicit func argument)'
      if not repf:
        repf = rescue
        good = False
        if explain:
          fmtRep += '\n\t\t\twhich is not defined: formatting as node types and numbers'

      if explain:
        error(f'\t\tFORMATTING: {fmtRep}', tm=False)
        error(f'\t\tMATERIAL:', tm=False)
      for n in xnodes:
        rep = repf(n)
        material.append(rep)
        if explain:
          error(f'\t\t\t{F.otype.v(n)} {n} ADDS "{rep}"', tm=False)

    if not good:
      error('Text format "{DEFAULT_FORMAT}" not defined in otext.tf', tm=False)
    return ''.join(material)

  def _compileFormats(self):
    api = self.api
    TF = api.TF
    cformats = TF._cformats
    features = TF.features

    self.formats = {}
    self._xformats = {}
    self._xdTypes = {}
    for (fmt, (rtpl, feats)) in sorted(cformats.items()):
      defaultType = self.splitDefaultFormat(fmt)
      if defaultType:
        self.defaultFormats[defaultType] = fmt
      (descendType, rtpl) = self.splitFormat(rtpl)
      tpl = rtpl.replace('\\n', '\n').replace('\\t', '\t')
      self._xdTypes[fmt] = descendType
      self._xformats[fmt] = _compileFormat(tpl, feats, features)
      self.formats[fmt] = descendType

  def splitFormat(self, tpl):
    api = self.api
    F = api.F
    slotType = F.otype.slotType
    otypes = set(F.otype.all)

    descendType = slotType
    parts = tpl.split(TYPE_FMT_SEP, maxsplit=1)
    if len(parts) == 2 and parts[0] in otypes:
      (descendType, tpl) = parts
    return (descendType, tpl)

  def splitDefaultFormat(self, tpl):
    api = self.api
    F = api.F
    otypes = set(F.otype.all)

    parts = tpl.rsplit(SEP, maxsplit=1)
    return (
        parts[0]
        if len(parts) == 2 and parts[1] == 'default' and parts[0] in otypes else
        None
    )


def _compileFormat(rtpl, feats, features):
  replaceFuncs = []
  for feat in feats:
    (feat, default) = feat
    replaceFuncs.append(_makeFunc(feat, default, features))

  def g(n):
    values = tuple(replaceFunc(n) for replaceFunc in replaceFuncs)
    return rtpl.format(*values)

  return g


def _makeFunc(feat, default, features):
  if len(feat) == 1:
    ft = feat[0]
    f = features[ft].data
    return (lambda n: f.get(n, default))
  elif len(feat) == 2:
    (ft1, ft2) = feat
    f1 = features[ft1].data
    f2 = features[ft2].data
    return (lambda n: (f1.get(n, f2.get(n, default))))
  else:
    def getValue(n):
      v = None
      for ft in feat:
        v = features[ft].data.get(n, None)
        if v is not None:
          break
      return v or default
    return getValue
