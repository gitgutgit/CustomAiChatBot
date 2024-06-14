
# TVCF 챗봇 구동 방법 안내

(app.py is recent version of tvcf_customercenter.py)
## 0.5V 기준 (구버전 설명)

1. **벡터 저장소 및 파일 업로드**  
   `python3 tvcf_documentUploader.py` 실행  
   벡터 저장소 및 ID 생성 또는 파일 업로드  
   *(ID는 현재 터미널에서 복사해야 합니다)*

2. **Assistant 생성**  
   `python3 tvcf_Assistant_creator.py` 실행  
   (실행 전에 vector_id에 1번에서 복사한 내용 삽입 필요)  
   Assistant 및 ID 생성

3. **고객 센터 실행**  
   `streamlit run tvcf_customercenter.py` 실행  
   *(현재는 2번에서 가져온 assistant ID 기입 필요)*

## 0.7V 기준 (최신 버전)

*(API key 정보 확인 및 수정은 `api_secrets.toml` 확인)*

1. **(선택 사항) 파일 업로드**  
   `streamlit run tvcf_documentUploader.py` 실행하여 UI를 통해 파일 업로드  
   *(새로운 공간을 만들지 않는다면 기존 공간 사용 가능)*

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

## tvcf_Assistant_creator
- **V0.5**: Create 기능 담당
- **V0.6**: API key 등 보안 관련 업데이트 완료

---

이 문서를 통해 TVCF 챗봇의 구버전 및 최신 버전 구동 방법과 각 버전의 업데이트 내용을 확인할 수 있습니다. 최신 버전에서는 보안이 강화되고 UI가 개선되어 사용이 더욱 편리해졌습니다.
