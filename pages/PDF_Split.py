import streamlit as st
from scripts.functions import get_pdf_page_count, pdf_split, save_file, delete_pdf_files
import re
import os
import zipfile
from io import BytesIO

# Clean up any existing temporary PDF files
delete_pdf_files()

# Set page title and layout
st.set_page_config(page_title="PDF Splitter", layout="centered")
st.title("PDF Splitter")
st.markdown("Easily split your PDF into specific page ranges or individual pages with a simple and intuitive interface.")

# Styling for a clean, professional look
st.markdown("""
    <style>
    .stButton>button {
        background-color: #0078d4;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #005a9e;
    }
    .stTextInput input {
        border-radius: 5px;
        padding: 10px;
    }
    .stFileUploader label {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# File uploader
pdf_file = st.file_uploader("Upload your PDF file", type=['pdf'], accept_multiple_files=False)

if pdf_file:
    # Save the uploaded file and get page count
    path = save_file(file_uploader=pdf_file)
    total_pages = get_pdf_page_count(path)
    st.info(f"Uploaded PDF has {total_pages} page{'s' if total_pages != 1 else ''}.")

    # Create tabs for the two split options
    tab1, tab2 = st.tabs(["Split by Page Ranges", "Split into Individual Pages"])

    # Tab 1: Split by Page Ranges
    with tab1:
        st.markdown("Enter page ranges to split your PDF into separate files (e.g., '1-3, 5-8, 10').")
        ranges_input = st.text_input(
            "Page Ranges",
            placeholder="e.g., 1-3, 5-8, 10",
            help="Enter page ranges like '1-3' for pages 1 to 3, or '5' for a single page. Separate multiple ranges with commas."
        )
        if st.button("Split by Ranges"):
            if ranges_input:
                try:
                    # Parse page ranges (e.g., "1-3, 5-8, 10")
                    ranges = []
                    for r in ranges_input.replace(" ", "").split(","):
                        if "-" in r:
                            start, end = map(int, r.split("-"))
                            if 1 <= start <= end <= total_pages:
                                ranges.append((start - 1, end))
                            else:
                                raise ValueError(f"Invalid range {r}. Pages must be between 1 and {total_pages}.")
                        else:
                            page = int(r)
                            if 1 <= page <= total_pages:
                                ranges.append((page - 1, page))
                            else:
                                raise ValueError(f"Invalid page {r}. Pages must be between 1 and {total_pages}.")

                    # Create a ZIP file to store split PDFs
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for start, end in ranges:
                            output_pdf = pdf_split(pdf=path, pagerange=(start, end))
                            range_name = f"{pdf_file.name.replace('.pdf', '')}_pages_{start + 1}{'-' + str(end) if start + 1 != end else ''}.pdf"
                            zip_file.writestr(range_name, output_pdf.getvalue())

                    # Clean up temporary files
                    delete_pdf_files()

                    # Provide download link for the ZIP file
                    st.success(f"Successfully split PDF into {len(ranges)} file{'s' if len(ranges) != 1 else ''}.")
                    st.download_button(
                        label="Download Split PDFs (ZIP)",
                        data=zip_buffer.getvalue(),
                        file_name=f"{pdf_file.name.replace('.pdf', '')}_split_ranges.zip",
                        mime="application/zip"
                    )
                except ValueError as e:
                    st.error(f"Error: {str(e)}")
                    delete_pdf_files()
            else:
                st.error("Please enter page ranges.")

    # Tab 2: Split into Individual Pages
    with tab2:
        st.markdown("Split your PDF into individual pages, each saved as a separate PDF file.")
        if st.button("Split into Individual Pages"):
            # Create a ZIP file to store individual pages
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for page in range(total_pages):
                    output_pdf = pdf_split(pdf=path, pagerange=(page, page + 1))
                    page_name = f"{pdf_file.name.replace('.pdf', '')}_page_{page + 1}.pdf"
                    zip_file.writestr(page_name, output_pdf.getvalue())

            # Clean up temporary files
            delete_pdf_files()

            # Provide download link for the ZIP file
            st.success(f"Successfully split PDF into {total_pages} individual page{'s' if total_pages != 1 else ''}.")
            st.download_button(
                label="Download Individual Pages (ZIP)",
                data=zip_buffer.getvalue(),
                file_name=f"{pdf_file.name.replace('.pdf', '')}_split_pages.zip",
                mime="application/zip"
            )