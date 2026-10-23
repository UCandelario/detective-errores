"""API: entrega a la página el estado actual y el historial de los sitios.

Contrato (se implementa en las etapas 2 y 3, ver docs/tareas/):
    - Recibe eventos de una Lambda Function URL (o API Gateway) y responde JSON.
    - Rutas previstas: GET /hola (etapa 2), GET /sitios y GET /sitios/{id}/historial (etapa 3).
    - Valida las entradas y devuelve errores claros (400, 404), nunca el detalle interno.
    - "Sin dato" no es 0: un sitio sin revisiones se devuelve como ausente, no con latencia 0.

La lógica va en funciones puras; el acceso a DynamoDB se inyecta para poder
probarlo con un repositorio falso en memoria.
"""
