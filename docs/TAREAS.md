# Tareas y reparto

Somos tres personas. El reparto es una propuesta y se puede ajustar de común acuerdo. Cada carril es dueño de su carpeta para no pisarse.

| Carril | Qué hace | Carpeta principal | Responsable |
|---|---|---|---|
| **A** | Revisor, EventBridge y avisador a Slack | `functions/revisor/`, `functions/avisador/` | por asignar |
| **B** | API, DynamoDB y pruebas | `functions/api/`, modelo de datos en `docs/` | por asignar |
| **C** | Panel web, Terraform y pipeline (coordina la infraestructura) | `web/`, `infra/`, `.github/` | dueño de la cuenta |

Lenguaje de las Lambdas: **Python** ([ADR 0001](adr/0001-lenguaje-lambdas.md)).

## Cómo están partidas las tareas
Cada etapa tiene su archivo en `docs/tareas/`. Cada tarea:
- Es **pequeña** (de 20 minutos a 2 horas) y se puede probar sola.
- Dice de qué **depende**, cuánto **cuesta**, qué se **aprende**, los **pasos**, una **prueba rápida** y cuándo está **hecha**.
- Si es de lógica, se prueba en local en segundos con `python scripts/probar.py`.
- Si toca AWS, necesita el **OK del dueño** antes de crear nada y se anota en `docs/RECURSOS.md`.

## Mapa de etapas
| Etapa | Carril | Meta | Tareas | Detalle |
|---|---|---|---|---|
| 0. Base | C y todos | Equipo listo para trabajar en local | T0.1 a T0.6 | [etapa-0](tareas/etapa-0-base.md) |
| 1. Página en S3 | C | Página estática en bucket privado, con CloudFront y Terraform | T1.1 a T1.10 | [etapa-1](tareas/etapa-1-pagina-s3.md) |
| 2. Primera Lambda | B (apoya C) | Función "hola" desplegada y consumida por la página | T2.1 a T2.8 | [etapa-2](tareas/etapa-2-primera-lambda.md) |
| 3. Datos | B | Tabla DynamoDB y API de estado e historial | T3.1 a T3.9 | [etapa-3](tareas/etapa-3-datos.md) |
| 4. El detective | A | Revisor cada 5 min y aviso a Slack en cambios | T4.1 a T4.12 | [etapa-4](tareas/etapa-4-detective.md) |
| 5. Panel | C | Página con estado real e historial | T5.1 a T5.7 | [etapa-5](tareas/etapa-5-panel.md) |
| 6. Pipeline y cierre | C y todos | CI, seguridad y decisión de futuro; despliegue con OIDC **opcional** (T6.4 y T6.5) | T6.1 a T6.8 | [etapa-6](tareas/etapa-6-pipeline-cierre.md) |

## Qué se puede hacer en paralelo
Las etapas 1, 2, 3 y 4 empiezan con tareas de **lógica pura** que no necesitan AWS, así que los tres pueden trabajar a la vez desde el primer día:

| Carril | Puede empezar ya con | Sin tocar AWS |
|---|---|---|
| A | T4.1, T4.2, T4.4, T4.5 | sí |
| B | T2.1, T2.2, T3.1, T3.2, T3.3 | sí |
| C | T1.1, T1.2 | sí |

Lo que toca AWS espera al OK del dueño y se hace de a una pieza por vez.

## Dependencias importantes
- La etapa 4 (despliegue y programación) necesita la tabla de la etapa 3.
- El panel real (etapa 5) necesita la API de la etapa 3.
- El pipeline (etapa 6) necesita que lo anterior exista en Terraform.

## Cómo tomar una tarea
1. Elige una tarea sin dueño en tu carril, o acuerda con el equipo si es de otro.
2. Crea una rama (ver [`CONTRIBUIR.md`](CONTRIBUIR.md)), por ejemplo `a/t4-1-validar-sitios`.
3. Escribe primero la prueba, luego el código. Los resultados esperados exactos de las funciones están en [`CONTRATOS.md`](CONTRATOS.md). Corre `python scripts/probar.py`.
4. Abre un PR pequeño. Marca la tarea como hecha **en el mismo PR** cambiando su título a "✅".
