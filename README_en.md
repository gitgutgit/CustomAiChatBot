# TVCF Chatbot Execution Guide

(app.py is the recent version of tvcf_customercenter.py)

## Version 0.5 (Old Version Instructions)

1. **Vector Store and File Upload**  
   Run `python3 tvcf_documentUploader.py`  
   This will create a vector store and generate an ID, or allow you to upload a file.  
   _(You need to copy the ID from the terminal)_

2. **Assistant Creation**  
   Run `python3 tvcf_Assistant_creator.py`  
   (Before running, you need to insert the ID copied from step 1 into vector_id)  
   This will create an Assistant and generate an ID.

3. **Run Customer Center**  
   Run `streamlit run tvcf_customercenter.py`  
   _(You will need to insert the assistant ID generated in step 2)_

## Version 0.7 (Latest Version)

_(For API key info, check and modify `api_secrets.toml`)_

1. **(Optional) File Upload**  
   Run `streamlit run tvcf_documentUploader.py` and use the UI to upload files.  
   _(You can use an existing vector space if you don’t want to create a new one)_

2. **(Optional) Assistant Creation**  
   Run `python3 tvcf_Assistant_creator.py`  
   Only required if creating a new vector space or modifying instructions.

3. **Run Customer Center**  
   Run `streamlit run tvcf_customercenter.py`

---

# Version History

## tvcf_documentUploader

- **V0.5**: Separated from the create assistant function.
- **V0.6**: API keys are loaded from `api_secrets.toml` (enhanced security).
- **V0.7**: Vector_id is now stored in `api_secrets.toml`.
- **V0.8**: Added Streamlit UI, making vector space creation and file uploads flexible.

## tvcf_customercenter

- **V0.5**: Fixed API integration errors and prevented warning messages.
- **V0.6**: Code separated based on Uploader and Creator separation.
- **V0.7**: Removed unnecessary message outputs.
- **V0.8**: OpenAPI and Assistant API keys stored in `api_secrets.toml` (enhanced security).
- **V0.9**: Added fallback to internal `secrets.toml` if `api_secrets.toml` is missing.

## tvcf_Assistant_creator

- **V0.5**: Responsible for the Create functionality.
- **V0.6**: Security updates completed, including API keys.

---

This document explains how to run the TVCF chatbot for both older and newer versions, as well as detailing version updates. The latest version has enhanced security and improved UI for easier use.
