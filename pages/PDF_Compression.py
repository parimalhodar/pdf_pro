import streamlit as st
from scripts.functions import pdf_compress, delete_pdf_files, save_file, pdf_compress_ghost
import io
import os
try:
    import ghostscript as gs
    ghostscript_available = True
except ImportError:
    ghostscript_available = False

delete_pdf_files()

st.title('Compressing PDFs')

with st.expander(label='Job Aids'):
    st.info(
    '''
    Welcome to the PDF Compression Tool! Choose a compression method and upload your PDF file below.
    The tool supports two compression methods: **PyPDF2 Compression** and **Ghostscript Compression** (if available).
    
    - **PyPDF2 Compression:** Uses the PyPDF2 library to compress PDF files.
    - **Ghostscript Compression:** Uses Ghostscript for advanced compression (requires Ghostscript binary installed).
    
    For Ghostscript Compression, you have two options: Screen and eBook

    - **Screen Compression:** Optimized for quick online viewing, reduces file size and resolution, ideal for web pages and presentations.
    - **eBook Compression:** Balances quality and size, offering better resolution than Screen, perfect for e-readers.
    
    First upload the PDF file you wish to compress. Then click the **Compress PDF** button to start the compression process.
    The compressed file will be available for download once the process is complete.
    
    **Note:** If Ghostscript is not installed, only PyPDF2 Compression will be available.
    ''')

uploaded_file = st.file_uploader('Upload your PDF file (single file upload supported)', type=['pdf'], accept_multiple_files=False)

if uploaded_file:
    compression_options = ['PyPDF2 Compression']
    if ghostscript_available:
        compression_options.append('Ghostscript Compression')
    compression_method = st.radio('Select Compression Method', compression_options)
    
    pdf_settings = None
    if compression_method == 'Ghostscript Compression' and ghostscript_available:
        pdf_settings = st.radio('Select Compression Setting', ('eBook', 'Screen'))
    
    if st.button('Compress PDF'):
        output_file_name = uploaded_file.name.replace('.pdf', '_compressed.pdf')
        try:
            if compression_method == 'PyPDF2 Compression':
                compressed_pdf = pdf_compress(uploaded_file)
            elif compression_method == 'Ghostscript Compression' and ghostscript_available:
                output_file = pdf_compress_ghost(uploaded_file=uploaded_file,
                                                output_file_name=output_file_name,
                                                pdf_settings=pdf_settings)
                with open(output_file, 'rb') as f:
                    compressed_pdf = io.BytesIO(f.read())
            else:
                st.error('Ghostscript is not installed. Falling back to PyPDF2 Compression.')
                compressed_pdf = pdf_compress(uploaded_file)

            uploaded_file_size = len(uploaded_file.getvalue()) / (1024 * 1024)
            compressed_file_size = len(compressed_pdf.getvalue()) / (1024 * 1024)

            st.success(f'Successfully compressed the uploaded PDF using {compression_method}. Initial file size {uploaded_file_size:.2f} MB reduced to {compressed_file_size:.2f} MB. Click the button to download the compressed file.')

            delete_pdf_files()

            st.download_button('Download Compressed PDF', compressed_pdf, key='download_pdf', file_name=output_file_name)
        except Exception as e:
            st.error(f'Error during compression: {str(e)}')
            delete_pdf_files()