# 데이터 사전

## `course_offerings.csv`

한 행은 한 전공에서 한 학기 동안 개설되는 교과목 하나를 뜻합니다.

| 열 | 의미 |
|---|---|
| `offering_id` | 이 데이터셋 안에서의 개설 레코드 ID |
| `department_id`, `department_name` | 전공 식별자와 전공명 |
| `curriculum_area` | `general_common`, `academic_foundation_msc`, `major` 중 하나 |
| `year`, `semester` | 권장/편성 학년과 학기. `year=0`은 전학년 과목 |
| `requirement_type_raw` | 원문 이수구분 |
| `is_curriculum_required` | 원문 교육과정표의 필수 표기 |
| `is_policy_required` | 공학교육인증 등 별도 정책에 따른 필수 여부 |
| `is_effectively_required` | 원문 필수 또는 정책 필수 중 하나 이상 |
| `course_name_raw` | 원문 과목명 |
| `course_name_canonical` | 공백·주석표시 등을 제거한 비교용 과목명 |
| `credit_structure_raw` | 원문의 `학점-강의-설계-실습` 문자열 |
| `source_table_index`, `source_row_index` | DOCX 내부의 0부터 시작하는 표/행 위치 |
| `normalization_note`, `quality_flag` | 정규화와 검토 필요 사항 |

## SQLite 뷰

| 뷰 | 용도 |
|---|---|
| `v_first_year_effective_required` | 전공별 1학년 유효 필수 과목 |
| `v_required_course_overlap` | 2개 전공 이상 공통 유효 필수 과목 |
| `v_later_msc_required_overlap` | 2~4학년 MSC 필수 중 2개 전공 이상 공통 과목 |

## 정규화 원칙

1. 원문은 절대 덮어쓰지 않고 `*_raw` 열에 보존합니다.
2. 비교용 과목명에서는 공백과 원문의 주석표시 `*`를 제거합니다.
3. 소재디자인공학전공의 `LA0502 일반물리학실험`은 같은 코드 기준으로 `일반물리학실험1`에 정규화합니다.
4. 건축공학전공의 `LA0508 일반물리학2`는 수정하지 않고 오기 가능성 플래그만 부여합니다.
5. 동일 과목명이 여러 코드로 존재해도 자동으로 동일인정 과목이라고 단정하지 않습니다.
