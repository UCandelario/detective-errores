"""Revisor: consulta la lista fija de sitios y mide código de respuesta y latencia.

Contrato (se implementa en la etapa 4, ver docs/tareas/etapa-4-detective.md):
    - Entrada: evento de EventBridge Scheduler (se ignora su contenido).
    - Lee la lista fija de sitios de la configuración. Nunca una URL externa.
    - Por cada sitio: estado ("sano", "degradado", "caido"), código y latencia en ms.
    - Guarda el resultado en DynamoDB y avisa al avisador solo si el estado cambió.

La lógica va en funciones pequeñas y puras (sin llamadas a AWS ni a la red) para
poder probarlas rápido; el handler solo las orquesta.
"""
