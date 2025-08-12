PDF Editor Application
This is a simple PDF Editor Application developed by Parimal Hodar (parimal.court@gmail.com). It allows users to perform various operations on PDF files, such as merging, compressing, splitting, and inserting one PDF into another. The application is built using Streamlit and leverages the PyPDF2 library for PDF manipulation.
This repository is tailored for streamlit.io deployments and is running on editpdfs.streamlit.app for you to explore.
If you like the app and want to fund similar open-source projects: 
Application Pages
Home Page

Welcoming message and navigation instructions.

PDF Merger Page

Upload and merge multiple PDF files into one PDF file.

PDF Compression Page

Upload and compress a PDF file to reduce its size using PyPDF2 or Ghostscript (if available).

PDF Slicer Page

Upload and slice a PDF file to extract specific pages and create a new PDF file.

PDF Inserter Page

Upload two PDF files and insert the second file after a specified page of the first file. Select specific page ranges as needed.

Watermarking Page

Upload a PDF file and add a watermark with customizable text, color, and position (Confidential or DoNotCopy, Red or Grey, Overlay or Underlay).

Installation

Clone the repository:
git clone https://github.com/your-username/PDF_Editor_StreamlitDeployment.git
cd PDF_Editor_StreamlitDeployment


Install the required Python packages:
pip install -r requirements.txt


For Ghostscript Compression (optional):

Install the Ghostscript binary:
Windows: Download from Ghostscript Downloads and add to PATH.
Linux: Run sudo apt install ghostscript.
Mac: Run brew install ghostscript.


Install the Python package:pip install ghostscript==0.7




Ensure the assets/ directory contains watermark PDFs (Confidential_Red.pdf, Confidential_Grey.pdf, DoNotCopy_Red.pdf, DoNotCopy_Grey.pdf).

Run the application:
streamlit run app.py



Credits

The application utilizes the PyPDF2 library for PDF manipulation.
Ghostscript is used for advanced PDF compression. Visit Ghostscript for more information.
Credits to the PyPDF2 and Ghostscript developers for their contributions to the open-source community.

Conclusion
This PDF Editor Application provides a user-friendly interface for common PDF editing tasks. Feel free to explore and enhance your PDFs seamlessly!
by Parimal Hodar (parimal.court@gmail.com)