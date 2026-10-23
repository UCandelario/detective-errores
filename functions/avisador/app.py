"""Avisador: manda un mensaje a Slack cuando el estado de un sitio cambia.

Contrato (se implementa en la etapa 4, ver docs/tareas/etapa-4-detective.md):
    - Entrada: un cambio de estado (sitio, estado anterior, estado nuevo, hora).
    - Arma un mensaje claro y lo envía al webhook de Slack.
    - El webhook es un SECRETO: se lee de SSM Parameter Store, nunca del código.
    - Si no hay cambio, no manda nada (no se avisa en cada revisión).

La lógica de armar el mensaje es pura (sin red) para probarla rápido.
"""
