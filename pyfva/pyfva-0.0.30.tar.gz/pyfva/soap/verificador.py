# -*- coding: utf-8 -*-
# flake8:noqa
# isort:skip_file
# vim:et:ft=python:nowrap:sts=4:sw=4:ts=4
##############################################################################
# Note: Generated by soapfish.wsdl2py at 2018-02-27 14:09:20.817038
#       Try to avoid editing it if you might need to regenerate it.
##############################################################################

from soapfish import soap, xsd
from pyfva.soap import settings
BaseHeader = xsd.ComplexType

##############################################################################
# Schemas


# http://bccr.fva.cr/


class RespuestaDeLaSolicitud(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    CodigoDeError = xsd.Element(xsd.Int, minOccurs=1)
    ExisteUnaFirmaCompleta = xsd.Element(xsd.Boolean, minOccurs=1)
    FueExitosa = xsd.Element(xsd.Boolean, minOccurs=1)

    @classmethod
    def create(cls, CodigoDeError, ExisteUnaFirmaCompleta, FueExitosa):
        instance = cls()
        instance.CodigoDeError = CodigoDeError
        instance.ExisteUnaFirmaCompleta = ExisteUnaFirmaCompleta
        instance.FueExitosa = FueExitosa
        return instance


class ExisteUnaSolicitudDeFirmaCompleta(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    laCedulaDelUsuario = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class ExisteUnaSolicitudDeFirmaCompletaResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    ExisteUnaSolicitudDeFirmaCompletaResult = xsd.Element(RespuestaDeLaSolicitud, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class ValideElServicio(xsd.ComplexType):
    pass


class ValideElServicioResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    ValideElServicioResult = xsd.Element(xsd.Boolean, minOccurs=1)

    @classmethod
    def create(cls, ValideElServicioResult):
        instance = cls()
        instance.ValideElServicioResult = ValideElServicioResult
        return instance


Schema_c49e7 = xsd.Schema(
    imports=[],
    includes=[],
    targetNamespace=settings.FVA_HOST,
    elementFormDefault='qualified',
    simpleTypes=[],
    attributeGroups=[],
    groups=[],
    complexTypes=[RespuestaDeLaSolicitud],
    elements={'ExisteUnaSolicitudDeFirmaCompleta': xsd.Element(ExisteUnaSolicitudDeFirmaCompleta()), 'ExisteUnaSolicitudDeFirmaCompletaResponse': xsd.Element(ExisteUnaSolicitudDeFirmaCompletaResponse()), 'ValideElServicio': xsd.Element(ValideElServicio()), 'ValideElServicioResponse': xsd.Element(ValideElServicioResponse())},
)


##############################################################################
# Methods


ExisteUnaSolicitudDeFirmaCompleta_method = xsd.Method(
    soapAction=settings.FVA_HOST + 'ExisteUnaSolicitudDeFirmaCompleta',
    input='ExisteUnaSolicitudDeFirmaCompleta',
    inputPartName='parameters',
    output='ExisteUnaSolicitudDeFirmaCompletaResponse',
    outputPartName='parameters',
    operationName='ExisteUnaSolicitudDeFirmaCompleta',
    style='document',
)


ValideElServicio_method = xsd.Method(
    soapAction=settings.FVA_HOST + 'ValideElServicio',
    input='ValideElServicio',
    inputPartName='parameters',
    output='ValideElServicioResponse',
    outputPartName='parameters',
    operationName='ValideElServicio',
    style='document',
)


##############################################################################
# SOAP Service


VerificadorSoap_SERVICE = soap.Service(
    name='VerificadorSoap',
    targetNamespace=settings.FVA_HOST,
    location='${scheme}://${host}/'+settings.SERVICE_URLS['verifica'],
    schemas=[Schema_c49e7],
    version=soap.SOAPVersion.SOAP12,
    methods=[ExisteUnaSolicitudDeFirmaCompleta_method, ValideElServicio_method],
)


##############################################################################
# SOAP Service Stub


class VerificadorSoapServiceStub(soap.Stub):
    SERVICE = VerificadorSoap_SERVICE
    SCHEME = settings.STUB_SCHEME
    HOST = settings.STUB_HOST

    def ExisteUnaSolicitudDeFirmaCompleta(self, ExisteUnaSolicitudDeFirmaCompleta, header=None):
        return self.call('ExisteUnaSolicitudDeFirmaCompleta', ExisteUnaSolicitudDeFirmaCompleta, header=header)

    def ValideElServicio(self, ValideElServicio, header=None):
        return self.call('ValideElServicio', ValideElServicio, header=header)
