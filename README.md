
tvcf 챗봇 구동 방법 0.5V 기준 (구버전 설명)
=============================


1. python3 tvcf_documentUploader.py 실행  ->  벡터저장소및 Id 생성 or file 업로드  (id 현재는 터미널에서 복사해야함)
2. python3 tvcf_Assistant_creator.py 실행,(현재는 실행전에 vector_id에 1번에서 복사한내용 삽입)  -> assistant및 id 생성
3. streamlit run tvcf_customercenter.py 실행 (현재는 2번에서 가져온 assistant id 기입)





tvcf 챗봇 구동 방법 0.7V 기준
(api key 정보 확인 및 수정은 api_secrets.toml 확인)
=============================
1. (Option) streamlit run tvcf_documentUploader.py 실행해서 UI를따라 파일 업로드를하면됨 (새로운 공간만들꺼아니면 기존껄로)
2. (Option) python3 tvcf_Assistant_creator.py 실행 -> 새로운 벡터 space 또는 instruction 수정이 있을때만
3. streamlit run tvcf_customercenter.py 실행


# 버전 History
==========================


tvcf_docmentUploader
V0.5 -> create assistant 와분리
V0.6 -> openai 키 api_secrets.toml 에서 불러옴 (보안 강화)
V0.7-> Vector_id api_secrets.toml에 저장
V0.8 -> streamlit으로 UI를 넣어 vectorespace 설정,생성,파일 업로드 유동적으로 가능함
============================
tvcf_customercenter


V0.5 -> api 연동에러 수정 경고메시지 방지
V0.6 -> uploder,creator 분리에 따라 코드 분리
V0.7 -> source6.x등 불피요한 메시지 뜨는 Assistant Api 기본 문제 수정
V0.8 -> api_secrets.toml 파일에 open api및 assistant Api를 넣어둠 (보안 강화)

==============================
tvcf_Assistant_creator
V0.5 -> create 만 담당
V0.6 -> api key등 보안 관련 업데이트 완료

