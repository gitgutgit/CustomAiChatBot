# TVCF Chatbot Guide

- [English Version](#English-version)
- [한국어 버전](#한국어-버전)

## English Version

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

## 한국어 버전

# TVCF 챗봇 구동 방법 안내

(app.py is recent version of tvcf_customercenter.py)

## 0.5V 기준 (구버전 설명)

1. **벡터 저장소 및 파일 업로드**  
   `python3 tvcf_documentUploader.py` 실행  
   벡터 저장소 및 ID 생성 또는 파일 업로드  
   _(ID는 현재 터미널에서 복사해야 합니다)_

2. **Assistant 생성**  
   `python3 tvcf_Assistant_creator.py` 실행  
   (실행 전에 vector_id에 1번에서 복사한 내용 삽입 필요)  
   Assistant 및 ID 생성

3. **고객 센터 실행**  
   `streamlit run tvcf_customercenter.py` 실행  
   _(현재는 2번에서 가져온 assistant ID 기입 필요)_

## 0.7V 기준 (최신 버전)

_(API key 정보 확인 및 수정은 `api_secrets.toml` 확인)_

1. **(선택 사항) 파일 업로드**  
   `streamlit run tvcf_documentUploader.py` 실행하여 UI를 통해 파일 업로드  
   _(새로운 공간을 만들지 않는다면 기존 공간 사용 가능)_

2. **(선택 사항) Assistant 생성**  
   `python3 tvcf_Assistant_creator.py` 실행  
   새로운 벡터 공간 생성 또는 instruction 수정 시에만 필요

3. **고객 센터 실행**  
   `streamlit run tvcf_customercenter.py` 실행

# 버전 히스토리

## tvcf_documentUploader

- **V0.5**: create assistant와 분리
- **V0.6**: openai 키를 `api_secrets.toml`에서 불러옴 (보안 강화)
- **V0.7**: Vector_id를 `api_secrets.toml`에 저장
- **V0.8**: Streamlit으로 UI 추가, 벡터 공간 설정, 생성, 파일 업로드 유동적으로 가능

## tvcf_customercenter

- **V0.5**: API 연동 에러 수정, 경고 메시지 방지
- **V0.6**: Uploader, Creator 분리에 따라 코드 분리
- **V0.7**: 불필요한 메시지 출력 수정
- **V0.8**: `api_secrets.toml` 파일에 Open API 및 Assistant API 저장 (보안 강화)
- **V0.9**: `api_secrets.toml` 파일존재하지않을때 내부 secrets.toml 에 작동하게 만듬

## tvcf_Assistant_creator

- **V0.5**: Create 기능 담당
- **V0.6**: API key 등 보안 관련 업데이트 완료

---

이 문서를 통해 TVCF 챗봇의 구버전 및 최신 버전 구동 방법과 각 버전의 업데이트 내용을 확인할 수 있습니다. 최신 버전에서는 보안이 강화되고 UI가 개선되어 사용이 더욱 편리해졌습니다.
