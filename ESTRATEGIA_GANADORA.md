# ESTRATEGIA GANADORA - London Temperature Markets

## RESUMEN EJECUTIVO

Basado en el analisis de **365 mercados historicos** y **10,000 simulaciones Monte Carlo**.

---

## LA ESTRATEGIA OPTIMA

```
ENTRADA:     97%
STOP LOSS:   50%
APUESTA:     15-25% del bankroll por trade
```

### Metricas Clave

| Metrica | Valor |
|---------|-------|
| Win Rate | **98.5%** |
| EV por $1 apostado | **+$0.0226** |
| Trades historicos | 68 |
| Perdidas | 1 (pero salvada por stop loss) |

### Proyeccion con $1,000

| Escenario | Resultado despues de 100 trades |
|-----------|--------------------------------|
| Mediana | **$1,849** (+85% ROI) |
| Peor caso | $835 (-16.5%) |
| Mejor caso | $2,111 (+111%) |
| Prob. ganancia | **99.7%** |
| Prob. ruina | **0.00%** |

---

## COMO EJECUTAR

### Paso 1: Monitorear el Mercado
- Los mercados de London Temperature se resuelven a las **00:00 UTC** (medianoche Londres)
- La mayoria de buckets llegan a 97% entre **12:00-15:00 UTC** (mediodia Londres)

### Paso 2: Identificar la Entrada
1. Abre Polymarket y busca el mercado de temperatura de Londres del dia
2. Espera a que UN bucket llegue a **97%** o mas
3. Verifica que quedan al menos **4 horas** para el cierre

### Paso 3: Ejecutar
1. Compra el bucket que esta a 97%+
2. Invierte **15-25%** de tu bankroll
3. Pon una orden de venta (stop loss) en **50%**

### Paso 4: Esperar
- **98.5% de las veces**: El bucket sube a 100% y ganas +3%
- **1.5% de las veces**: El bucket cae, el stop loss se activa en 50%, pierdes -47%

---

## MATEMATICA DEL EDGE

### Por que funciona

```
Probabilidad de ganar:    98.5%
Ganancia si ganas:        +3% ($0.03 por $1)
Probabilidad de perder:   1.5%
Perdida si pierdes:       -47% ($0.47 por $1 con stop loss)

EV = 0.985 × $0.03 - 0.015 × $0.47 = +$0.0226 por $1
```

**Por cada $100 que apuestas, esperas ganar $2.26 en promedio.**

### Comparacion con otras estrategias

| Estrategia | Win Rate | EV/trade | Veredicto |
|------------|----------|----------|-----------|
| **97% + Stop 50%** | 98.5% | **+$0.0226** | OPTIMA |
| 97% sin stop | 98.5% | +$0.0153 | Viable |
| 98% cualquiera | 100% | +$0.0200 | Muy pocos trades |
| 95% sin stop | 93.1% | -$0.0063 | PERDER DINERO |
| 90% sin stop | 89.3% | -$0.0067 | PERDER DINERO |

---

## EL UNICO CASO DE FALLO

**Fecha:** 2026-02-01
**Bucket que fallo:** 10C (llego a 97%)
**Ganador real:** 9C

### Que paso:
- 12:44 UTC: 10C llega a 97%
- 12:48 UTC: Cae a 88.5% (4 minutos despues)
- 13:25 UTC: Cae a 79%
- 13:42 UTC: Cae a 60%
- 13:43 UTC: **STOP LOSS SE ACTIVA** en ~50%
- Final: 10C termina en 0.1%

### Leccion:
Sin stop loss habrias perdido 97%. Con stop loss en 50%, perdiste solo 47%.
**El stop loss salvo $50 de cada $100 apostados.**

---

## REGLAS DE ORO

1. **NUNCA** entres por debajo de 97% sin stop loss
2. **SIEMPRE** usa stop loss en 50%
3. **NUNCA** apuestes mas del 25% del bankroll por trade
4. **ESPERA** a que el bucket llegue al umbral, no anticipes
5. **VERIFICA** que quedan >4 horas para el cierre
6. Si ya paso de 98%, el profit es menor pero mas seguro

---

## FRECUENCIA DE TRADES

- ~1 trade por dia (cuando un bucket llega a 97%)
- ~30 trades por mes
- La mayoria de oportunidades aparecen **12:00-16:00 UTC**

---

## SIZING RECOMENDADO

| Bankroll | Apuesta por trade | Ganancia esperada/mes |
|----------|-------------------|----------------------|
| $100 | $15-25 | ~$10-17 |
| $500 | $75-125 | ~$50-85 |
| $1,000 | $150-250 | ~$100-170 |
| $5,000 | $750-1,250 | ~$500-850 |

*Basado en 30 trades/mes con EV de +$0.0226 por $1*

---

## RIESGOS

1. **Cambio de patron**: Los mercados pueden cambiar. El edge historico puede desaparecer.
2. **Liquidez**: En algunos momentos puede ser dificil comprar/vender al precio deseado.
3. **Plataforma**: Polymarket puede tener problemas tecnicos.
4. **Regulatorio**: Las plataformas de prediccion tienen riesgos regulatorios.

---

## DISCLAIMER

Este analisis esta basado en datos historicos. El rendimiento pasado NO garantiza resultados futuros. Solo invierte lo que puedas permitirte perder.

---

*Generado por London Edge - Analysis Suite*
*Datos: 365 mercados historicos de Polymarket*
*Simulaciones: 10,000 Monte Carlo*
