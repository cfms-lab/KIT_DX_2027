# DX대학 교육과정 데이터

금오공과대학교 DX대학 소속 9개 전공의 2026학년도 교육과정을 재사용 가능한 CSV, SQLite, Graphify 형식으로 정리한 저장소입니다.

## 대상 전공

- 건축공학전공
- 토목공학전공
- 산업공학전공
- 수리빅데이터전공
- 고분자공학전공
- 신소재공학전공
- 소재디자인공학전공
- 화학공학전공
- 화학생명소재전공

공학교육인증 유지 전공은 고분자공학, 신소재공학, 소재디자인공학, 화학공학의 4개 전공입니다.

## 데이터 파일

- `data/departments.csv`: 전공 목록과 공학교육인증 여부
- `data/course_offerings.csv`: 전공·학년·학기별 교과목 원자료
- `data/course_overlap.csv`: 정규화 과목명 기준 전공 간 중복 집계
- `data/quality_issues.csv`: 원문 오기 가능성, 과목명 정규화, 다중 코드 항목
- `data/dx_curriculum.sqlite`: 위 자료와 재사용 가능한 SQL 뷰를 포함한 SQLite 데이터베이스
- `graphify-out/graph.html`: 대화형 지식 그래프
- `graphify-out/graph.json`: GraphRAG 및 후속 분석용 그래프 데이터
- `graphify-out/GRAPH_REPORT.md`: 그래프 감사 보고서

CSV는 Excel에서 한글이 깨지지 않도록 UTF-8 BOM으로 저장합니다. `course_offerings.csv`는 원문 과목명과 정규화 과목명을 모두 보존합니다.

## 필수 여부 해석

- `is_curriculum_required`: 교육과정표의 `교필` 또는 `전필` 표기
- `is_policy_required`: 교육과정표의 선택 표기와 별개인 공학교육인증 요건
- `is_effectively_required`: 위 두 조건 중 하나 이상이 참

따라서 소재디자인공학·화학공학의 `창의입문설계`처럼 원표가 `전선`이더라도 공학교육인증 유지에 필요한 경우를 별도로 조회할 수 있습니다. 화학생명소재전공의 `창의입문설계`는 선택과목으로 유지됩니다.

## 재생성

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts\build_curriculum_dataset.py
.\.venv\Scripts\python.exe scripts\verify_dataset.py
```

간단한 검색은 SQLite 프로그램 없이도 실행할 수 있습니다.

```powershell
python scripts\query_curriculum.py --course 확률및통계
python scripts\query_curriculum.py --department 소재디자인
python scripts\query_curriculum.py --later-msc-overlap
```

## SQLite 예제 질의

2개 전공 이상에서 공통으로 요구되는 2~4학년 MSC 과목:

```sql
SELECT *
FROM v_later_msc_required_overlap
ORDER BY department_count DESC, course_name_canonical;
```

1학년 유효 필수 교과목:

```sql
SELECT department_name, semester, course_name_canonical, required_reason
FROM v_first_year_effective_required
ORDER BY department_name, semester, course_name_canonical;
```

## Graphify 사용

```powershell
graphify query "2~4학년 공통 MSC 필수과목"
graphify explain "창의입문설계"
graphify path "소재디자인공학전공" "확률및통계"
```

Graphify는 관계 탐색용입니다. 학년·학기·필수 여부의 최종 확인에는 CSV/SQLite의 원문 추적 필드를 우선 사용하십시오.
`scripts/build_graphify_seed.py`는 SQLite의 전체 교과목 관계를 Graphify 호환 추출 형식으로 변환하여, 의미 추출에서 누락될 수 있는 과목도 그래프에 남깁니다.

## 공개 전 확인

- `src/` 원본 문서의 공개 재배포 가능 여부를 확인하십시오.
- 공식 문서의 오기 가능성은 `data/quality_issues.csv`에서 확인하십시오.
- 저장소 라이선스는 원본 문서의 저작권과 데이터 재사용 범위를 확인한 뒤 추가하십시오.
- 이 저장소는 공식 학사 안내를 대체하지 않습니다.
