# GitHub 공개 전 체크리스트

- [ ] `src/`의 HWPX·DOCX·PDF 원본을 공개 재배포할 수 있는지 확인
- [ ] 문서에 개인정보, 내부 연락처, 서명 또는 비공개 회의정보가 없는지 확인
- [ ] `data/quality_issues.csv`의 경고를 원문 담당 부서에 확인
- [ ] 저장소 라이선스와 데이터 라이선스를 결정
- [ ] `README.md`의 비공식 자료 면책문구 확인
- [ ] `tmp/`가 Git에 포함되지 않는지 확인
- [ ] `python scripts/verify_dataset.py`가 통과하는지 확인
- [ ] `graphify-out/graph.html`이 로컬 브라우저에서 열리는지 확인

GitHub의 일반 파일 보기 화면에서는 대화형 HTML의 JavaScript가 실행되지 않습니다. 공개 그래프를 웹에서 직접 보여주려면 GitHub Pages를 별도로 설정해야 합니다.
