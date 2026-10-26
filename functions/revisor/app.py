"""Revisor: consulta la lista fija de sitios y mide código de respuesta y latencia.

Contrato (se implementa en la etapa 4, ver docs/tareas/etapa-4-detective.md):
    - Entrada: evento de EventBridge Scheduler (se ignora su contenido).
    - Lee la lista fija de sitios de la configuración. Nunca una URL externa.
    - Por cada sitio: estado ("sano", "degradado", "caido"), código y latencia en ms.
    - Guarda el resultado en DynamoDB y avisa al avisador solo si el estado cambió.

La lógica va en funciones pequeñas y puras (sin llamadas a AWS ni a la red) para
poder probarlas rápido; el handler solo las orquesta.
"""

def evaluar_respuesta(codigo, latencia_ms, umbral_ms=2000):
        if codigo is None and latencia_ms is None:
            return "caido"
        if (codigo < 100 or codigo > 599) or latencia_ms < 0:
            raise ValueError("Código o latencia inválidos")
        if 200 <= codigo <= 299:
            if latencia_ms > umbral_ms:
                return "degradado"
            else:
                return "sano" 
        if 300 <= codigo <= 399:
            return "degradado"
        else:
            return "caido"
