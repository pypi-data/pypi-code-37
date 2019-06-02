# @Classes
from .WhatsappExtract import WhatsappExtract

def get_whatsapp_extract(files, nlp_admin_instance=None, model_id=''):
    """
    A partir de un archivo con contenido en el formato esperado, parsea el contenido
    y, de ser provisto, crea las tareas de análisis requeridas para realizar el
    análisis.

    :files: [List(File)] - Arreglo de archivos del cual extraer la información.

    :nlp_admin_instance: [NLPModelAdmin] - Instancia activa del administrador de 
    modelos de nlp_model_gen.

    :model_id: [String] - Id del modelo a utilizar. Requerido si se utiliza una instancia
    del administrador de modelos.

    :return: [Dict] - Resultados de la extracción.
    """
    return WhatsappExtract(files, nlp_admin_instance, model_id)
    