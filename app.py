import streamlit as st
import yfinance as yf
import numpy as np
import plotly.graph_objects as go
import random
import time

st.set_page_config(page_title="Simulador de Coberturas", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=DM+Mono:wght@400;500&display=swap');

/* ── PALETA ──
   Fondo principal:   #f0f0ed  (gris marfil cálido)
   Fondo secundario:  #e8e8e4  (gris piedra)
   Acento verde pino: #2d5a3d
   Acento azul noche: #1b2d4f
   Texto principal:   #1a1a18
   Texto suave:       #5c5c58
   Borde:             #c8c8c4
*/

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #f0f0ed;
    color: #1a1a18;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1280px; background: #f0f0ed; }

/* Encabezado */
.top-header {
    border-bottom: 2.5px solid #1b2d4f;
    padding-bottom: 1.2rem;
    margin-bottom: 2rem;
}
.top-header h1 {
    font-size: 1.7rem; font-weight: 700;
    letter-spacing: -0.03em; margin: 0;
    color: #1b2d4f;
}
.top-header p { font-size: 0.9rem; color: #5c5c58; margin: 0.3rem 0 0 0; }

/* Badges y secciones */
.step-badge {
    display: inline-block;
    background: #1b2d4f;
    color: #f0f0ed;
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.08em; padding: 3px 12px;
    border-radius: 2px; margin-bottom: 0.6rem;
    text-transform: uppercase;
}
.section-title {
    font-size: 1.15rem; font-weight: 700;
    letter-spacing: -0.02em; margin: 0 0 0.3rem 0;
    color: #1a1a18;
}
.section-sub { font-size: 0.88rem; color: #5c5c58; margin: 0 0 1.2rem 0; line-height: 1.6; }

/* Tarjeta de caso */
.case-card {
    border: 2px solid #1b2d4f;
    border-radius: 6px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    background: #fafaf7;
    box-shadow: 0 2px 12px rgba(27,45,79,0.07);
}
.case-label {
    position: absolute; top: -12px; left: 20px;
    background: #1b2d4f; color: #f0f0ed;
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.1em; padding: 2px 14px;
    text-transform: uppercase; border-radius: 2px;
}
.case-title { font-size: 1.25rem; font-weight: 700; margin: 0.5rem 0 0.8rem 0; color: #1b2d4f; }
.case-narrative {
    font-size: 0.96rem; line-height: 1.9; color: #3a3a36;
    font-style: italic;
    border-left: 3px solid #2d5a3d;
    padding-left: 1rem; margin-bottom: 1.2rem;
    background: #f4f7f4;
    border-radius: 0 4px 4px 0;
    padding: 0.8rem 1rem;
}
.case-problema { font-size: 0.96rem; line-height: 1.8; color: #2a2a26; margin-bottom: 1rem; }
.case-pregunta {
    font-size: 1rem; font-weight: 700; color: #fafaf7;
    background: #2d5a3d;
    border-radius: 4px;
    padding: 0.9rem 1.3rem;
    margin-top: 1rem;
}

/* Pills */
.pill-row { display: flex; gap: 0.8rem; flex-wrap: wrap; margin: 1rem 0 0 0; }
.pill {
    border: 1.5px solid #1b2d4f;
    border-radius: 3px; padding: 4px 14px;
    font-size: 0.82rem; font-weight: 500;
    color: #1b2d4f; background: #eef0f5;
}
.pill-alert {
    border: 1.5px solid #8b2020;
    border-radius: 3px; padding: 4px 14px;
    font-size: 0.82rem; font-weight: 600;
    color: #8b2020; background: #fdf0f0;
}

/* Divisor */
.divider { border: none; border-top: 1px solid #c8c8c4; margin: 2rem 0; }

/* Paneles participantes */
.panel {
    border: 2px solid #c8c8c4;
    border-radius: 6px; padding: 1.4rem;
    background: #fafaf7;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05);
}
.panel-title {
    font-size: 1rem; font-weight: 700;
    padding-bottom: 0.8rem;
    border-bottom: 2px solid #1b2d4f;
    margin-bottom: 1rem; color: #1b2d4f;
}

/* Resultados */
.resultado-num   { font-family: 'DM Mono', monospace; font-size: 1.35rem; font-weight: 700; }
.resultado-label {
    font-size: 0.75rem; color: #5c5c58;
    text-transform: uppercase; letter-spacing: 0.06em;
    margin-bottom: 0.15rem; margin-top: 0.7rem;
}
.pos { color: #2d5a3d; }
.neg { color: #8b2020; }

/* Timer */
.timer-badge {
    display: inline-block; font-family: 'DM Mono', monospace;
    font-size: 0.82rem; background: #e8e8e4;
    border: 1.5px solid #c8c8c4; border-radius: 3px;
    padding: 3px 10px; margin-top: 0.5rem; color: #5c5c58;
}
.timer-fast { background: #dff0e5; border-color: #2d5a3d; color: #1d3d29; }
.timer-slow { background: #fef6e0; border-color: #8a6e20; color: #5a4610; }

/* Veredicto */
.veredicto-card {
    border: none; border-radius: 6px; padding: 2rem;
    margin: 1.5rem 0;
    background: linear-gradient(135deg, #1b2d4f 0%, #2d5a3d 100%);
    color: #f0f0ed;
    box-shadow: 0 4px 20px rgba(27,45,79,0.25);
}
.veredicto-card h2 {
    font-size: 1.5rem; font-weight: 700;
    margin: 0 0 0.5rem 0; letter-spacing: -0.03em;
    color: #ffffff;
}
.veredicto-card p { font-size: 0.95rem; line-height: 1.8; color: #c8d8c8; margin: 0; }
.veredicto-card .perfil {
    margin-top: 1.2rem; padding-top: 1.2rem;
    border-top: 1px solid rgba(255,255,255,0.2);
    font-size: 0.92rem; line-height: 1.7; color: #d8e8d8;
}

/* Perdedor */
.perdedor-card {
    border: 2px solid #8b2020; border-radius: 6px;
    padding: 1.4rem 1.8rem; margin: 1rem 0;
    background: #fdf5f5;
}
.perdedor-card h4 { color: #8b2020; margin: 0 0 0.8rem 0; font-size: 1rem; }

/* Empate */
.empate-card {
    border: 2px solid #5c5c58; border-radius: 6px;
    padding: 1.5rem 2rem; margin: 1.5rem 0;
    background: #f4f4f0;
}

/* Fórmulas */
.formula-box {
    background: #eef0f5;
    border: 1px solid #c8cede;
    border-left: 4px solid #1b2d4f;
    border-radius: 4px; padding: 1rem 1.2rem;
    margin: 0.8rem 0 1rem 0;
    font-size: 0.88rem; line-height: 1.8;
}
.formula-box .ftitle {
    font-weight: 700; font-size: 0.82rem;
    text-transform: uppercase; letter-spacing: 0.07em;
    color: #1b2d4f; margin-bottom: 0.5rem;
}
.formula-box .fmath {
    font-family: 'DM Mono', monospace; font-size: 0.88rem;
    background: #fafaf7; border: 1px solid #c8c8c4;
    border-radius: 3px; padding: 0.4rem 0.8rem;
    margin: 0.4rem 0; display: block; color: #1b2d4f;
}
.formula-box .fexplain { font-size: 0.84rem; color: #4a4a46; margin-top: 0.5rem; line-height: 1.6; }

/* Botones */
.stButton > button {
    background: #1b2d4f !important;
    color: #f0f0ed !important;
    border: none !important; border-radius: 4px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
    padding: 0.6rem 1.8rem !important; width: 100% !important;
    transition: background 0.2s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover { background: #2d5a3d !important; }
.stButton > button:disabled {
    background: #9ca3a0 !important;
    color: #e0e0dc !important;
    opacity: 0.6 !important;
}

/* Métricas */
[data-testid="metric-container"] {
    border: 1px solid #c8c8c4;
    border-radius: 6px; padding: 0.8rem 1rem;
    background: #fafaf7;
}
[data-testid="metric-container"] label {
    color: #5c5c58 !important; font-size: 0.78rem !important;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #1b2d4f !important; font-weight: 700 !important;
}

/* Info boxes de Streamlit */
.stAlert {
    border-radius: 4px !important;
    border-left-width: 4px !important;
}

/* Selectbox y sliders */
.stSelectbox > div > div {
    border-color: #c8c8c4 !important;
    background: #fafaf7 !important;
    border-radius: 4px !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #1b2d4f !important;
}
</style>
""", unsafe_allow_html=True)

# ── DATOS DE MERCADO ──
@st.cache_data(ttl=3600)
def cargar_mercado():
    try:
        hist = yf.Ticker("EURUSD=X").history(period="1y")
        spot = round(hist['Close'].iloc[-1], 4)
        vol  = round(hist['Close'].pct_change().std() * np.sqrt(252), 4)
        return spot, vol, 0.0530, hist
    except:
        return 1.0850, 0.068, 0.0530, None

spot_actual, volatilidad, sofr, hist_fx = cargar_mercado()

def forward_teorico(spot, r_usd, r_eur, dias):
    return round(spot * (1 + r_usd * dias/365) / (1 + r_eur * dias/365), 4)

# ── CASOS NARRATIVOS ──
def casos_narrativos(spot, fwd, tasa_hoy, vol):
    return [
        {
            "emoji": "🏗️",
            "sector": "Construcción e Infraestructura",
            "titulo": "El contrato más grande — y el riesgo que nadie calculó",
            "narrativa": (
                f"Es enero. El gerente financiero de una constructora en Guayaquil acaba de firmar "
                f"el contrato más importante de la historia de la empresa: un proyecto con una firma "
                f"española que pagará en dólares. Todo parece perfecto — hasta que el equipo financiero "
                f"nota un problema. Los materiales de construcción especializados se importan de Europa "
                f"y deben pagarse en euros. El contrato dura 8 meses, y el primer pago grande cae "
                f"exactamente en ese plazo."
            ),
            "problema": (
                f"Hoy un euro vale <b>${spot:.4f}</b>. Si el euro sube a <b>${spot*1.08:.4f}</b> — "
                f"algo perfectamente posible dado que la volatilidad histórica del EUR/USD es "
                f"<b>{vol*100:.1f}% anual</b> — la empresa perdería <b>${(spot*1.08 - spot)*300000:,.0f}</b> "
                f"de su margen de ganancia sin haber cometido ningún error operativo. "
                f"El directorio se reúne de emergencia. El gerente tiene que presentar una solución mañana."
            ),
            "pregunta": "¿Cómo protege la empresa sus €300,000 de obligación cambiaria antes de que el euro se mueva?",
            "monto_eur": 300_000,
            "deuda_usd": 150_000,
            "plazo_meses": 8,
            "spread": 0.02,
            "riesgo_principal": "cambiario",
        },
        {
            "emoji": "🌸",
            "sector": "Agroindustria / Exportación",
            "titulo": "Las flores llegaron — pero el dinero se encogió",
            "narrativa": (
                f"Una empresa exportadora de flores de la Sierra ecuatoriana lleva 15 años vendiendo "
                f"a Europa. Siempre cobró en euros y siempre le funcionó bien. Pero este año algo "
                f"cambió: el dólar se fortaleció frente al euro, y cuando la empresa convirtió sus "
                f"cobros en euros a dólares, recibió mucho menos de lo esperado. Las flores fueron "
                f"las mismas, el precio en euros fue el mismo — pero en dólares, los ingresos cayeron."
            ),
            "problema": (
                f"La empresa espera recibir €250,000 en los próximos 6 meses por exportaciones ya "
                f"comprometidas. Si el euro cae de <b>${spot:.4f}</b> a <b>${spot*0.94:.4f}</b>, "
                f"la empresa recibirá <b>${(spot - spot*0.94)*250000:,.0f} menos</b> que lo proyectado "
                f"en su presupuesto anual. Eso compromete el pago a proveedores y el bono de la cosecha. "
                f"El gerente de finanzas necesita asegurar hoy el tipo de cambio al que recibirá esos euros."
            ),
            "pregunta": "¿Cómo asegura la empresa que recibirá un tipo de cambio justo por sus €250,000, sin importar lo que haga el mercado?",
            "monto_eur": 250_000,
            "deuda_usd": 100_000,
            "plazo_meses": 6,
            "spread": 0.018,
            "riesgo_principal": "cambiario",
        },
        {
            "emoji": "🏥",
            "sector": "Salud Privada",
            "titulo": "El equipo médico llega en 4 meses — el precio, nadie lo sabe",
            "narrativa": (
                f"Una cadena de clínicas privadas en Quito acaba de ganar la licitación para modernizar "
                f"tres centros de diagnóstico. Los equipos de resonancia magnética y tomografía se fabrican "
                f"en Alemania. El proveedor europeo fijó el precio en euros, con entrega en 4 meses y "
                f"pago contra entrega. La dirección médica ya anunció la modernización públicamente."
            ),
            "problema": (
                f"El presupuesto fue aprobado con el euro a <b>${spot:.4f}</b>. Si al momento del pago "
                f"el euro vale <b>${spot*1.06:.4f}</b> — un movimiento moderado y perfectamente realista — "
                f"la factura en dólares sería <b>${(spot*1.06)*200000:,.0f}</b> en lugar de "
                f"<b>${spot*200000:,.0f}</b>. Esa diferencia de <b>${(spot*1.06 - spot)*200000:,.0f}</b> "
                f"no está en ningún presupuesto. Cancelar el pedido tiene penalidades. No pagar, tampoco es opción."
            ),
            "pregunta": "¿Cómo bloquea la clínica hoy el precio de sus €200,000 para no llevarse una sorpresa en 4 meses?",
            "monto_eur": 200_000,
            "deuda_usd": 200_000,
            "plazo_meses": 4,
            "spread": 0.022,
            "riesgo_principal": "cambiario",
        },
        {
            "emoji": "🏢",
            "sector": "Bienes Raíces / Financiamiento",
            "titulo": "El crédito parecía barato — hasta que la tasa empezó a subir",
            "narrativa": (
                f"Un fondo inmobiliario en Cuenca financió un complejo de departamentos con un crédito "
                f"internacional de $200,000 a tasa variable. Cuando firmaron, la tasa era atractiva: "
                f"SOFR + 2%, lo que daba un {tasa_hoy:.2f}% anual. Todo el modelo financiero del proyecto "
                f"se construyó sobre ese número. Las ventas van bien. Pero en los últimos meses, "
                f"la Reserva Federal de Estados Unidos ha dado señales claras de que las tasas seguirán subiendo."
            ),
            "problema": (
                f"Si la tasa SOFR sube de <b>{sofr*100:.2f}%</b> a <b>{sofr*100+2:.2f}%</b> — "
                f"algo que los analistas consideran probable — el pago mensual de intereses del fondo "
                f"subiría en <b>${200000 * 0.02 / 12:,.0f} adicionales por mes</b>. "
                f"En 9 meses, eso se convierte en <b>${200000 * 0.02 * 9/12:,.0f}</b> no presupuestados. "
                f"El margen del proyecto pasa de rentable a crítico. Los inversionistas empiezan a preguntar."
            ),
            "pregunta": "¿Cómo convierte el fondo su deuda variable en un pago fijo predecible, antes de que la tasa suba más?",
            "monto_eur": 150_000,
            "deuda_usd": 200_000,
            "plazo_meses": 9,
            "spread": 0.02,
            "riesgo_principal": "tasa",
        },
        {
            "emoji": "💻",
            "sector": "Tecnología e Importación",
            "titulo": "El servidor más caro de la historia — y nadie lo vio venir",
            "narrativa": (
                f"Una empresa importadora de tecnología en Guayaquil ganó un contrato para equipar "
                f"los laboratorios de cómputo de tres universidades privadas. El precio al cliente "
                f"ya está fijado en dólares y firmado. Los servidores y equipos se compran en Europa "
                f"y el proveedor alemán cotiza exclusivamente en euros. El margen de la operación "
                f"es del 12% — justo lo suficiente para ser rentable."
            ),
            "problema": (
                f"El pedido es de €350,000 pagaderos en 6 meses. Si el euro sube apenas un 6% — "
                f"de <b>${spot:.4f}</b> a <b>${spot*1.06:.4f}</b> — el costo en dólares sube en "
                f"<b>${(spot*1.06 - spot)*350000:,.0f}</b>. Ese monto representa más de la mitad "
                f"del margen total de la operación. La empresa no puede subir el precio al cliente "
                f"porque el contrato ya está firmado. Si no hace nada, el tipo de cambio decide "
                f"si este negocio fue rentable o una pérdida."
            ),
            "pregunta": "¿Cómo protege la empresa su margen de ganancia frente a una subida del euro en los próximos 6 meses?",
            "monto_eur": 350_000,
            "deuda_usd": 150_000,
            "plazo_meses": 6,
            "spread": 0.025,
            "riesgo_principal": "cambiario",
        },
    ]

# ── FUNCIONES FINANCIERAS ──
def calc_forward(spot_fut, tasa_fwd, nocional):
    sin = nocional * spot_fut
    con = nocional * tasa_fwd
    return {"sin": sin, "con": con, "ahorro": sin - con}

def calc_opcion(spot_fut, strike, prima, nocional):
    sin       = nocional * spot_fut
    prima_tot = prima * nocional
    ejercida  = spot_fut > strike
    con       = (nocional * strike if ejercida else nocional * spot_fut) + prima_tot
    return {"sin": sin, "con": con, "ahorro": sin - con,
            "prima_total": prima_tot, "ejercida": ejercida}

def calc_swap(sofr_fut, tasa_fija, spread, nocional, meses):
    var = (sofr_fut/100 + spread) * nocional * meses/12
    fij = (tasa_fija/100 + spread) * nocional * meses/12
    return {"sin": var, "con": fij, "ahorro": var - fij}

def norm_cdf(x):
    return 0.5 * (1 + np.sign(x) * np.sqrt(1 - np.exp(-2*x**2/np.pi)))

def black_scholes_call(S, K, T, r, sigma):
    if T <= 0 or sigma <= 0:
        return max(S - K, 0)
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return float(S*norm_cdf(d1) - K*np.exp(-r*T)*norm_cdf(d2))

def var_95(nocional, spot, vol, T):
    return nocional * spot * vol * np.sqrt(T) * 1.645

# ── VALIDACIONES ──
def validar_forward(tasa_fwd, fwd_ref):
    margen_min = round(fwd_ref - 0.02, 4)
    margen_max = round(fwd_ref + 0.05, 4)
    if tasa_fwd < margen_min:
        return False, (f"Tasa {tasa_fwd:.4f} demasiado baja — ningún banco aceptará un forward "
                       f"tan por debajo del precio justo de mercado ({fwd_ref:.4f}). "
                       f"Mínimo aceptable: {margen_min:.4f}.")
    if tasa_fwd > margen_max:
        return False, (f"Tasa {tasa_fwd:.4f} innecesariamente alta — pagarías de más sin razón. "
                       f"Máximo razonable: {margen_max:.4f}.")
    return True, ""

def validar_opcion(strike, spot, prima, prima_bs):
    strike_min = round(spot - 0.01, 4)
    strike_max = round(spot + 0.08, 4)
    prima_min  = round(max(0.010, prima_bs * 0.5), 4)
    prima_max  = round(prima_bs * 2.5, 4)
    errores = []
    if strike < strike_min:
        errores.append(f"Strike {strike:.4f} demasiado bajo — el banco no emite opciones tan dentro del dinero a ese precio.")
    if strike > strike_max:
        errores.append(f"Strike {strike:.4f} demasiado alto — cubres un riesgo tan lejano que la prima no justifica la protección.")
    if prima < prima_min:
        errores.append(f"Prima ${prima:.4f}/€ irrealmente baja — Black-Scholes indica ${prima_bs:.4f}/€ como referencia de mercado.")
    if prima > prima_max:
        errores.append(f"Prima ${prima:.4f}/€ excesiva — pagarías {prima/max(prima_bs,0.001):.1f}x el valor teórico calculado.")
    if errores:
        return False, " | ".join(errores)
    return True, ""

def validar_swap(tasa_fija, sofr):
    min_swap = round(sofr * 100 + 0.30, 2)
    max_swap = round(sofr * 100 + 2.50, 2)
    if tasa_fija < min_swap:
        return False, (f"Tasa fija {tasa_fija:.2f}% imposible — ningún banco acepta menos de "
                       f"SOFR+0.30% ({min_swap:.2f}%). El banco perdería dinero en este contrato.")
    if tasa_fija > max_swap:
        return False, (f"Tasa fija {tasa_fija:.2f}% irrazonable — pagarías más que la tasa variable "
                       f"proyectada. Máximo razonable: {max_swap:.2f}%.")
    return True, ""

# ── ANÁLISIS DEL PERDEDOR ──
def analisis_perdedor(tipo, res, caso, spot_futuro, sofr, fwd_ref, prima_bs=None):
    ahorro    = res["ahorro"]
    flujo_mes = max((caso["monto_eur"] * spot_futuro) / caso["plazo_meses"], 1)
    lineas    = []

    # Error de instrumento
    if tipo == "Swap de Tasa de Interés" and caso["riesgo_principal"] == "cambiario":
        perdida_expo = caso["monto_eur"] * abs(spot_futuro - spot_actual)
        meses_expo   = perdida_expo / flujo_mes
        lineas.append(
            f"**❌ Error de diagnóstico — instrumento incorrecto para este riesgo.**\n\n"
            f"El fideicomiso tenía exposición cambiaria (variación del EUR/USD), no de tasa de interés. "
            f"El swap fija pagos de intereses sobre deuda en dólares — pero no protege el costo de "
            f"comprar euros. El fideicomiso quedó completamente desprotegido frente al movimiento "
            f"cambiario y absorbió una pérdida de **${perdida_expo:,.0f}** — equivalente a "
            f"**{meses_expo:.1f} meses** del flujo operativo del fideicomiso."
        )
    elif tipo in ["Forward Cambiario", "Opción sobre Divisas"] and caso["riesgo_principal"] == "tasa":
        lineas.append(
            f"**❌ Error de diagnóstico — instrumento incorrecto para este riesgo.**\n\n"
            f"El fideicomiso tenía exposición a tasa de interés variable (SOFR), no cambiaria. "
            f"Un forward o una opción sobre divisas no modifica los pagos de intereses de la deuda. "
            f"El riesgo real quedó sin cubrir."
        )
    else:
        # Instrumento correcto pero mal calibrado
        if tipo == "Forward Cambiario":
            tasa_usada = res["con"] / caso["monto_eur"]
            desvio     = tasa_usada - fwd_ref
            if desvio > 0.008:
                sobrepago   = desvio * caso["monto_eur"]
                meses_sobre = sobrepago / flujo_mes
                lineas.append(
                    f"**⚠️ Calibración costosa — forward mal negociado.**\n\n"
                    f"El forward fue contratado a {tasa_usada:.4f} cuando el precio justo de mercado "
                    f"era {fwd_ref:.4f}. Ese exceso de **${sobrepago:,.0f}** se pagó al banco sin necesidad "
                    f"— representa **{meses_sobre:.1f} meses** de flujo del fideicomiso que se perdieron "
                    f"por no haber negociado correctamente."
                )

        if tipo == "Opción sobre Divisas" and prima_bs is not None:
            prima_usada = res["prima_total"] / caso["monto_eur"]
            if prima_usada > prima_bs * 1.4:
                sobrepago   = (prima_usada - prima_bs) * caso["monto_eur"]
                meses_sobre = sobrepago / flujo_mes
                lineas.append(
                    f"**⚠️ Prima excesiva — seguro sobrevaluado.**\n\n"
                    f"La prima pagada fue ${prima_usada:.4f}/€ cuando Black-Scholes indica "
                    f"${prima_bs:.4f}/€ como valor teórico de mercado. "
                    f"El sobrepago de **${sobrepago:,.0f}** en la prima sola "
                    f"representa **{meses_sobre:.1f} meses** del flujo del fideicomiso "
                    f"que se entregaron al banco sin justificación técnica."
                )

    # Consecuencia narrativa final
    if ahorro < 0:
        meses_perdida = abs(ahorro) / flujo_mes
        lineas.append(
            f"**📉 Impacto en el fideicomiso: la cobertura generó una pérdida adicional.**\n\n"
            f"En lugar de proteger al fideicomiso, esta estrategia empeoró su situación en "
            f"**${abs(ahorro):,.0f}** frente a no haberse cubierto. Eso equivale a "
            f"**{meses_perdida:.1f} meses** del flujo operativo del fideicomiso — recursos que los "
            f"beneficiarios o acreedores no recibirán por una decisión financiera incorrecta."
        )
    elif ahorro < res["sin"] * 0.02:
        meses_desc = (res["sin"] - ahorro) / flujo_mes
        lineas.append(
            f"**📉 Protección insuficiente — el fideicomiso quedó mayormente expuesto.**\n\n"
            f"La cobertura apenas neutralizó el {ahorro/max(res['sin'],1)*100:.1f}% del riesgo real. "
            f"El {100 - ahorro/max(res['sin'],1)*100:.1f}% restante — equivalente a "
            f"**{meses_desc:.1f} meses** de flujo — quedó sin protección. En un fideicomiso real, "
            f"esa exposición no cubierta habría afectado directamente la capacidad de pago a beneficiarios."
        )
    else:
        meses_dif = abs(ahorro) / flujo_mes if ahorro > 0 else 0
        lineas.append(
            f"**📊 Resultado aceptable pero superado por la estrategia ganadora.**\n\n"
            f"La cobertura funcionó y protegió ${ahorro:,.0f} del fideicomiso "
            f"({meses_dif:.1f} meses de flujo), pero la estrategia rival fue significativamente "
            f"más eficiente. En un comité de inversión real, esta diferencia habría puesto en "
            f"cuestión el criterio técnico del gestor."
        )

    return lineas

# ── BLOQUES DE FÓRMULA ──
def formula_forward(spot, r_usd, r_eur, dias, tasa_fwd, nocional, spot_fut):
    fwd_calc  = spot * (1 + r_usd * dias/365) / (1 + r_eur * dias/365)
    costo_con = nocional * tasa_fwd
    costo_sin = nocional * spot_fut
    ahorro    = costo_sin - costo_con
    color_ah  = "#16a34a" if ahorro >= 0 else "#dc2626"
    signo     = "ahorras" if ahorro >= 0 else "pagas de más"
    return f"""
<div class="formula-box">
  <div class="ftitle">📐 Fórmula aplicada — Paridad de Tasas de Interés</div>
  <span class="fmath">Forward = Spot × (1 + tasa_USD × días/365) ÷ (1 + tasa_EUR × días/365)</span>
  <span class="fmath">Forward = {spot:.4f} × (1 + {r_usd:.4f} × {dias}/365) ÷ (1 + {r_eur:.4f} × {dias}/365) = <b>{fwd_calc:.4f}</b></span>
  <div class="fexplain">
    ✏️ <b>¿Qué nos dice esta fórmula?</b> El precio "justo" de mercado para comprar euros en {dias} días
    es <b>{fwd_calc:.4f} USD por euro</b>. Si fijas el forward a <b>{tasa_fwd:.4f}</b>,
    pagarás <b>${costo_con:,.0f}</b> en total — sin importar lo que haga el mercado.<br>
    En el escenario simulado, sin forward habrías pagado <b>${costo_sin:,.0f}</b>.
    Resultado: <span style="color:{color_ah};font-weight:700">${abs(ahorro):,.0f} ({signo})</span>
  </div>
</div>"""

def formula_opcion(S, K, T_years, r, sigma, nocional, prima_usada, spot_fut):
    prima_bs     = black_scholes_call(S, K, T_years, r, sigma)
    prima_tot    = prima_usada * nocional
    prima_bs_tot = prima_bs * nocional
    if T_years > 0 and sigma > 0:
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T_years) / (sigma*np.sqrt(T_years))
        d2 = d1 - sigma*np.sqrt(T_years)
    else:
        d1 = d2 = 0.0
    ejercida         = spot_fut > K
    estado           = "✅ ejercida — el seguro te protegió" if ejercida else "❌ no ejercida — el mercado no llegó al tope"
    diferencia_prima = prima_usada - prima_bs
    color_prima      = "#dc2626" if diferencia_prima > 0.005 else "#16a34a"
    juicio_prima     = "pagaste MÁS de lo que valía el seguro" if diferencia_prima > 0.005 else "pagaste un precio razonable"
    return f"""
<div class="formula-box">
  <div class="ftitle">📐 Fórmula aplicada — Black-Scholes (Precio Teórico del Seguro)</div>
  <span class="fmath">d1 = [ln(S/K) + (r + σ²/2) × T] ÷ (σ × √T)</span>
  <span class="fmath">Prima = S × N(d1) − K × e^(−rT) × N(d2)</span>
  <span class="fmath">d1 = {d1:.4f} | d2 = {d2:.4f}</span>
  <span class="fmath">Prima teórica = <b>${prima_bs:.4f}/euro</b> → por €{nocional:,} = <b>${prima_bs_tot:,.0f}</b></span>
  <div class="fexplain">
    ✏️ <b>¿Qué nos dice esta fórmula?</b><br>
    • <b>Spot (S):</b> {S:.4f} | <b>Strike (K):</b> {K:.4f} | <b>σ:</b> {sigma*100:.1f}% anual<br>
    • <b>Prima teórica Black-Scholes:</b> ${prima_bs:.4f}/€ = <b>${prima_bs_tot:,.0f}</b> total<br>
    • <b>Prima elegida:</b> ${prima_usada:.4f}/€ = ${prima_tot:,.0f} →
      <span style="color:{color_prima};font-weight:600">{juicio_prima}</span><br>
    • <b>Al vencimiento:</b> opción {estado}
  </div>
</div>"""

def formula_swap(sofr_actual, sofr_fut, tasa_fija, spread, nocional, meses):
    tasa_var_hoy  = sofr_actual + spread
    tasa_var_fut  = sofr_fut/100 + spread
    tasa_fija_tot = tasa_fija/100 + spread
    pago_var      = tasa_var_fut  * nocional * meses/12
    pago_fij      = tasa_fija_tot * nocional * meses/12
    ahorro        = pago_var - pago_fij
    color_ah      = "#16a34a" if ahorro >= 0 else "#dc2626"
    signo         = "ahorras" if ahorro >= 0 else "pagas de más"
    var_val       = var_95(nocional, 1, 0.15, meses/12)
    return f"""
<div class="formula-box">
  <div class="ftitle">📐 Fórmula aplicada — Swap de Tasa de Interés (IRS)</div>
  <span class="fmath">Pago variable = (SOFR + spread) × nocional × meses/12</span>
  <span class="fmath">Pago fijo     = (tasa_fija + spread) × nocional × meses/12</span>
  <span class="fmath">Sin swap: ({sofr_fut:.2f}% + {spread*100:.2f}%) × ${nocional:,} × {meses}/12 = <b>${pago_var:,.0f}</b></span>
  <span class="fmath">Con swap: ({tasa_fija:.2f}% + {spread*100:.2f}%) × ${nocional:,} × {meses}/12 = <b>${pago_fij:,.0f}</b></span>
  <div class="fexplain">
    ✏️ <b>¿Qué nos dice esta fórmula?</b><br>
    • Tasa variable hoy: <b>{tasa_var_hoy*100:.2f}%</b> → al vencimiento: <b>{tasa_var_fut*100:.2f}%</b><br>
    • Con el swap fijaste el pago en <b>{tasa_fija_tot*100:.2f}%</b> sin importar lo que pasara<br>
    • Resultado: <span style="color:{color_ah};font-weight:700">{signo} ${abs(ahorro):,.0f}</span> vs. no haberse cubierto<br>
    • <b>VaR 95%</b> (máxima pérdida esperada): <b>${var_val:,.0f}</b>
  </div>
</div>"""

# ── GRÁFICOS ──
def base_layout(titulo, subtitulo):
    return dict(
        title=dict(text=f"<b>{titulo}</b><br><span style='font-size:11px;color:#666'>{subtitulo}</span>",
                   font=dict(size=13, family="DM Sans"), x=0, xanchor="left"),
        height=260, plot_bgcolor="#fff", paper_bgcolor="#fff",
        showlegend=True, margin=dict(t=58, b=50, l=55, r=16),
        font=dict(family="DM Sans", size=11),
        legend=dict(orientation="h", y=-0.28, x=0, font=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0", tickprefix="$", tickformat=",.0f"),
        xaxis=dict(showgrid=False),
        hovermode="x unified",
    )

def grafico_forward(nocional, tasa_fwd, spot_fut, spot_act):
    spots = np.linspace(0.90, 1.40, 150)
    c_sin = spot_fut * nocional
    c_con = tasa_fwd * nocional
    dif   = c_sin - c_con
    fig   = go.Figure()
    fig.add_scatter(x=spots, y=spots*nocional, name="Sin protección",
                    line=dict(color="#dc2626", width=3))
    fig.add_scatter(x=spots, y=np.full_like(spots, tasa_fwd*nocional),
                    name=f"Con forward {tasa_fwd:.4f}", line=dict(color="#16a34a", width=3))
    fig.add_scatter(x=[spot_fut], y=[c_sin], mode="markers+text",
                    marker=dict(color="#dc2626", size=12, line=dict(width=2, color="white")),
                    text=[f"${c_sin:,.0f}"], textposition="top center",
                    textfont=dict(size=11, color="#dc2626"), name="Sin forward")
    fig.add_scatter(x=[spot_fut], y=[c_con], mode="markers+text",
                    marker=dict(color="#16a34a", size=12, line=dict(width=2, color="white")),
                    text=[f"${c_con:,.0f}"], textposition="bottom center",
                    textfont=dict(size=11, color="#16a34a"), name="Con forward")
    fig.add_vline(x=spot_fut, line_dash="dash", line_color="#9ca3af", line_width=1.3)
    subt = f"El forward te {'ahorra' if dif>=0 else 'cuesta'} ${abs(dif):,.0f} en este escenario"
    fig.update_layout(**base_layout("¿Cuánto pagarías por los euros?", subt))
    fig.update_xaxes(title="Si el euro terminara valiendo esto →")
    fig.update_yaxes(title="Costo total (USD)")
    return fig

def grafico_opcion(nocional, strike, prima, spot_fut, spot_act):
    spots     = np.linspace(0.90, 1.40, 150)
    prima_tot = prima * nocional
    con_op    = np.where(spots > strike, strike*nocional+prima_tot, spots*nocional+prima_tot)
    c_sin     = spot_fut * nocional
    ejercida  = spot_fut > strike
    c_con     = (strike*nocional+prima_tot) if ejercida else (spot_fut*nocional+prima_tot)
    dif       = c_sin - c_con
    fig       = go.Figure()
    fig.add_scatter(x=spots, y=spots*nocional, name="Sin protección",
                    line=dict(color="#dc2626", width=3))
    fig.add_scatter(x=spots, y=con_op, name=f"Con opción (tope {strike:.4f})",
                    line=dict(color="#16a34a", width=3))
    fig.add_scatter(x=[spot_fut], y=[c_sin], mode="markers+text",
                    marker=dict(color="#dc2626", size=12, line=dict(width=2, color="white")),
                    text=[f"${c_sin:,.0f}"], textposition="top center",
                    textfont=dict(size=11, color="#dc2626"), name="Sin opción")
    fig.add_scatter(x=[spot_fut], y=[c_con], mode="markers+text",
                    marker=dict(color="#16a34a", size=12, line=dict(width=2, color="white")),
                    text=[f"${c_con:,.0f}"], textposition="bottom center",
                    textfont=dict(size=11, color="#16a34a"),
                    name=f"Con opción {'(ejercida)' if ejercida else '(no ejercida)'}")
    fig.add_vline(x=spot_fut, line_dash="dash", line_color="#9ca3af", line_width=1.3)
    fig.add_vline(x=strike, line_dash="dot", line_color="#2563eb", line_width=1.2,
                  annotation_text=" tope máximo", annotation_font_size=9,
                  annotation_font_color="#2563eb")
    subt = f"La opción te {'protege, ahorras' if dif>=0 else 'cuesta'} ${abs(dif):,.0f} en este escenario"
    fig.update_layout(**base_layout("¿Cuándo conviene usar el seguro de tipo de cambio?", subt))
    fig.update_xaxes(title="Si el euro terminara valiendo esto →")
    fig.update_yaxes(title="Costo total (USD)")
    return fig

def grafico_swap(nocional, tasa_fija, spread, meses, sofr_fut):
    sofrs   = np.linspace(1.0, 9.0, 120)
    fij_pay = (tasa_fija/100 + spread) * nocional * meses/12
    p_var   = (sofr_fut/100 + spread) * nocional * meses/12
    dif     = p_var - fij_pay
    fig     = go.Figure()
    fig.add_scatter(x=sofrs, y=(sofrs/100+spread)*nocional*meses/12,
                    name="Sin protección", line=dict(color="#dc2626", width=3))
    fig.add_scatter(x=sofrs, y=np.full_like(sofrs, fij_pay),
                    name=f"Con swap {tasa_fija:.2f}%", line=dict(color="#16a34a", width=3))
    fig.add_scatter(x=[sofr_fut], y=[p_var], mode="markers+text",
                    marker=dict(color="#dc2626", size=12, line=dict(width=2, color="white")),
                    text=[f"${p_var:,.0f}"], textposition="top center",
                    textfont=dict(size=11, color="#dc2626"), name="Sin swap")
    fig.add_scatter(x=[sofr_fut], y=[fij_pay], mode="markers+text",
                    marker=dict(color="#16a34a", size=12, line=dict(width=2, color="white")),
                    text=[f"${fij_pay:,.0f}"], textposition="bottom center",
                    textfont=dict(size=11, color="#16a34a"), name="Con swap")
    fig.add_vline(x=sofr_fut, line_dash="dash", line_color="#9ca3af", line_width=1.3)
    subt = f"El swap te {'ahorra' if dif>=0 else 'cuesta'} ${abs(dif):,.0f} en este escenario"
    fig.update_layout(**base_layout("¿Cuánto pagarías de intereses?", subt))
    fig.update_xaxes(title="Si la tasa terminara en este nivel →", ticksuffix="%")
    fig.update_yaxes(title="Pago de intereses (USD)")
    return fig

# ── PERFILES ──
PERFILES = {
    "Forward Cambiario": {
        "nombre": "El Estratega Conservador", "icono": "🛡️",
        "desc": ("Prefieres certeza sobre flexibilidad. Cuando identificas un riesgo lo neutralizas "
                 "de forma directa y sin ambigüedades. Tu perfil financiero se inclina hacia la "
                 "planificación metódica: fijas condiciones hoy para no depender del azar mañana. "
                 "Ideal en contextos de alta incertidumbre cambiaria donde el costo de equivocarse "
                 "supera el costo de la cobertura."),
    },
    "Opción sobre Divisas": {
        "nombre": "El Analista de Oportunidades", "icono": "🎯",
        "desc": ("Entiendes que el mercado puede moverse a tu favor o en tu contra y pagas por "
                 "conservar esa posibilidad. Tu perfil combina gestión del riesgo con apertura a "
                 "beneficiarte si el escenario es favorable. Limitas pérdidas sin renunciar a "
                 "ganancias potenciales. Perfil típico de un CFO moderno en empresas con flujos variables."),
    },
    "Swap de Tasa de Interés": {
        "nombre": "El Gestor de Flujos", "icono": "📊",
        "desc": ("Tu foco está en la previsibilidad del flujo de caja. Sabes que una tasa variable "
                 "es una incógnita incontrolable dentro de tu modelo de negocio y prefieres eliminarla. "
                 "Perfil disciplinado que valora la estabilidad operativa sobre la especulación. "
                 "Ideal en fideicomisos con compromisos de pago a largo plazo."),
    },
}

def comentario_velocidad(segundos):
    if segundos is None:
        return ""
    if segundos < 15:
        return ("⚡ <b>Decidió en menos de 15 segundos</b> — Una reacción así revela intuición financiera "
                "entrenada. En mercados reales los mejores operadores no dudan: analizan rápido y ejecutan. "
                "Esta lucidez bajo presión es una ventaja competitiva real.")
    elif segundos < 35:
        return (f"🕐 <b>Decidió en {int(segundos)} segundos</b> — Tomó el tiempo justo para analizar sin "
                "sobrepensar. En finanzas la parálisis por análisis cuesta tanto como la impulsividad. "
                "Este equilibrio entre reflexión y acción es el sello de un buen gestor.")
    else:
        return (f"🕐 <b>Decidió en {int(segundos)} segundos</b> — Fue meticuloso antes de comprometerse. "
                "En fideicomisos reales una decisión mal ejecutada puede costar cientos de miles. "
                "La prudencia tiene su valor, aunque en mercados volátiles la ventana puede cerrarse.")

def puntaje(tipo, res, spot_fut, nocional, riesgo_principal):
    p = 0; d = []
    ahorro = res["ahorro"]
    ref = nocional * abs(spot_fut - fwd_ref) if tipo != "Swap de Tasa de Interés" else max(res["sin"], 1)
    if ahorro > 0:
        p += min(40, int(40 * ahorro / max(ref, 1)))
        d.append(f"✅ Protegió **${ahorro:,.0f}** del riesgo real")
    else:
        d.append(f"❌ Generó pérdida adicional de **${abs(ahorro):,.0f}**")
    if tipo == "Opción sobre Divisas":
        prima = res.get("prima_total", 0); prot = max(ahorro, 1)
        if prima < prot * 0.20:
            p += 30; d.append("✅ Prima muy eficiente — bajo costo, alta protección")
        elif prima < prot:
            p += 18; d.append("⚠️ Prima razonable pero con costos evitables")
        else:
            p += 4;  d.append("❌ Prima más cara que el riesgo que cubría")
    else:
        p += 25; d.append("✅ Sin prima — costo directo y controlado")
    if riesgo_principal == "cambiario":
        if tipo in ["Forward Cambiario", "Opción sobre Divisas"]:
            p += 30; d.append("✅ Instrumento correcto para el **riesgo cambiario** del caso")
        else:
            p += 10; d.append("❌ El swap cubre tasa de interés — este caso era de **riesgo cambiario**")
    else:
        if tipo == "Swap de Tasa de Interés":
            p += 30; d.append("✅ Instrumento correcto para el **riesgo de tasa** del caso")
        else:
            p += 10; d.append("❌ Forward/Opción cubren tipo de cambio — este caso era de **riesgo de tasa**")
    return min(p, 100), d

# ── ESTADO DE SESIÓN ──
defaults = {
    "seed": random.randint(0,9999),
    "start_time": time.time(),
    "sim_a": None, "sim_b": None,
    "listo_a": False, "listo_b": False,
    "inst_a_final": None, "inst_b_final": None,
    "res_a_final": None,  "res_b_final": None,
    "prima_bs_a": None,   "prima_bs_b": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

fwd_ref     = forward_teorico(spot_actual, sofr, 0.04, 180)
tasa_hoy    = (sofr + 0.02) * 100
lista_casos = casos_narrativos(spot_actual, fwd_ref, tasa_hoy, volatilidad)
rng_caso    = random.Random(st.session_state.seed)
caso        = rng_caso.choice(lista_casos)
fwd_ref     = forward_teorico(spot_actual, sofr, 0.04, caso["plazo_meses"] * 30)
tasa_hoy    = (sofr + caso["spread"]) * 100
plazo_txt   = f"{caso['plazo_meses']} {'mes' if caso['plazo_meses']==1 else 'meses'}"
T_years     = caso["plazo_meses"] / 12

# Rangos de sliders según mercado
fw_min  = round(fwd_ref - 0.04, 3)
fw_max  = round(fwd_ref + 0.08, 3)
sw_min  = round(sofr*100 + 0.30, 2)
sw_max  = round(sofr*100 + 2.50, 2)
prima_bs_ref = black_scholes_call(spot_actual, spot_actual, T_years, sofr, volatilidad)
pr_min  = round(max(0.010, prima_bs_ref * 0.5), 3)
pr_max  = round(prima_bs_ref * 2.5 + 0.001, 3)
str_min = round(spot_actual - 0.01, 3)
str_max = round(spot_actual + 0.08, 3)

# ── ENCABEZADO ──
hc1, hc2 = st.columns([6, 2])
with hc1:
    st.markdown("""<div class="top-header">
        <h1>Simulador de Coberturas Financieras</h1>
        <p>Derivados aplicados a fideicomisos con riesgo cambiario y de tasas — duelo en vivo</p>
    </div>""", unsafe_allow_html=True)
with hc2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↻  Nuevo caso aleatorio"):
        for k in list(defaults.keys()):
            st.session_state.pop(k, None)
        st.session_state.seed       = random.randint(0, 9999)
        st.session_state.start_time = time.time()
        st.rerun()

# ── SECCIÓN 1 — CASO ──
st.markdown('<div class="step-badge">Situación 01</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">El caso a resolver</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Lee la situación con atención. El cronómetro corre desde ahora.</div>', unsafe_allow_html=True)

perdida_estimada = caso["monto_eur"] * spot_actual * 0.07

st.markdown(f'<div class="case-card"><div class="case-label">{caso["sector"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="case-title">{caso["emoji"]} {caso["titulo"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="case-narrative">{caso["narrativa"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="case-problema">{caso["problema"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="case-pregunta">🤔 {caso["pregunta"]}</div>', unsafe_allow_html=True)
impacto_fx   = caso["monto_eur"] * (fwd_ref - spot_actual)
impacto_tasa = caso["deuda_usd"] * (sofr + 0.02) * caso["plazo_meses"] / 12
mov_posible  = spot_actual * volatilidad

st.markdown(f"""
<div class="pill-row">
    <div class="pill">EUR/USD hoy: <b>{spot_actual:.4f}</b></div>
    <div class="pill">Forward {plazo_txt}: <b>{fwd_ref:.4f}</b></div>
    <div class="pill">Tasa variable hoy: <b>{tasa_hoy:.2f}%</b></div>
    <div class="pill">Volatilidad EUR/USD: <b>{volatilidad*100:.1f}% anual</b></div>
    <div class="pill-alert">⚠️ Pérdida potencial estimada: ${perdida_estimada:,.0f}</div>
</div>
<div style="margin-top:1rem;padding:0.9rem 1.2rem;background:#fafafa;border-radius:4px;
            border:1px solid #e0e0e0;font-size:0.88rem;line-height:1.9;color:#333;">
    <b>¿Qué significan estos números para el fideicomiso?</b><br>
    • <b>EUR/USD hoy ({spot_actual:.4f}):</b> por cada euro que el fideicomiso debe pagar,
      hoy necesita <b>${spot_actual:.4f} dólares</b>. Si el euro sube, ese costo aumenta automáticamente.<br>
    • <b>Forward teórico ({fwd_ref:.4f}):</b> el precio "justo" calculado por la fórmula de paridad de tasas
      para comprar euros en {plazo_txt}. Un buen forward debe estar cerca de este valor —
      alejarse demasiado significa pagar de más o que el banco lo rechace.<br>
    • <b>Volatilidad {volatilidad*100:.1f}% anual:</b> el euro puede moverse hasta
      <b>±${mov_posible:.4f}</b> por euro en un año según su comportamiento histórico.
      A mayor volatilidad, mayor urgencia de cubrirse.<br>
    • <b>Tasa variable {tasa_hoy:.2f}%:</b> lo que el fideicomiso paga hoy por su deuda.
      Si el SOFR sube 1 punto, los pagos aumentan en
      <b>${caso['deuda_usd']*0.01*caso['plazo_meses']/12:,.0f}</b> adicionales en {plazo_txt}.<br>
    • <b>Pérdida potencial ${perdida_estimada:,.0f}:</b> si el euro sube un 7% —
      un movimiento dentro de lo históricamente normal — y el fideicomiso no tiene cobertura,
      ese dinero simplemente desaparece del presupuesto.
</div>
</div>
""", unsafe_allow_html=True)

# ── SECCIÓN 2 — ESCENARIO ──
st.markdown('<div class="step-badge">Situación 02 — Solo para el presentador</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎬 Revela qué pasó con el mercado</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="section-sub">
<b>Esta sección la controla únicamente el presentador</b> — los participantes deciden sin conocer este resultado.
Mueve los sliders para revelar qué pasó {plazo_txt} después.<br><br>
👉 <b>Slider 1:</b> mueve hacia la derecha si el euro se encareció, hacia la izquierda si se abarató.<br>
👉 <b>Slider 2:</b> mueve hacia la derecha si las tasas subieron, hacia la izquierda si bajaron.
</div>
""", unsafe_allow_html=True)

sc1, sc2 = st.columns(2)
with sc1:
    st.markdown("**💶 ¿Cuánto valió el euro al final del plazo?**")
    spot_futuro = st.slider("euro", 0.90, 1.40, round(spot_actual*1.08, 3), 0.001,
                            label_visibility="collapsed")
    if spot_futuro > spot_actual:
        st.caption(f"📈 El euro subió de ${spot_actual:.4f} a ${spot_futuro:.4f} — comprar euros cuesta más")
    else:
        st.caption(f"📉 El euro bajó de ${spot_actual:.4f} a ${spot_futuro:.4f} — comprar euros cuesta menos")

with sc2:
    st.markdown("**🏦 ¿En qué nivel terminó la tasa de interés?**")
    sofr_futuro = st.slider("tasa", 1.0, 9.0, round((sofr+0.015)*100, 2), 0.05,
                            label_visibility="collapsed")
    if sofr_futuro > sofr*100:
        st.caption(f"📈 La tasa subió de {sofr*100:.2f}% a {sofr_futuro:.2f}% — la deuda variable es más cara")
    else:
        st.caption(f"📉 La tasa bajó de {sofr*100:.2f}% a {sofr_futuro:.2f}% — la deuda variable es más barata")

var_fx  = (spot_futuro - spot_actual) / spot_actual * 100
var_sof = sofr_futuro - sofr*100
imp_sin = caso["monto_eur"] * (spot_futuro - spot_actual)
tasa_vf = sofr_futuro/100 + caso["spread"]

st.markdown("<br>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("EUR/USD al vencer",     f"{spot_futuro:.4f}", f"{var_fx:+.2f}%")
m2.metric("Tasa al vencer",        f"{sofr_futuro:.2f}%", f"{var_sof:+.2f} pb")
m3.metric("Impacto sin cobertura", f"${imp_sin:+,.0f}", delta_color="inverse")
m4.metric("Tasa variable final",   f"{tasa_vf*100:.2f}%",
          f"{(tasa_vf-sofr-caso['spread'])*100:+.2f}%", delta_color="inverse")

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── SECCIÓN 3 — PANELES ──
st.markdown('<div class="step-badge">Decisión 03</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Elige y calibra tu estrategia</div>', unsafe_allow_html=True)
st.markdown("""<div class="section-sub">
Cada participante elige su instrumento, revisa la fórmula con los números reales del caso
y ajusta los parámetros dentro de rangos reales de mercado.
Si los parámetros están fuera de rango, el banco no aprobaría el contrato y el botón se bloquea.
</div>""", unsafe_allow_html=True)

INSTRUMENTOS = ["Forward Cambiario", "Opción sobre Divisas", "Swap de Tasa de Interés"]
DESCRIPCIONES = {
    "Forward Cambiario":       "🔒 Bloqueas HOY el precio al que comprarás euros en el futuro. Sin sorpresas, sin flexibilidad.",
    "Opción sobre Divisas":    "🛡️ Compras un seguro: el derecho de comprar euros a un precio máximo. Si el euro baja, aprovechas el mercado.",
    "Swap de Tasa de Interés": "🔄 Cambias tu deuda de tasa variable a tasa fija. Sabes exactamente cuánto pagarás cada mes.",
}
PISTAS = {
    "cambiario": "💡 Este caso tiene riesgo cambiario — el Forward o la Opción son los instrumentos indicados.",
    "tasa":      "💡 Este caso tiene riesgo de tasa de interés — el Swap es el instrumento indicado.",
}
st.info(PISTAS[caso["riesgo_principal"]])

col_a, col_b = st.columns(2)

# ── PANEL A ──
with col_a:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🔵 Participante A</div>', unsafe_allow_html=True)

    inst_bloqueado_a = st.session_state.get("inst_b_final") if st.session_state.listo_b else None
    opciones_a = [i for i in INSTRUMENTOS if i != inst_bloqueado_a]
    if inst_bloqueado_a:
        st.warning(f"El instrumento **{inst_bloqueado_a}** ya fue tomado por el Participante B — elige una estrategia diferente.")
    inst_a = st.selectbox("Instrumento", opciones_a, key="inst_a")
    st.caption(DESCRIPCIONES[inst_a])
    valido_a   = True
    aviso_a    = ""
    prima_bs_a = None

    if inst_a == "Forward Cambiario":
        fw_a = st.slider("¿A qué precio fijas el euro?", fw_min, fw_max,
                         round(min(max(fwd_ref, fw_min), fw_max), 3), 0.001, key="fw_a",
                         help=f"Precio justo de mercado: {fwd_ref:.4f} | Rango aceptable: {fw_min}–{fw_max}")
        valido_a, aviso_a = validar_forward(fw_a, fwd_ref)
        res_a  = calc_forward(spot_futuro, fw_a, caso["monto_eur"])
        st.markdown(formula_forward(spot_actual, sofr, 0.04,
                    caso["plazo_meses"]*30, fw_a, caso["monto_eur"], spot_futuro), unsafe_allow_html=True)
        fig_a  = grafico_forward(caso["monto_eur"], fw_a, spot_futuro, spot_actual)

    elif inst_a == "Opción sobre Divisas":
        prima_bs_a = black_scholes_call(spot_actual, spot_actual, T_years, sofr, volatilidad)
        str_a = st.slider("Strike — precio máximo que aceptas pagar por euro",
                          str_min, str_max,
                          round(min(max(spot_actual, str_min), str_max), 3), 0.001, key="str_a")
        pri_a = st.slider("Prima — costo del seguro por euro (USD)",
                          pr_min, pr_max,
                          round(min(max(prima_bs_a, pr_min), pr_max), 3), 0.001, key="pri_a")
        valido_a, aviso_a = validar_opcion(str_a, spot_actual, pri_a, prima_bs_a)
        res_a  = calc_opcion(spot_futuro, str_a, pri_a, caso["monto_eur"])
        st.markdown(formula_opcion(spot_actual, str_a, T_years, sofr,
                    volatilidad, caso["monto_eur"], pri_a, spot_futuro), unsafe_allow_html=True)
        fig_a  = grafico_opcion(caso["monto_eur"], str_a, pri_a, spot_futuro, spot_actual)

    else:
        tf_a = st.slider("Tasa fija que propones (%)", sw_min, sw_max,
                         round(min(max(sofr*100+0.80, sw_min), sw_max), 2), 0.05, key="tf_a",
                         help=f"Rango aceptable para el banco: {sw_min}% – {sw_max}%")
        valido_a, aviso_a = validar_swap(tf_a, sofr)
        res_a  = calc_swap(sofr_futuro, tf_a, caso["spread"], caso["deuda_usd"], caso["plazo_meses"])
        st.markdown(formula_swap(sofr, sofr_futuro, tf_a, caso["spread"],
                    caso["deuda_usd"], caso["plazo_meses"]), unsafe_allow_html=True)
        fig_a  = grafico_swap(caso["deuda_usd"], tf_a, caso["spread"], caso["plazo_meses"], sofr_futuro)

    st.plotly_chart(fig_a, use_container_width=True, config={"displayModeBar": False})

    if not valido_a:
        st.error(f"⛔ **Parámetros rechazados por el banco**\n\n{aviso_a}\n\n"
                 f"⚠️ Ajusta los valores para habilitar la simulación.")

    ahorro_a = res_a["ahorro"]
    cls_a    = "pos" if ahorro_a >= 0 else "neg"
    etiq_a   = "Ahorro vs. sin cobertura" if ahorro_a >= 0 else "Pérdida adicional"
    st.markdown(f"""
    <div style="padding-top:0.8rem;border-top:1.5px solid #e0e0e0">
        <div class="resultado-label">Sin cobertura pagarías</div>
        <div class="resultado-num">${res_a['sin']:,.0f}</div>
        <div class="resultado-label">Con tu cobertura pagas</div>
        <div class="resultado-num">${res_a['con']:,.0f}</div>
        <div class="resultado-label">{etiq_a}</div>
        <div class="resultado-num {cls_a}">${ahorro_a:+,.0f}</div>
    </div>""", unsafe_allow_html=True)

    if inst_a == "Opción sobre Divisas":
        if res_a["ejercida"]:
            st.success("✅ Opción ejercida — el seguro funcionó")
        else:
            st.warning("⚠️ Opción no ejercida — pagaste prima sin usarla")

    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state.listo_a:
        if valido_a:
            if st.button("▶  Simular — Participante A", key="btn_a"):
                st.session_state.sim_a        = time.time() - st.session_state.start_time
                st.session_state.listo_a      = True
                st.session_state.inst_a_final = inst_a
                st.session_state.res_a_final  = res_a
                st.session_state.prima_bs_a   = prima_bs_a
                st.rerun()
        else:
            st.button("▶  Simular — Participante A", key="btn_a", disabled=True)
            st.caption("🔒 Corrige los parámetros para habilitar la simulación.")
    else:
        seg   = st.session_state.sim_a
        cls_t = "timer-fast" if seg < 20 else "timer-slow"
        st.markdown(f'<div class="timer-badge {cls_t}">⏱ Simulado en {seg:.1f}s</div>',
                    unsafe_allow_html=True)
        st.success("✅ Decisión registrada")
    st.markdown('</div>', unsafe_allow_html=True)

# ── PANEL B ──
with col_b:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🟣 Participante B</div>', unsafe_allow_html=True)

    inst_bloqueado_b = st.session_state.get("inst_a_final") if st.session_state.listo_a else None
    opciones_b = [i for i in INSTRUMENTOS if i != inst_bloqueado_b]
    idx_b = min(1, len(opciones_b) - 1)
    if inst_bloqueado_b:
        st.warning(f"El instrumento **{inst_bloqueado_b}** ya fue tomado por el Participante A — elige una estrategia diferente.")
    inst_b = st.selectbox("Instrumento", opciones_b, index=idx_b, key="inst_b")
    st.caption(DESCRIPCIONES[inst_b])
    valido_b   = True
    aviso_b    = ""
    prima_bs_b = None

    if inst_b == "Forward Cambiario":
        fw_b = st.slider("¿A qué precio fijas el euro?", fw_min, fw_max,
                         round(min(max(fwd_ref*1.01, fw_min), fw_max), 3), 0.001, key="fw_b",
                         help=f"Precio justo de mercado: {fwd_ref:.4f} | Rango aceptable: {fw_min}–{fw_max}")
        valido_b, aviso_b = validar_forward(fw_b, fwd_ref)
        res_b  = calc_forward(spot_futuro, fw_b, caso["monto_eur"])
        st.markdown(formula_forward(spot_actual, sofr, 0.04,
                    caso["plazo_meses"]*30, fw_b, caso["monto_eur"], spot_futuro), unsafe_allow_html=True)
        fig_b  = grafico_forward(caso["monto_eur"], fw_b, spot_futuro, spot_actual)

    elif inst_b == "Opción sobre Divisas":
        prima_bs_b = black_scholes_call(spot_actual, spot_actual, T_years, sofr, volatilidad)
        str_b = st.slider("Strike — precio máximo que aceptas pagar por euro",
                          str_min, str_max,
                          round(min(max(spot_actual*1.01, str_min), str_max), 3), 0.001, key="str_b")
        pri_b = st.slider("Prima — costo del seguro por euro (USD)",
                          pr_min, pr_max,
                          round(min(max(prima_bs_b*1.2, pr_min), pr_max), 3), 0.001, key="pri_b")
        valido_b, aviso_b = validar_opcion(str_b, spot_actual, pri_b, prima_bs_b)
        res_b  = calc_opcion(spot_futuro, str_b, pri_b, caso["monto_eur"])
        st.markdown(formula_opcion(spot_actual, str_b, T_years, sofr,
                    volatilidad, caso["monto_eur"], pri_b, spot_futuro), unsafe_allow_html=True)
        fig_b  = grafico_opcion(caso["monto_eur"], str_b, pri_b, spot_futuro, spot_actual)

    else:
        tf_b = st.slider("Tasa fija que propones (%)", sw_min, sw_max,
                         round(min(max(sofr*100+1.20, sw_min), sw_max), 2), 0.05, key="tf_b",
                         help=f"Rango aceptable para el banco: {sw_min}% – {sw_max}%")
        valido_b, aviso_b = validar_swap(tf_b, sofr)
        res_b  = calc_swap(sofr_futuro, tf_b, caso["spread"], caso["deuda_usd"], caso["plazo_meses"])
        st.markdown(formula_swap(sofr, sofr_futuro, tf_b, caso["spread"],
                    caso["deuda_usd"], caso["plazo_meses"]), unsafe_allow_html=True)
        fig_b  = grafico_swap(caso["deuda_usd"], tf_b, caso["spread"], caso["plazo_meses"], sofr_futuro)

    st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})

    if not valido_b:
        st.error(f"⛔ **Parámetros rechazados por el banco**\n\n{aviso_b}\n\n"
                 f"⚠️ Ajusta los valores para habilitar la simulación.")

    ahorro_b = res_b["ahorro"]
    cls_b    = "pos" if ahorro_b >= 0 else "neg"
    etiq_b   = "Ahorro vs. sin cobertura" if ahorro_b >= 0 else "Pérdida adicional"
    st.markdown(f"""
    <div style="padding-top:0.8rem;border-top:1.5px solid #e0e0e0">
        <div class="resultado-label">Sin cobertura pagarías</div>
        <div class="resultado-num">${res_b['sin']:,.0f}</div>
        <div class="resultado-label">Con tu cobertura pagas</div>
        <div class="resultado-num">${res_b['con']:,.0f}</div>
        <div class="resultado-label">{etiq_b}</div>
        <div class="resultado-num {cls_b}">${ahorro_b:+,.0f}</div>
    </div>""", unsafe_allow_html=True)

    if inst_b == "Opción sobre Divisas":
        if res_b["ejercida"]:
            st.success("✅ Opción ejercida — el seguro funcionó")
        else:
            st.warning("⚠️ Opción no ejercida — pagaste prima sin usarla")

    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state.listo_b:
        if valido_b:
            if st.button("▶  Simular — Participante B", key="btn_b"):
                st.session_state.sim_b        = time.time() - st.session_state.start_time
                st.session_state.listo_b      = True
                st.session_state.inst_b_final = inst_b
                st.session_state.res_b_final  = res_b
                st.session_state.prima_bs_b   = prima_bs_b
                st.rerun()
        else:
            st.button("▶  Simular — Participante B", key="btn_b", disabled=True)
            st.caption("🔒 Corrige los parámetros para habilitar la simulación.")
    else:
        seg   = st.session_state.sim_b
        cls_t = "timer-fast" if seg < 20 else "timer-slow"
        st.markdown(f'<div class="timer-badge {cls_t}">⏱ Simulado en {seg:.1f}s</div>',
                    unsafe_allow_html=True)
        st.success("✅ Decisión registrada")
    st.markdown('</div>', unsafe_allow_html=True)

# ── SECCIÓN 4 — VEREDICTO ──
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

if st.session_state.listo_a and st.session_state.listo_b:
    st.markdown('<div class="step-badge">Resultado 04</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Análisis y veredicto final</div>', unsafe_allow_html=True)

    # Usar resultados guardados al momento de simular
    inst_a_f    = st.session_state.inst_a_final or inst_a
    inst_b_f    = st.session_state.inst_b_final or inst_b
    res_a_f     = st.session_state.res_a_final  or res_a
    res_b_f     = st.session_state.res_b_final  or res_b
    pbs_a       = st.session_state.prima_bs_a
    pbs_b       = st.session_state.prima_bs_b
    ahorro_a_f  = res_a_f["ahorro"]
    ahorro_b_f  = res_b_f["ahorro"]
    seg_a       = st.session_state.sim_a
    seg_b       = st.session_state.sim_b

    pts_a, det_a = puntaje(inst_a_f, res_a_f, spot_futuro, caso["monto_eur"], caso["riesgo_principal"])
    pts_b, det_b = puntaje(inst_b_f, res_b_f, spot_futuro, caso["monto_eur"], caso["riesgo_principal"])

    ga, gb = st.columns(2)
    with ga:
        fig1 = go.Figure()
        fig1.add_bar(x=["🔵 Participante A","🟣 Participante B"], y=[pts_a, pts_b],
                     marker_color=["#0a0a0a","#6b7280"],
                     text=[f"{pts_a} pts",f"{pts_b} pts"],
                     textposition="outside", width=0.4)
        fig1.update_layout(title="Puntaje final", height=260, yaxis_range=[0,115],
                           plot_bgcolor="#fff", paper_bgcolor="#fff", showlegend=False,
                           font=dict(family="DM Sans",size=12), margin=dict(t=36,b=20,l=40,r=16),
                           yaxis=dict(showgrid=True,gridcolor="#f0f0f0"), xaxis=dict(showgrid=False))
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar":False})

    with gb:
        fig2 = go.Figure()
        fig2.add_bar(x=["🔵 Participante A","🟣 Participante B"],
                     y=[ahorro_a_f, ahorro_b_f],
                     marker_color=["#0a0a0a" if ahorro_a_f>=0 else "#dc2626",
                                   "#6b7280" if ahorro_b_f>=0 else "#ef4444"],
                     text=[f"${ahorro_a_f:+,.0f}",f"${ahorro_b_f:+,.0f}"],
                     textposition="outside", width=0.4)
        fig2.update_layout(title="Ahorro vs. no cubrirse", height=260,
                           plot_bgcolor="#fff", paper_bgcolor="#fff", showlegend=False,
                           font=dict(family="DM Sans",size=12), margin=dict(t=36,b=20,l=40,r=16),
                           yaxis=dict(showgrid=True,gridcolor="#f0f0f0",
                                      zeroline=True,zerolinecolor="#0a0a0a",zerolinewidth=1.5),
                           xaxis=dict(showgrid=False))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

    da, db = st.columns(2)
    with da:
        st.markdown(f"**🔵 Participante A — {pts_a}/100** ⏱ {seg_a:.1f}s")
        for d in det_a: st.markdown(d)
    with db:
        st.markdown(f"**🟣 Participante B — {pts_b}/100** ⏱ {seg_b:.1f}s")
        for d in det_b: st.markdown(d)

    st.markdown("<br>", unsafe_allow_html=True)

    if pts_a > pts_b:
        ganador_nom, ganador_tipo = "🔵 Participante A", inst_a_f
        perdedor_nom              = "🟣 Participante B"
        diff                      = pts_a - pts_b
        dif_econ                  = abs(ahorro_a_f - ahorro_b_f)
        seg_gan                   = seg_a
        res_per, tipo_per, pbs_per = res_b_f, inst_b_f, pbs_b
        perfil = PERFILES.get(inst_a_f, PERFILES["Forward Cambiario"])
    elif pts_b > pts_a:
        ganador_nom, ganador_tipo = "🟣 Participante B", inst_b_f
        perdedor_nom              = "🔵 Participante A"
        diff                      = pts_b - pts_a
        dif_econ                  = abs(ahorro_b_f - ahorro_a_f)
        seg_gan                   = seg_b
        res_per, tipo_per, pbs_per = res_a_f, inst_a_f, pbs_a
        perfil = PERFILES.get(inst_b_f, PERFILES["Forward Cambiario"])
    else:
        ganador_nom = None

    if ganador_nom:
        com_vel = comentario_velocidad(seg_gan)
        st.markdown(f"""
<div class="veredicto-card">
    <h2>🏆 ¡{ganador_nom} gana! — {diff} puntos de ventaja</h2>
    <p>
        Excelente decisión. Elegiste <b>{ganador_tipo}</b> y lo aplicaste con criterio
        al riesgo real del fideicomiso. La diferencia económica frente a la estrategia
        rival fue de <b>${dif_econ:,.0f}</b> — dinero real que el fideicomiso conserva
        gracias a tu juicio financiero.<br><br>
        {com_vel}
    </p>
    <div class="perfil">
        <b>{perfil['icono']} Tu perfil financiero: {perfil['nombre']}</b><br><br>
        {perfil['desc']}
    </div>
</div>""", unsafe_allow_html=True)

        # Análisis del perdedor
        st.markdown(f"#### ❌ ¿Qué salió mal — {perdedor_nom}?")
        st.markdown('<div class="perdedor-card"><h4>Diagnóstico de la estrategia perdedora</h4>',
                    unsafe_allow_html=True)
        lineas_perdedor = analisis_perdedor(tipo_per, res_per, caso,
                                            spot_futuro, sofr, fwd_ref, pbs_per)
        for linea in lineas_perdedor:
            st.markdown(linea)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
<div class="empate-card">
    <h3 style="margin:0 0 0.5rem 0">🤝 Empate técnico</h3>
    <p style="margin:0;color:#444;font-size:0.95rem">
        Ambas estrategias tuvieron desempeño equivalente. Genera un nuevo caso o ajusta los parámetros.
    </p>
</div>""", unsafe_allow_html=True)

    if hist_fx is not None:
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown('<div class="step-badge">Contexto 05</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">EUR/USD — último año (datos reales de mercado)</div>',
                    unsafe_allow_html=True)
        fig3 = go.Figure()
        fig3.add_scatter(x=hist_fx.index, y=hist_fx['Close'], name="EUR/USD",
                         line=dict(color="#0a0a0a", width=1.8),
                         fill="tozeroy", fillcolor="rgba(10,10,10,0.04)")
        fig3.add_hline(y=spot_futuro, line_dash="dash", line_color="#dc2626", line_width=1.5,
                       annotation_text=f"  Escenario simulado {spot_futuro:.4f}",
                       annotation_font_color="#dc2626")
        fig3.add_hline(y=spot_actual, line_dash="dot", line_color="#2563eb", line_width=1.5,
                       annotation_text=f"  Hoy {spot_actual:.4f}",
                       annotation_font_color="#2563eb")
        fig3.add_hline(y=fwd_ref, line_dash="dot", line_color="#d97706", line_width=1.5,
                       annotation_text=f"  Forward teórico {fwd_ref:.4f}",
                       annotation_font_color="#d97706")
        fig3.update_layout(height=340, plot_bgcolor="#fff", paper_bgcolor="#fff",
                           showlegend=False, font=dict(family="DM Sans",size=12),
                           margin=dict(t=20,b=20,l=40,r=100),
                           yaxis=dict(showgrid=True,gridcolor="#f0f0f0"),
                           xaxis=dict(showgrid=False))
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})

else:
    pendiente = []
    if not st.session_state.listo_a: pendiente.append("🔵 Participante A")
    if not st.session_state.listo_b: pendiente.append("🟣 Participante B")
    st.info(f"⏳ Esperando que {' y '.join(pendiente)} "
            f"{'presione' if len(pendiente)==1 else 'presionen'} "
            f"**Simular** para revelar el veredicto.")

st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.caption(f"Datos EUR/USD: Yahoo Finance · Black-Scholes con volatilidad histórica real · Caso #{st.session_state.seed}")