#####################################################################################################
# Libraries
#####################################################################################################

import streamlit as st
import pandas as pd
import numpy as np

#####################################################################################################
# Title
#####################################################################################################

st.set_page_config(page_title = "PGE-Argide Interference Correction", layout="wide")
st.title("PGE-Argide Interference Correction")
st.write("Contact Information: Matthew Brzozowski, PhD | matt.brzozow@gmail.com")

st.write("-------------")
st.write("")

#####################################################################################################
# Important - Read First
#####################################################################################################

st.subheader("Important - Read First")

with st.expander(label = "Important - Read First"):

    st.subheader("Data format")
    st.write("PGE, Cu, and Zn data need to be in the following format --> Cu63, Cu65, Zn66, Zn68, Rh103, Pd105, Pd106, Pd108 (same format for all other elements as well)")
    st.write("The file uploader removes the first 3 rows (the header information) from the csv. If the elements are on row 1 of the CSV, add 3 rows above them (i.e., elements start on row 4).")
    
    st.subheader("Interferences corrected:")
    st.write("Cu63Ar40 --> Rh103")
    st.write("Cu65Ar40 --> Pd105")
    st.write("Zn66Ar40 --> Pd106")
    st.write("Zn68Ar40 --> Pd108")

    st.subheader("Interferences that have to be corrected after:")
    st.write("Cd106 --> Pd106")
    st.write("Cd108 --> Pd108")
    st.write("These can be corrected for by applying a correction factor to concentrations determined on Pd106 and Pd108.")
    st.write("Pd106 --> Pd106_ppm - (0.043 * Cd_ppm)")
    st.write("Pd108 --> Pd108_ppm - (0.034 * Cd_ppm)")

st.write("")

#####################################################################################################
# Load user data
#####################################################################################################

st.subheader("Upload your data as a CSV")

uploaded_file = st.file_uploader(label = "", type = "csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, skiprows = 3)

#####################################################################################################
# Argide interference calculations
#####################################################################################################

st.sidebar.header("Input the PGE ratios from Cu and Zn metal analyses")

Rh103_metal_Cu63_metal = st.sidebar.number_input(label = "Rh103/Cu63", format = "%e")
Pd105_metal_Cu65_metal = st.sidebar.number_input(label = "Pd105/Cu65", format = "%e")
Pd106_metal_Zn66_metal = st.sidebar.number_input(label = "Pd106/Zn66", format = "%e")
Pd108_metal_Zn68_metal = st.sidebar.number_input(label = "Pd108/Zn68", format = "%e")

if uploaded_file is not None:
    Cu63Ar40_int_cps = data.Cu63 * (Rh103_metal_Cu63_metal)
    Cu65Ar40_int_cps = data.Cu65 * (Pd105_metal_Cu65_metal)
    Zn66Ar40_int_cps = data.Zn66 * (Pd106_metal_Zn66_metal)
    Zn68Ar40_int_cps = data.Zn68 * (Pd108_metal_Zn68_metal)

    Rh103_corr_cps = data.Rh103 - Cu63Ar40_int_cps
    Pd105_corr_cps = data.Pd105 - Cu65Ar40_int_cps
    Pd106_corr_cps = data.Pd106 - Zn66Ar40_int_cps
    Pd108_corr_cps = data.Pd108 - Zn68Ar40_int_cps

    Rh103_corr_cps = np.where(Rh103_corr_cps < 0, 0, Rh103_corr_cps)
    Pd105_corr_cps = np.where(Pd105_corr_cps < 0, 0, Pd105_corr_cps)
    Pd106_corr_cps = np.where(Pd106_corr_cps < 0, 0, Pd106_corr_cps)
    Pd108_corr_cps = np.where(Pd108_corr_cps < 0, 0, Pd108_corr_cps)

    data["Rh103"] = Rh103_corr_cps
    data["Pd105"] = Pd105_corr_cps
    data["Pd106"] = Pd106_corr_cps
    data["Pd108"] = Pd108_corr_cps

#####################################################################################################
# Argide-corrected data
#####################################################################################################

if uploaded_file is not None:
    st.write("")
    st.subheader("Argide-corrected data")
    st.write("")

    st.dataframe(data)

    st.write("")

    # Download button for RFC model results

    file_name = st.text_input(label = "Input file name (incude .csv)")

    @st.cache
    def convert_df(df):
        return df.to_csv().encode("utf-8")

    corrected_data_download = convert_df(data)
    st.download_button(label = "Download corrected data", data = corrected_data_download, file_name = file_name, mime = "text/csv")