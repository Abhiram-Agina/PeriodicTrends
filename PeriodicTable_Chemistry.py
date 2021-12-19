import streamlit as st

from matplotlib import pyplot as plt
from plotly import graph_objs as go
import numpy as np

from bokeh.plotting import figure #pip install --force-reinstall --no-deps bokeh==2.4.1

import plotly.express as px

#periodic table data is assigned to the variable ptable
from mendeleev.fetch import fetch_table

ptable = fetch_table('elements')
# type(ptable) # this is a pandas dataframe

st.header("Periodic Table Trends")

nav = st.sidebar.radio("Navigation:",["Trends in Periodic Table","Periodic Table Blocks"])

if nav=="Trends in Periodic Table":

    xv = st.selectbox("enter property for x-axis - usually atomic_number", ptable.columns, index=1)
    xval = ptable[xv]

    yv1 = st.selectbox("enter property #1 for y-axis: ", ptable.columns, index=3)
    yval1 = ptable[yv1]

    # yv2 = st.selectbox("enter property #2 for y-axis: ", ptable.columns, index=5)
    # yval2 = ptable[yv2]

    st.write("Statistics of properties selected")
    cols = st.columns(2)
    cols[0].write(ptable[[xv, yv1]])
    cols[1].write(ptable[yv1].describe()) #statistics about this column

    graphType = st.selectbox("select graph type", ('line', 'scatter', 'vbar'), index=2)

    p = figure(
         title='Trends in Periodic Table',
         x_axis_label=xv,
         y_axis_label=yv1)

    if graphType=="line":
        p.line(xval, yval1, legend_label='Trend', line_width=2)
    if graphType=="scatter":
        p.scatter(xval, yval1, legend_label='Trend')
    if graphType=="vbar":
        p.vbar(x=xval, width=0.1, top=yval1, legend_label='Trend')
     
    st.bokeh_chart(p, use_container_width=True)

###

if nav=="Periodic Table Blocks":
    st.header("Periodic Table Blocks")

    new_ptable = ptable.set_index("symbol")

    cols = st.columns(2)
    blk = cols[0].selectbox("Select a Periodic Table Block to analyze", new_ptable["block"].unique())
    prp = cols[1].multiselect("Select a Property to analyze in the Block", new_ptable.columns, default=["atomic_number","boiling_point"])

    st.write(new_ptable.groupby("block").get_group(blk[0])[prp])
    fig = px.scatter(new_ptable, x=new_ptable[prp[0]], y=new_ptable[prp[1]], animation_frame=new_ptable[prp[0]],
               log_x=False, size_max=55, range_x=[1,119], range_y=[-200,5500])
    st.write(fig)

    # st.write("table sorted by second property")
    # st.write(new_ptable.groupby("block").get_group(blk[0])[prp].sort_values(by=new_ptable[prp[0]])) ==> fix error

