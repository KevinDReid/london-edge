"""
London Edge - Historical Analysis Dashboard
Entry point for Streamlit Cloud deployment
"""
import streamlit as st
import pandas as pd
import numpy as np
import json
import gzip
from pathlib import Path
from datetime import datetime, timezone
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="London Temperature - Historical Analysis",
    page_icon="🌡️",
    layout="wide"
)


@st.cache_data
def load_all_markets():
    """Cargar todos los mercados - primero intenta comprimido, luego JSONs individuales"""

    # Buscar archivo comprimido primero
    compressed_paths = [
        Path(__file__).parent / "data" / "markets_compressed.json.gz",
        Path("data/markets_compressed.json.gz"),
    ]

    for compressed_path in compressed_paths:
        if compressed_path.exists():
            try:
                with gzip.open(compressed_path, 'rt', encoding='utf-8') as f:
                    markets = json.load(f)
                return markets
            except Exception as e:
                continue

    # Fallback: cargar JSONs individuales
    data_dirs = [
        Path(__file__).parent / "data" / "historical_prices",
        Path("data/historical_prices"),
        Path("C:/Users/kevin/OneDrive/Escritorio/arbi/london_edge/data/historical_prices"),
    ]

    for data_dir in data_dirs:
        if data_dir.exists():
            markets = []
            for filepath in sorted(data_dir.glob("*.json")):
                try:
                    with open(filepath, encoding='utf-8') as f:
                        m = json.load(f)
                    total_points = sum(len(b.get('history', [])) for b in m['buckets'].values())
                    if total_points > 0:
                        markets.append(m)
                except:
                    continue
            if markets:
                return markets

    return []


def parse_temp(label):
    """Extraer temperatura numerica del label"""
    if '<=' in label:
        return int(label.replace('<=', '').replace('C', ''))
    elif '>=' in label:
        return int(label.replace('>=', '').replace('C', ''))
    else:
        return int(label.replace('C', ''))


def get_winner(market):
    """Obtener bucket ganador"""
    for label, bucket in market['buckets'].items():
        if bucket.get('resolved_to') == 'YES':
            return label
    return None


# Cargar datos
markets = load_all_markets()

if not markets:
    st.error("No hay datos historicos disponibles.")
    st.info("Los datos se cargan desde archivos JSON en la carpeta data/historical_prices/")
    st.stop()

st.title("🌡️ London Temperature Markets - Analysis")
st.caption(f"{len(markets)} mercados analizados | {markets[-1]['date']} - {markets[0]['date']}")

# Tabs principales
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Estrategia",
    "🎯 Convergencia",
    "🎲 Monte Carlo",
    "📈 Price Explorer",
    "📋 Datos"
])

# =============================================================================
# TAB 1: ESTRATEGIA RECOMENDADA
# =============================================================================
with tab1:
    st.header("Estrategia Optima")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Configuracion")
        st.markdown("""
        | Parametro | Valor |
        |-----------|-------|
        | **Entrada** | 97% |
        | **Stop Loss** | 50% |
        | **Apuesta** | 15-25% bankroll |
        """)

        st.subheader("Metricas Historicas")
        st.metric("Win Rate", "98.5%", delta="67/68 trades")
        st.metric("EV por $1", "+$0.0226", delta="+2.26%")
        st.metric("Riesgo de Ruina", "0.00%")

    with col2:
        st.subheader("Proyeccion 100 Trades ($1,000)")

        # Mini simulacion
        np.random.seed(42)
        results = []
        for _ in range(1000):
            bankroll = 1000
            for _ in range(100):
                bet = bankroll * 0.20
                if np.random.random() < 0.985:
                    bankroll += bet * 0.03
                else:
                    bankroll -= bet * 0.47
            results.append(bankroll)

        results = np.array(results)

        col_a, col_b = st.columns(2)
        col_a.metric("Mediana", f"${np.median(results):,.0f}")
        col_b.metric("Media", f"${np.mean(results):,.0f}")

        fig = px.histogram(x=results, nbins=30, title="Distribucion de Resultados")
        fig.add_vline(x=1000, line_dash="dash", line_color="red", annotation_text="Inicial")
        fig.update_xaxes(title="Bankroll Final ($)")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Reglas de Oro")
    st.success("✅ Entrar cuando el bucket llega a 97%+")
    st.success("✅ Usar stop loss en 50%")
    st.success("✅ Apostar 15-25% del bankroll")
    st.warning("⚠️ Verificar que quedan >4 horas para el cierre")
    st.error("❌ NUNCA entrar por debajo de 95% sin stop loss")


# =============================================================================
# TAB 2: CONVERGENCIA
# =============================================================================
with tab2:
    st.header("Convergencia del Ganador")

    # Grafico de convergencia
    convergence_data = []

    for market in markets:
        winner = get_winner(market)
        if not winner:
            continue

        history = market['buckets'][winner].get('history', [])
        if not history:
            continue

        history = sorted(history, key=lambda x: x['t'])
        last_ts = history[-1]['t']

        for p in history:
            hours_before = (last_ts - p['t']) / 3600
            convergence_data.append({
                'hours_before': hours_before,
                'price': p['p'] * 100,
                'date': market['date'],
            })

    df_conv = pd.DataFrame(convergence_data)

    fig = px.scatter(
        df_conv,
        x='hours_before',
        y='price',
        opacity=0.3,
        title='Precio del Ganador vs Horas Restantes',
        labels={'hours_before': 'Horas antes del cierre', 'price': 'Precio (%)'}
    )
    fig.update_xaxes(autorange="reversed")
    fig.add_hline(y=90, line_dash="dash", line_color="orange", annotation_text="90%")
    fig.add_hline(y=95, line_dash="dash", line_color="green", annotation_text="95%")
    fig.add_hline(y=97, line_dash="dash", line_color="blue", annotation_text="97%")
    st.plotly_chart(fig, use_container_width=True)

    # Win rate por umbral
    st.subheader("Win Rate por Umbral de Entrada")

    thresholds = [0.90, 0.92, 0.95, 0.97, 0.98]
    wr_data = []

    for thresh in thresholds:
        wins = 0
        total = 0

        for market in markets:
            winner = get_winner(market)
            if not winner:
                continue

            for label, bucket in market['buckets'].items():
                history = bucket.get('history', [])
                if len(history) < 10:
                    continue

                history = sorted(history, key=lambda x: x['t'])
                touched = any(p['p'] >= thresh for p in history)

                if touched:
                    total += 1
                    if label == winner:
                        wins += 1

        if total > 0:
            wr_data.append({
                'Umbral': f"{thresh*100:.0f}%",
                'Win Rate': wins / total,
                'Trades': total,
                'Wins': wins,
                'EV': (wins/total) * (1-thresh) - ((total-wins)/total) * thresh if total > 0 else 0
            })

    df_wr = pd.DataFrame(wr_data)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df_wr['Umbral'],
        y=df_wr['Win Rate'],
        text=[f"{wr:.1%}" for wr in df_wr['Win Rate']],
        textposition='outside',
        marker_color=['red' if ev < 0 else 'green' for ev in df_wr['EV']]
    ))
    fig2.update_layout(
        title='Win Rate por Umbral (Verde = EV+, Rojo = EV-)',
        yaxis_title='Win Rate',
        yaxis_tickformat='.0%'
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(df_wr)


# =============================================================================
# TAB 3: MONTE CARLO
# =============================================================================
with tab3:
    st.header("Monte Carlo Simulator")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        entry = st.selectbox("Entrada", [90, 92, 95, 97, 98], index=3, format_func=lambda x: f"{x}%")

    with col2:
        use_stop = st.checkbox("Stop Loss", value=True)

    with col3:
        stop_level = st.selectbox("Nivel Stop", [0, 40, 50, 60, 70], index=2 if use_stop else 0, format_func=lambda x: f"{x}%" if x > 0 else "Sin stop")

    with col4:
        bet_pct = st.slider("Apuesta %", 5, 50, 20, 5)

    # Ajustar stop_level si no se usa stop loss
    if not use_stop:
        stop_level = 0

    col5, col6, col7 = st.columns(3)

    with col5:
        n_trades = st.slider("Trades", 50, 200, 100, 25)

    with col6:
        initial = st.number_input("Bankroll $", 100, 10000, 1000, 100)

    with col7:
        n_sims = st.selectbox("Simulaciones", [1000, 5000, 10000], index=1)

    # Calcular win rate historico
    entry_thresh = entry / 100
    stop_thresh = stop_level / 100 if use_stop else 0

    wins = losses_stopped = losses_full = 0

    for market in markets:
        winner = get_winner(market)
        if not winner:
            continue

        for label, bucket in market['buckets'].items():
            history = bucket.get('history', [])
            if len(history) < 10:
                continue

            history = sorted(history, key=lambda x: x['t'])
            is_winner = (label == winner)

            entry_idx = None
            for i, p in enumerate(history):
                if p['p'] >= entry_thresh:
                    entry_idx = i
                    break

            if entry_idx is None:
                continue

            post_entry = history[entry_idx:]
            min_price = min(p['p'] for p in post_entry)
            stop_hit = use_stop and min_price < stop_thresh

            if is_winner and not stop_hit:
                wins += 1
            elif stop_hit:
                losses_stopped += 1
            else:
                losses_full += 1

    total = wins + losses_stopped + losses_full

    if total > 0:
        p_win = wins / total
        p_stopped = losses_stopped / total
        p_full = losses_full / total

        profit_win = 1 - entry_thresh
        loss_stop = entry_thresh - stop_thresh if use_stop else entry_thresh
        loss_full = entry_thresh

        ev = p_win * profit_win - p_stopped * loss_stop - p_full * loss_full

        st.divider()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Win Rate", f"{p_win:.1%}")
        col2.metric("EV/trade", f"${ev:+.4f}")
        col3.metric("Trades historicos", total)
        col4.metric("Wins", wins)

        if ev < 0:
            st.error(f"⚠️ EV NEGATIVO - Esta configuracion pierde dinero")
        else:
            st.success(f"✅ EV POSITIVO - Edge de ${ev:.4f} por $1")

        if st.button("🚀 Simular", type="primary"):
            with st.spinner(f"Corriendo {n_sims:,} simulaciones..."):
                final_bankrolls = []
                paths = []

                bet_size = bet_pct / 100

                for sim in range(n_sims):
                    bankroll = initial
                    path = [bankroll]

                    for _ in range(n_trades):
                        bet = bankroll * bet_size
                        rand = np.random.random()

                        if rand < p_win:
                            bankroll += bet * profit_win
                        elif rand < p_win + p_stopped:
                            bankroll -= bet * loss_stop
                        else:
                            bankroll -= bet * loss_full

                        path.append(max(0, bankroll))
                        if bankroll <= 0:
                            break

                    final_bankrolls.append(bankroll)
                    if sim < 50:
                        paths.append(path)

                final_bankrolls = np.array(final_bankrolls)

            st.subheader("Resultados")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Mediana", f"${np.median(final_bankrolls):,.0f}")
            col2.metric("Media", f"${np.mean(final_bankrolls):,.0f}")
            col3.metric("Min", f"${np.min(final_bankrolls):,.0f}")
            col4.metric("Max", f"${np.max(final_bankrolls):,.0f}")

            col1, col2, col3 = st.columns(3)
            col1.metric("Prob Profit", f"{np.mean(final_bankrolls > initial)*100:.1f}%")
            col2.metric("Prob 2x", f"{np.mean(final_bankrolls >= initial*2)*100:.1f}%")
            col3.metric("Prob Ruina", f"{np.mean(final_bankrolls < initial*0.1)*100:.2f}%")

            col1, col2 = st.columns(2)

            with col1:
                fig = px.histogram(x=final_bankrolls, nbins=50, title="Distribucion Final")
                fig.add_vline(x=initial, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig2 = go.Figure()
                for path in paths:
                    fig2.add_trace(go.Scatter(y=path, mode='lines', opacity=0.3, showlegend=False))
                fig2.add_hline(y=initial, line_dash="dash", line_color="red")
                fig2.update_layout(title="50 Simulaciones", xaxis_title="Trade", yaxis_title="Bankroll")
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No hay datos para este umbral")


# =============================================================================
# TAB 4: PRICE EXPLORER
# =============================================================================
with tab4:
    st.header("Price Explorer")

    market_options = {m['date']: m for m in markets}
    selected_date = st.selectbox("Mercado", list(market_options.keys()))
    market = market_options[selected_date]

    winner = get_winner(market)
    st.info(f"Ganador: **{winner}**")

    fig = go.Figure()

    for label, bucket in market['buckets'].items():
        history = bucket.get('history', [])
        if not history:
            continue

        history = sorted(history, key=lambda x: x['t'])
        times = [datetime.fromtimestamp(p['t'], tz=timezone.utc) for p in history]
        prices = [p['p'] * 100 for p in history]

        line_width = 3 if label == winner else 1

        fig.add_trace(go.Scatter(
            x=times,
            y=prices,
            name=f"{label} {'✅' if label == winner else ''}",
            line=dict(width=line_width),
            mode='lines'
        ))

    fig.update_layout(
        title=f"Precios - {market['title']}",
        xaxis_title="Tiempo (UTC)",
        yaxis_title="Precio (%)",
        hovermode='x unified'
    )
    fig.add_hline(y=97, line_dash="dash", line_color="blue", opacity=0.5)
    fig.add_hline(y=50, line_dash="dash", line_color="red", opacity=0.3)

    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# TAB 5: DATOS
# =============================================================================
with tab5:
    st.header("Datos")

    summary = []
    for market in markets:
        winner = get_winner(market)
        if not winner:
            continue

        history = market['buckets'][winner].get('history', [])
        if history:
            prices = [p['p'] for p in history]
            summary.append({
                'Fecha': market['date'],
                'Ganador': winner,
                'Min': f"{min(prices):.0%}",
                'Max': f"{max(prices):.0%}",
                'Buckets': len(market['buckets'])
            })

    st.dataframe(pd.DataFrame(summary), use_container_width=True)

    st.subheader("Estadisticas")
    st.metric("Total mercados", len(markets))
    st.metric("Rango fechas", f"{markets[-1]['date']} a {markets[0]['date']}")


# Footer
st.divider()
st.caption("London Edge | Data: Polymarket CLOB API | [GitHub](https://github.com)")
