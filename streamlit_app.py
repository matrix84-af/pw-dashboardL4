import datetime
import pandas as pd
import altair as alt

from UI import *

global uhr


# page layout
st.set_page_config(page_title="Power Wash L4 Dashboard", page_icon="images/logo2.png", layout="wide", )

theme_plotly = None

# load CSS Style
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown(""" <style>.st-emotion-cache-1jicfl2 {
    width: 100%;
    padding: 0rem 1rem 10rem;
        padding-top: 0rem;
        padding-right: 3rem;
        padding-bottom: 1rem;
        padding-left: 3rem;
    min-width: auto;
    max-width: initial;
    }</style>""", unsafe_allow_html=True)

UI()
# load dataset
df = pd.read_csv('datapw.csv')
df.astype({'Bakterienbelastungsgrad': int})

st.sidebar.image("images/logo2.png")
# filter date to view data
with st.sidebar:
    st.title("Filter Datum")
    start_date = st.date_input(label="Start-Datum", value=(datetime.date.today() - datetime.timedelta(51)))

with st.sidebar:
    end_date = st.date_input(label="End-Datum")
with st.sidebar:
    becken = st.selectbox("Vorbehandlungszone",
                          ("Entfetten", "Spülen/VE-Sprühkr.", "Spülen 1", "Spülen 2", "Spülen 3", "VE-Sprühkranz"))

# compare date
df2 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (df['Vorbehandlungszone'] == str(becken))]

# Toast for page refresh
st.toast("Seite wurde aktualisiert")

# dataframe
# with st.expander("Filter Excel Dataset"):
# filtered_df = dataframe_explorer(df2, case=False)
# st.dataframe(filtered_df, use_container_width=True)


b1, b2, b3 = st.columns(3)

# bar chart
with b1:
    from add_data import *

    st.subheader('Neuer Datensatz', divider='blue', )
    add_data(becken)

    # metric cards

if becken == "Entfetten":
    with b2:
        st.subheader(str("Status " + becken), divider='blue', )
        df3 = df[(df['Vorbehandlungszone'] == str(becken))]
        datemax = df3.Datum.max()
        df4 = df[(df['Datum'] == datemax) & (df['Vorbehandlungszone'] == str(becken))]
        timemax = df4.Uhrzeit.max()
        df5 = df[(df['Datum'] == datemax) & (df['Uhrzeit'] == timemax) & (df['Vorbehandlungszone'] == str(becken))]

        from streamlit_extras.metric_cards import style_metric_cards

        col1, col2 = st.columns(2)
        col1.metric(label="Reinigerkonz. [%]:", value=df5['Reinigerkonzentration'],
                    delta=float(df5['Reinigerkonzentration'] - 1).__round__(1))
        col2.metric(label="Temperatur [°C]:", value=df5['Temperatur'], delta=float(df5['Temperatur'] - 40).__round__(1))

        col11, col22 = st.columns(2)
        col11.metric(label="Leitwert [µS/cm]:", value=int(df5['Leitwert']), delta=int(df5['Leitwert'] - 1500),
                     delta_color="inverse")
        col22.metric(label="pH-Wert:", value=df5['pHWert'], delta=float(df5['pHWert'] - 8).__round__(1))

        col111, col222 = st.columns(2)
        col111.metric(label="Bakt.-BG [K/ml]:", value=df5['Bakterienbelastungsgrad'],
                      delta=int(df5['Bakterienbelastungsgrad'] - 1000), delta_color="inverse")
        col222.metric(label="Sprühdruck [bar]:", value=df5['Pumpendruck'],
                      delta=float(df5['Pumpendruck'] - 1).__round__(1))
        # style the metric
        style_metric_cards(background_color="#596073", border_left_color="#F71938", border_color="#1f66bd",
                           box_shadow="#F71938")

if becken == "Spülen/VE-Sprühkr.":
    with b2:
        st.subheader(str("Status " + becken), divider='blue', )
        df3 = df[(df['Vorbehandlungszone'] == "Spülen 1")]
        datemax = df3.Datum.max()
        df4 = df[(df['Datum'] == datemax) & (df['Vorbehandlungszone'] == "Spülen 1")]
        timemax = df4.Uhrzeit.max()
        df5 = df[(df['Datum'] == datemax) & (df['Uhrzeit'] == timemax) & (df['Vorbehandlungszone'] == "Spülen 1")]

        from streamlit_extras.metric_cards import style_metric_cards

        col1, col2, col3 = st.columns(3)
        col1.metric(label="SP1 Leitwert [µS/cm]:", value=int(df5['Leitwert']), delta=int(df5['Leitwert'] - 800),
                    delta_color="inverse", )
        col2.metric(label="SP1 Sprühdruck [bar]:", value=df5['Pumpendruck'],
                    delta=float(df5['Pumpendruck'] - 1.0).__round__(1))
        col3.metric(label="SP1 Bakt.-BG [K/ml]:", value=df5['Bakterienbelastungsgrad'],
                    delta=int(df5['Bakterienbelastungsgrad'] - 1000), delta_color="inverse")

        df3 = df[(df['Vorbehandlungszone'] == "Spülen 2")]
        datemax = df3.Datum.max()
        df4 = df[(df['Datum'] == datemax) & (df['Vorbehandlungszone'] == "Spülen 2")]
        timemax = df4.Uhrzeit.max()
        df5 = df[(df['Datum'] == datemax) & (df['Uhrzeit'] == timemax) & (df['Vorbehandlungszone'] == "Spülen 2")]

        col11, col22, col33 = st.columns(3)
        col11.metric(label="SP2 Leitwert [µS/cm]:", value=int(df5['Leitwert']), delta=int(df5['Leitwert'] - 300),
                     delta_color="inverse")
        col22.metric(label="SP2 Sprühdruck [bar]:", value=df5['Pumpendruck'],
                     delta=float(df5['Pumpendruck'] - 1.0).__round__(1))
        col33.metric(label="SP2 Bakt.-BG [K/ml]:", value=df5['Bakterienbelastungsgrad'],
                     delta=int(df5['Bakterienbelastungsgrad'] - 1000), delta_color="inverse")

        df3 = df[(df['Vorbehandlungszone'] == "Spülen 3")]
        datemax = df3.Datum.max()
        df4 = df[(df['Datum'] == datemax) & (df['Vorbehandlungszone'] == "Spülen 3")]
        timemax = df4.Uhrzeit.max()
        df5 = df[(df['Datum'] == datemax) & (df['Uhrzeit'] == timemax) & (df['Vorbehandlungszone'] == "Spülen 3")]

        col111, col222, col333 = st.columns(3)
        col111.metric(label="SP3 Leitwert [µS/cm]:", value=int(df5['Leitwert']), delta=int(df5['Leitwert'] - 50),
                      delta_color="inverse")
        col222.metric(label="SP3 Sprühdruck [bar]:", value=df5['Pumpendruck'],
                      delta=float(df5['Pumpendruck'] - 1.0).__round__(1))
        col333.metric(label="SP3 Bakt.-BG [K/ml]:", value=df5['Bakterienbelastungsgrad'],
                      delta=int(df5['Bakterienbelastungsgrad'] - 1000), delta_color="inverse")

        # style the metric
        style_metric_cards(background_color="#596073", border_left_color="#F71938", border_color="#1f66bd",
                           box_shadow="#F71938")


if becken == "Spülen 1":
    with b2:
        st.subheader(str("Status " + becken), divider='blue', )
        df3 = df[(df['Vorbehandlungszone'] == "Spülen 1")]
        datemax = df3.Datum.max()
        df4 = df[(df['Datum'] == datemax) & (df['Vorbehandlungszone'] == "Spülen 1")]
        timemax = df4.Uhrzeit.max()
        df5 = df[(df['Datum'] == datemax) & (df['Uhrzeit'] == timemax) & (df['Vorbehandlungszone'] == "Spülen 1")]

        from streamlit_extras.metric_cards import style_metric_cards

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Leitwert [µS/cm]:", value=int(df5['Leitwert']), delta=int(df5['Leitwert'] - 800),
                  delta_color="inverse", )

        col2.metric(label="Sprühdruck [bar]:", value=df5['Pumpendruck'],
                    delta=float(df5['Pumpendruck'] - 1.0).__round__(1))

        col3.metric(label="Bakt.-BG [K/ml]:", value=df5['Bakterienbelastungsgrad'],
                    delta=int(df5['Bakterienbelastungsgrad'] - 1000), delta_color="inverse")

if becken == "Spülen 2":
    with b2:
        st.subheader(str("Status " + becken), divider='blue', )
        df3 = df[(df['Vorbehandlungszone'] == "Spülen 2")]
        datemax = df3.Datum.max()
        df4 = df[(df['Datum'] == datemax) & (df['Vorbehandlungszone'] == "Spülen 2")]
        timemax = df4.Uhrzeit.max()
        df5 = df[(df['Datum'] == datemax) & (df['Uhrzeit'] == timemax) & (df['Vorbehandlungszone'] == "Spülen 2")]

        from streamlit_extras.metric_cards import style_metric_cards

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Leitwert [µS/cm]:", value=int(df5['Leitwert']), delta=int(df5['Leitwert'] - 300),
                            delta_color="inverse", )

        col2.metric(label="Sprühdruck [bar]:", value=df5['Pumpendruck'],
                    delta=float(df5['Pumpendruck'] - 1.0).__round__(1))

        col3.metric(label="Bakt.-BG [K/ml]:", value=df5['Bakterienbelastungsgrad'],
                    delta=int(df5['Bakterienbelastungsgrad'] - 1000), delta_color="inverse")

        # style the metric
        style_metric_cards(background_color="#596073", border_left_color="#F71938", border_color="#1f66bd",
                            box_shadow="#F71938")

if becken == "Spülen 3":
    with b2:
        st.subheader(str("Status " + becken), divider='blue', )
        df3 = df[(df['Vorbehandlungszone'] == "Spülen 3")]
        datemax = df3.Datum.max()
        df4 = df[(df['Datum'] == datemax) & (df['Vorbehandlungszone'] == "Spülen 3")]
        timemax = df4.Uhrzeit.max()
        df5 = df[(df['Datum'] == datemax) & (df['Uhrzeit'] == timemax) & (df['Vorbehandlungszone'] == "Spülen 3")]

        from streamlit_extras.metric_cards import style_metric_cards

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Leitwert [µS/cm]:", value=int(df5['Leitwert']), delta=int(df5['Leitwert'] - 50),
                  delta_color="inverse", )

        col2.metric(label="Sprühdruck [bar]:", value=df5['Pumpendruck'],
                    delta=float(df5['Pumpendruck'] - 1.0).__round__(1))

        col3.metric(label="Bakt.-BG [K/ml]:", value=df5['Bakterienbelastungsgrad'],
                    delta=int(df5['Bakterienbelastungsgrad'] - 1000), delta_color="inverse")

        # style the metric
        style_metric_cards(background_color="#596073", border_left_color="#F71938", border_color="#1f66bd",
                           box_shadow="#F71938")

if becken == "VE-Sprühkranz":
    with b2:
        st.subheader(str("Status " + becken), divider='blue', )
        df3 = df[(df['Vorbehandlungszone'] == "VE-Sprühkranz")]
        datemax = df3.Datum.max()
        df4 = df[(df['Datum'] == datemax) & (df['Vorbehandlungszone'] == "VE-Sprühkranz")]
        timemax = df4.Uhrzeit.max()
        df5 = df[(df['Datum'] == datemax) & (df['Uhrzeit'] == timemax) & (df['Vorbehandlungszone'] == "VE-Sprühkranz")]

        from streamlit_extras.metric_cards import style_metric_cards

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Leitwert [µS/cm]:", value=int(df5['Leitwert']), delta=int(df5['Leitwert'] - 10),
                  delta_color="inverse", )

        col2.metric(label="Volumenstrom [l/h]:", value=int(df5['Pumpendruck']),
                    delta=int(df5['Pumpendruck'] - 300).__round__(0))

        col3.metric(label="Bakt.-BG [K/ml]:", value=df5['Bakterienbelastungsgrad'],
                    delta=int(df5['Bakterienbelastungsgrad'] - 1000), delta_color="inverse")

        # style the metric
        style_metric_cards(background_color="#596073", border_left_color="#F71938", border_color="#1f66bd",
                           box_shadow="#F71938")

if becken == "Entfetten":
    with b3:
        st.subheader('pH-Wert Entfetten', divider='blue', )
        dfsp1 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Entfetten")]
        source = dfsp1

        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='pHWert',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[7.8, 9.2])
        band0 = alt.Chart(pd.DataFrame({'pHWert': [8]})).mark_rule(color='red').encode(y='pHWert')
        band1 = alt.Chart(pd.DataFrame({'pHWert': [9]})).mark_rule(color='red').encode(y='pHWert')

        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    # dot Plot
    a1, a2, a3 = st.columns(3)

    with a1:
        st.subheader('Reinigerkonz. Entfetten [%]', divider='blue', )
        dfent = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Entfetten")]
        source = dfent
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Reinigerkonzentration',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0.8, 1.7])
        band0 = alt.Chart(pd.DataFrame({'Reinigerkonzentration': [1.5]})).mark_rule(color='red').encode(
            y='Reinigerkonzentration')
        band1 = alt.Chart(pd.DataFrame({'Reinigerkonzentration': [1.0]})).mark_rule(color='red').encode(
            y='Reinigerkonzentration')

        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    with a2:
        st.subheader('Temperatur Entfetten [°C]', divider='blue', )
        dfent = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Entfetten")]
        source = dfent
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Temperatur',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[38, 62])
        band0 = alt.Chart(pd.DataFrame({'Temperatur': [60]})).mark_rule(color='red').encode(y='Temperatur')
        band1 = alt.Chart(pd.DataFrame({'Temperatur': [40]})).mark_rule(color='red').encode(y='Temperatur')

        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    with a3:
        st.subheader('Leitwert Entfetten [µS/cm]', divider='blue', )
        dfent = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Entfetten")]
        source = dfent
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Leitwert',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[500, 1600])
        band0 = alt.Chart(pd.DataFrame({'Leitwert': [600]})).mark_rule(color='red').encode(
            y='Leitwert')
        band1 = alt.Chart(pd.DataFrame({'Leitwert': [1500]})).mark_rule(color='red').encode(
            y='Leitwert')
        band2 = alt.Chart(pd.DataFrame({'Leitwert': [700]})).mark_rule(color='orange').encode(
            y='Leitwert')
        band3 = alt.Chart(pd.DataFrame({'Leitwert': [1400]})).mark_rule(color='orange').encode(
            y='Leitwert')
        st.altair_chart(chart + band0 + band1 + band2 + band3, theme="streamlit", use_container_width=True)

if becken == "Spülen/VE-Sprühkr.":
    with b3:
        st.subheader('Leitwert Spülen 1 [µS/cm]', divider='blue', )
        dfsp1 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Spülen 1")]
        source = dfsp1

        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Leitwert',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0, 900])
        band0 = alt.Chart(pd.DataFrame({'Leitwert': [800]})).mark_rule(color='red').encode(y='Leitwert')
        band1 = alt.Chart(pd.DataFrame({'Leitwert': [700]})).mark_rule(color='orange').encode(y='Leitwert')

        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    # dot Plot
    a1, a2, a3 = st.columns(3)

    with a1:
        st.subheader('Leitwert Spülen 2 [µS/cm]', divider='blue', )
        dfsp2 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Spülen 2")]
        source = dfsp2
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Leitwert',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0, 400])
        band0 = alt.Chart(pd.DataFrame({'Leitwert': [300]})).mark_rule(color='red').encode(y='Leitwert')
        band1 = alt.Chart(pd.DataFrame({'Leitwert': [250]})).mark_rule(color='orange').encode(y='Leitwert')
        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    with a2:
        st.subheader('Leitwert Spülen 3 [µS/cm]', divider='blue', )
        dfsp3 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Spülen 3")]
        source = dfsp3
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Leitwert',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0, 60])
        band0 = alt.Chart(pd.DataFrame({'Leitwert': [50]})).mark_rule(color='red').encode(y='Leitwert')
        band1 = alt.Chart(pd.DataFrame({'Leitwert': [40]})).mark_rule(color='orange').encode(y='Leitwert')
        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    with a3:
        st.subheader('Leitwert VE-Sprühkr. [µS/cm]', divider='blue', )
        dfve = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "VE-Sprühkranz")]
        source = dfve
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Leitwert',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0, 12])
        band0 = alt.Chart(pd.DataFrame({'Leitwert': [10]})).mark_rule(color='red').encode(
            y='Leitwert')
        band1 = alt.Chart(pd.DataFrame({'Leitwert': [7]})).mark_rule(color='orange').encode(
            y='Leitwert')
        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

if becken == "Spülen 1":
    # dot Plot
    a1, a2, a3 = st.columns(3)

    with a1:
        st.subheader('Leitwert Spülen 1 [µS/cm]', divider='blue', )
        dfsp1 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Spülen 1")]
        source = dfsp1

        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Leitwert',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0, 850])
        band0 = alt.Chart(pd.DataFrame({'Leitwert': [800]})).mark_rule(color='red').encode(y='Leitwert')
        band1 = alt.Chart(pd.DataFrame({'Leitwert': [700]})).mark_rule(color='orange').encode(y='Leitwert')
        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    with a2:
        st.subheader('Bakt.-BLG Spülen 1 [K/ml]', divider='blue', )
        dfsp3 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Spülen 1")]
        source = dfsp3
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Bakterienbelastungsgrad',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0, 1100])
        band0 = alt.Chart(pd.DataFrame({'Bakterienbelastungsgrad': [1000]})).mark_rule(color='red').encode(
            y='Bakterienbelastungsgrad')

        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    with a3:
        st.subheader('Sprühdruck Spülen 1 [bar]', divider='blue', )
        dfve = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Spülen 1")]
        source = dfve
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Pumpendruck',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0.7, 1.8])
        band0 = alt.Chart(pd.DataFrame({'Pumpendruck': [1.5]})).mark_rule(color='red').encode(
            y='Pumpendruck')
        band1 = alt.Chart(pd.DataFrame({'Pumpendruck': [1.0]})).mark_rule(color='red').encode(
            y='Pumpendruck')
        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

if becken == "Spülen 2":
    # dot Plot
    a1, a2, a3 = st.columns(3)

    with a1:
        st.subheader('Leitwert Spülen 2 [µS/cm]', divider='blue', )
        dfsp1 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Spülen 2")]
        source = dfsp1

        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Leitwert',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0, 400])
        band0 = alt.Chart(pd.DataFrame({'Leitwert': [300]})).mark_rule(color='red').encode(y='Leitwert')
        band1 = alt.Chart(pd.DataFrame({'Leitwert': [250]})).mark_rule(color='orange').encode(y='Leitwert')
        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    with a2:
        st.subheader('Bakt.-BLG Spülen 2 [K/ml]', divider='blue', )
        dfsp3 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Spülen 2")]
        source = dfsp3
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Bakterienbelastungsgrad',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0, 1100])
        band0 = alt.Chart(pd.DataFrame({'Bakterienbelastungsgrad': [1000]})).mark_rule(color='red').encode(
            y='Bakterienbelastungsgrad')
        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    with a3:
        st.subheader('Sprühdruck Spülen 2 [bar]', divider='blue', )
        dfve = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Spülen 2")]
        source = dfve
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Pumpendruck',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0.7, 1.8])
        band0 = alt.Chart(pd.DataFrame({'Pumpendruck': [1.5]})).mark_rule(color='red').encode(
            y='Pumpendruck')
        band1 = alt.Chart(pd.DataFrame({'Pumpendruck': [1.0]})).mark_rule(color='red').encode(
            y='Pumpendruck')
        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

if becken == "Spülen 3":
    # dot Plot
    a1, a2, a3 = st.columns(3)

    with a1:
        st.subheader('Leitwert Spülen 3 [µS/cm]', divider='blue', )
        dfsp1 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Spülen 3")]
        source = dfsp1

        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Leitwert',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0, 70])
        band0 = alt.Chart(pd.DataFrame({'Leitwert': [50]})).mark_rule(color='red').encode(y='Leitwert')
        band1 = alt.Chart(pd.DataFrame({'Leitwert': [45]})).mark_rule(color='orange').encode(y='Leitwert')
        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    with a2:
        st.subheader('Bakt.-BLG Spülen 3 [K/ml]', divider='blue', )
        dfsp3 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Spülen 3")]
        source = dfsp3
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Bakterienbelastungsgrad',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0, 1100])
        band0 = alt.Chart(pd.DataFrame({'Bakterienbelastungsgrad': [1000]})).mark_rule(color='red').encode(
            y='Bakterienbelastungsgrad')
        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    with a3:
        st.subheader('Sprühdruck Spülen 3 [bar]', divider='blue', )
        dfve = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "Spülen 3")]
        source = dfve
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Pumpendruck',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0.7, 1.8])
        band0 = alt.Chart(pd.DataFrame({'Pumpendruck': [1.5]})).mark_rule(color='red').encode(
            y='Pumpendruck')
        band1 = alt.Chart(pd.DataFrame({'Pumpendruck': [1.0]})).mark_rule(color='red').encode(
            y='Pumpendruck')
        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

if becken == "VE-Sprühkranz":
    # dot Plot
    a1, a2, a3 = st.columns(3)

    with a1:
        st.subheader('Leitwert VE-Sprühkr. [µS/cm]', divider='blue', )
        dfsp1 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "VE-Sprühkranz")]
        source = dfsp1

        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Leitwert',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0, 12])
        band0 = alt.Chart(pd.DataFrame({'Leitwert': [10]})).mark_rule(color='red').encode(y='Leitwert')
        band1 = alt.Chart(pd.DataFrame({'Leitwert': [7]})).mark_rule(color='orange').encode(y='Leitwert')
        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    with a2:
        st.subheader('Bakt.-BLG VE-Sprühkr. [K/ml]', divider='blue', )
        dfsp3 = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "VE-Sprühkranz")]
        source = dfsp3
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Bakterienbelastungsgrad',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[0, 1100])
        band0 = alt.Chart(pd.DataFrame({'Bakterienbelastungsgrad': [1000]})).mark_rule(color='red').encode(
            y='Bakterienbelastungsgrad')

        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)

    with a3:
        st.subheader('Volumenstr. VE-Sprühkr. [l/h]', divider='blue', )
        dfve = df[(df['Datum'] >= str(start_date)) & (df['Datum'] <= str(end_date)) & (
                df['Vorbehandlungszone'] == "VE-Sprühkranz")]
        source = dfve
        chart = alt.Chart(source).mark_line().encode(
            x='Datum',
            y='Pumpendruck',
            # color='Category',

        ).interactive()
        chart.encoding.y.scale = alt.Scale(domain=[280, 340])
        band0 = alt.Chart(pd.DataFrame({'Pumpendruck': [300]})).mark_rule(color='red').encode(
            y='Pumpendruck')

        st.altair_chart(chart + band0 + band1, theme="streamlit", use_container_width=True)
# select only numeric or number data
# pip install pandas-select
# https://pypi.org/project/pandas-select/
