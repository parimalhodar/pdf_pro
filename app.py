# importing required packages
import streamlit as st

# Content for Home Page
st.title('Welcome to the PDF Editor App!')

st.markdown('''This app, developed by Parimal Hodar (parimal.court@gmail.com), allows you to perform various PDF editing tasks easily.
To get started, please navigate to the sidebar on the left where you will find the following editing options:''')

st.markdown('- Merge multiple PDF files into one.')
st.markdown('- Compress PDF files to reduce their size.')
st.markdown('- Insert one PDF into another after a certain page.')
st.markdown('- Slice some pages from a PDF file.')
st.markdown('- Add Watermark or Stamp to a PDF file.')

st.markdown('Simply click on the option you would like to use, and follow the instructions provided. Enjoy editing your PDFs! 🎉')