import streamlit as st
from scripts.functions import get_pdf_page_count, pdf_inserter, save_file, delete_pdf_files

# Clean up any existing temporary PDF files
delete_pdf_files()

# Set page title and layout
st.set_page_config(page_title="PDF Inserter", layout="centered")
st.title("PDF Inserter")
st.markdown("Insert pages from one PDF into another with a simple, step-by-step process.")

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
    .stNumberInput input {
        border-radius: 5px;
        padding: 10px;
    }
    .stFileUploader label {
        font-weight: bold;
    }
    .step-header {
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Step 1: Upload Main PDF
st.markdown("<div class='step-header'>Step 1: Upload Main PDF</div>", unsafe_allow_html=True)
pdf_file_1 = st.file_uploader("Upload the main PDF file", type=['pdf'], accept_multiple_files=False, key="main_pdf")
main_pages = 0
if pdf_file_1:
    path1 = save_file(file_uploader=pdf_file_1)
    main_pages = get_pdf_page_count(path1)
    st.info(f"Main PDF has {main_pages} page{'s' if main_pages != 1 else ''}.")

# Step 2: Enter Insertion Page Number
st.markdown("<div class='step-header'>Step 2: Choose Insertion Point</div>", unsafe_allow_html=True)
if main_pages > 0:
    insert_after = st.number_input(
        "Enter the page number after which to insert pages",
        min_value=1,
        max_value=main_pages,
        value=1,
        step=1,
        help=f"Enter a page number from 1 to {main_pages}. Pages from the second PDF will be inserted after this page."
    )
else:
    insert_after = None
    st.warning("Please upload the main PDF first.")

# Step 3: Upload Insert PDF
st.markdown("<div class='step-header'>Step 3: Upload Insert PDF</div>", unsafe_allow_html=True)
pdf_file_2 = st.file_uploader("Upload the PDF to insert", type=['pdf'], accept_multiple_files=False, key="insert_pdf")
insert_pages = 0
if pdf_file_2:
    path2 = save_file(file_uploader=pdf_file_2)
    insert_pages = get_pdf_page_count(path2)
    st.info(f"Insert PDF has {insert_pages} page{'s' if insert_pages != 1 else ''}.")

# Step 4: Enter Page Range from Insert PDF
st.markdown("<div class='step-header'>Step 4: Select Pages to Insert</div>", unsafe_allow_html=True)
if insert_pages > 0:
    insert_range = st.text_input(
        "Enter page range from insert PDF",
        placeholder="e.g., 3-5 or 7",
        help="Enter a range like '3-5' or a single page like '7'. Pages must be between 1 and {insert_pages}."
    )
else:
    insert_range = None
    st.warning("Please upload the insert PDF first.")

# Preview and Insert Buttons
if pdf_file_1 and pdf_file_2 and insert_range:
    try:
        # Parse insert range
        if "-" in insert_range:
            start, end = map(int, insert_range.split("-"))
            if not (1 <= start <= end <= insert_pages):
                raise ValueError(f"Invalid range {insert_range}. Pages must be between 1 and {insert_pages}.")
            pagerange2 = (start - 1, end)
        else:
            page = int(insert_range)
            if not (1 <= page <= insert_pages):
                raise ValueError(f"Invalid page {page}. Pages must be between 1 and {insert_pages}.")
            pagerange2 = (page - 1, page)

        # Preview Button
        if st.button("Preview Final Page Order"):
            total_pages_after = main_pages + (pagerange2[1] - pagerange2[0])
            preview_text = (
                f"**Final Page Order**:\n"
                f"- Pages 1 to {insert_after} from Main PDF\n"
                f"- Pages {pagerange2[0] + 1} to {pagerange2[1]} from Insert PDF\n"
                f"- Pages {insert_after + 1} to {main_pages} from Main PDF\n"
                f"**Total Pages**: {total_pages_after}"
            )
            st.success(preview_text)

        # Insert Button
        if st.button("Insert and Download PDF"):
            final_pdf = pdf_inserter(
                pdf1=path1,
                pagerange1=(0, main_pages),
                pdf2=path2,
                pagerange2=pagerange2,
                position=insert_after
            )
            delete_pdf_files()
            st.success("PDF pages inserted successfully. Click below to download the final file.")
            st.download_button(
                label="Download Final PDF",
                data=final_pdf,
                file_name=f"{pdf_file_1.name.replace('.pdf', '')}_inserted.pdf",
                key="download_pdf"
            )
    except ValueError as e:
        st.error(f"Error: {str(e)}")
        delete_pdf_files()
else:
    st.info("Complete all steps to preview or insert pages.")