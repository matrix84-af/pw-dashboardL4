# import libraries
import streamlit as st
import pandas as pd


def add_data(becken):
    df = pd.read_csv("datapw.csv")

    with st.form("form 2", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        Datum = col1.date_input(label="Datum")
        region = col2.selectbox("VB-Zone", ("Entfetten", "Spülen 1", "Spülen 2", "Spülen 3", "VE-Spülring"))
        presure = col3.selectbox("Sprühdruck [bar]", ("0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0",
                                                 "1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9", "2.0"))

        col11, col22, col33 = st.columns(3)
        city = col11.selectbox("Reinigerkonz.[%]",
                               ("0.0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9",
                                "1.0", "1.1", "1.2", "1.3", "1.5", "1.6", "1.7", "1.8", "1.9", "2.0"), )
        category = col22.selectbox("Temperatur [°C]", df["Temperatur"])
        unitprice = col33.text_input("Leitwert [µS/cm]", value="", placeholder="z.B. 1200")

        col111, col222, col333 = st.columns(3)
        quantity = col111.selectbox("pH-Wert", ("5.5", "5.6", "5.7", "5.8", "5.9", "6.0", "6.1", "6.2", "6.3", "6.4",
                                                "6.7", "6.8", "6.9", "7.0", "7.1", "7.2", "7.3", "7.4", "7.5", "7.6",
                                                "7.7", "7.8", "7.9", "8.0", "8.1", "8.2", "8.3", "8.4", "8.5", "8.6",
                                                "8.7", "8.8", "8.9", "9.0", "9.1", "9.2", "9.3", "9.4", "9.5", "9.6",
                                                "9.7", "9.8", "9.9", "10.0"))
        product = col222.selectbox("Bakt.-BLG [K/ml]", (0, 10, 100, 1000, 10000, 100000))

        time1 = col333.time_input("Uhrzeit", value="now", step=160)

        btn = st.form_submit_button("Speichern", type="primary", use_container_width=True)

        # if btn is clicked
        # validate
        if btn:
            if Datum == "" or region == "" or city == "" or category == "" or product == "" or quantity == "" or \
                    unitprice == "":
                st.warning("All fields are required")
                return False
            else:

                df = pd.concat([df, pd.DataFrame.from_records([{
                    'Datum': Datum,
                    'Vorbehandlungszone': region,
                    'Uhrzeit': time1,
                    'Reinigerkonzentration': city,
                    'Temperatur': category,
                    'Pumpendruck': presure,
                    'Bakterienbelastungsgrad': product,
                    'Leitwert': unitprice,
                    'pHWert': quantity,
                }])])
            try:
                df.to_csv("datapw.csv", index=False)
                st.success(Datum + " " + time1 + " " + becken + " wurde erfogreich gespeichert!")
                st.toast("Seite wurde aktualisiert")
                st.rerun()
                return True

            except:
                st.warning("Unable to write, Please close your dataset !!")
                st.toast("Seite wurde aktualisiert")
                st.rerun()
                return False
