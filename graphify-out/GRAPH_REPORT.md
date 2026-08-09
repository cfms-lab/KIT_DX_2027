# Graph Report - D:\OneDrive\Documents\__잡무(backup_20190531)\_2026\_미래융합대학_교육과정  (2026-08-09)

## Corpus Check
- Corpus is ~31,132 words - fits in a single context window. You may not need a graph.

## Summary
- 379 nodes · 523 edges · 12 communities
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- 신소재공학
- 수리빅데이터·공통기초
- 산업공학
- 토목공학
- 화학생명소재
- 소재디자인
- 고분자공학
- 건축공학
- 화학공학
- 학사운영·교육과정 규정
- 학년후반 MSC 공통과목
- 수강신청·등록

## God Nodes (most connected - your core abstractions)
1. `신소재공학전공` - 74 edges
2. `화학생명소재전공` - 54 edges
3. `고분자공학전공` - 54 edges
4. `소재디자인공학전공` - 53 edges
5. `화학공학전공` - 52 edges
6. `토목공학전공` - 51 edges
7. `산업공학전공` - 50 edges
8. `수리빅데이터전공` - 45 edges
9. `건축공학전공` - 41 edges
10. `글로벌커뮤니케이션` - 10 edges

## Surprising Connections (you probably didn't know these)
- `DX대학 교육과정 지식 그래프 코퍼스` --references--> `건축공학전공`  [EXTRACTED]
  graph_corpus/overview.md → data/departments.csv
- `DX대학 교육과정 지식 그래프 코퍼스` --references--> `화학생명소재전공`  [EXTRACTED]
  graph_corpus/overview.md → data/departments.csv
- `화학공학전공` --implements--> `공학교육인증 유지`  [EXTRACTED]
  data/departments.csv → graph_corpus/departments/CHEMENG_화학공학전공.md
- `DX대학 교육과정 지식 그래프 코퍼스` --references--> `화학공학전공`  [EXTRACTED]
  graph_corpus/overview.md → data/departments.csv
- `DX대학 교육과정 지식 그래프 코퍼스` --references--> `토목공학전공`  [EXTRACTED]
  graph_corpus/overview.md → data/departments.csv

## Hyperedges (group relationships)
- **고급프로그래밍언어 공통 필수 전공군** — data_department_ind, data_department_matdes, data_department_mathdata, data_course_ba7ee899db72 [EXTRACTED 1.00]
- **공학수학 공통 필수 전공군** — data_department_arch, data_department_civil, data_department_ind, data_course_b15aa55faa45 [EXTRACTED 1.00]
- **공학수학1 공통 필수 전공군** — data_department_chemeng, data_department_mse, data_department_poly, data_course_75a4563b765f [EXTRACTED 1.00]
- **공학수학2 공통 필수 전공군** — data_department_chemeng, data_department_mse, data_department_poly, data_course_13f4709c7a3e [EXTRACTED 1.00]
- **글로벌커뮤니케이션 공통 필수 전공군** — data_department_arch, data_department_chembio, data_department_chemeng, data_department_civil, data_department_ind, data_department_matdes, data_department_mathdata, data_department_mse, data_department_poly, data_course_70116cd9076c [EXTRACTED 1.00]
- **글쓰기와발표 공통 필수 전공군** — data_department_arch, data_department_chembio, data_department_chemeng, data_department_civil, data_department_ind, data_department_matdes, data_department_mathdata, data_department_mse, data_department_poly, data_course_b54aceee45f2 [EXTRACTED 1.00]
- **대학수학1 공통 필수 전공군** — data_department_arch, data_department_chembio, data_department_chemeng, data_department_civil, data_department_ind, data_department_matdes, data_department_mathdata, data_department_mse, data_department_poly, data_course_8ce53b6c5858 [EXTRACTED 1.00]
- **대학수학2 공통 필수 전공군** — data_department_arch, data_department_chembio, data_department_chemeng, data_department_civil, data_department_ind, data_department_matdes, data_department_mathdata, data_department_mse, data_department_poly, data_course_33f87636d122 [EXTRACTED 1.00]
- **디지털문해력 공통 필수 전공군** — data_department_arch, data_department_chembio, data_department_chemeng, data_department_civil, data_department_ind, data_department_matdes, data_department_mathdata, data_department_mse, data_department_poly, data_course_918902aac35f [EXTRACTED 1.00]
- **물리화학2 공통 필수 전공군** — data_department_chembio, data_department_chemeng, data_course_9e511789db22 [EXTRACTED 1.00]
- **유기화학1 공통 필수 전공군** — data_department_chembio, data_department_poly, data_course_d54c2021bedf [EXTRACTED 1.00]
- **유기화학2 공통 필수 전공군** — data_department_chemeng, data_department_matdes, data_course_ea1d5f2d9436 [EXTRACTED 1.00]
- **일반물리학1 공통 필수 전공군** — data_department_arch, data_department_chembio, data_department_chemeng, data_department_civil, data_department_matdes, data_department_mse, data_department_poly, data_course_f1acb90f1949 [EXTRACTED 1.00]
- **일반물리학2 공통 필수 전공군** — data_department_arch, data_department_chembio, data_department_chemeng, data_department_civil, data_department_matdes, data_department_mse, data_department_poly, data_course_2d0f67659d50 [EXTRACTED 1.00]
- **일반물리학실험1 공통 필수 전공군** — data_department_chembio, data_department_chemeng, data_department_matdes, data_department_mse, data_department_poly, data_course_656342435f16 [EXTRACTED 1.00]
- **일반물리학실험2 공통 필수 전공군** — data_department_chembio, data_department_chemeng, data_department_matdes, data_department_mse, data_department_poly, data_course_0180e6e165bd [EXTRACTED 1.00]
- **일반화학1 공통 필수 전공군** — data_department_arch, data_department_chembio, data_department_chemeng, data_department_civil, data_department_matdes, data_department_mse, data_department_poly, data_course_605011f4fd44 [EXTRACTED 1.00]
- **일반화학2 공통 필수 전공군** — data_department_chembio, data_department_chemeng, data_department_matdes, data_department_mse, data_department_poly, data_course_299cde44c897 [EXTRACTED 1.00]
- **일반화학실험1 공통 필수 전공군** — data_department_chembio, data_department_chemeng, data_department_matdes, data_department_mse, data_department_poly, data_course_2be52e1e81d6 [EXTRACTED 1.00]
- **일반화학실험2 공통 필수 전공군** — data_department_chembio, data_department_chemeng, data_department_matdes, data_department_mse, data_department_poly, data_course_74649719c15f [EXTRACTED 1.00]
- **창의입문설계 공통 필수 전공군** — data_department_chemeng, data_department_matdes, data_department_mse, data_department_poly, data_course_d14f525f62f5 [EXTRACTED 1.00]
- **컴퓨터프로그래밍언어 공통 필수 전공군** — data_department_civil, data_department_ind, data_department_mathdata, data_course_9388000d5b2f [EXTRACTED 1.00]
- **확률및통계 공통 필수 전공군** — data_department_arch, data_department_civil, data_department_ind, data_department_matdes, data_department_mathdata, data_course_4fb4d5178996 [EXTRACTED 1.00]
- **9개 전공 공통 필수 기초교과목** — data_department_arch, data_department_chembio, data_department_chemeng, data_department_civil, data_department_ind, data_department_matdes, data_department_mathdata, data_department_mse, data_department_poly, data_course_70116cd9076c, data_course_b54aceee45f2, data_course_8ce53b6c5858, data_course_33f87636d122, data_course_918902aac35f [EXTRACTED 1.00]
- **물리·화학 이론 및 실험 전과정 필수 전공군** — data_department_chembio, data_department_chemeng, data_department_matdes, data_department_mse, data_department_poly, data_course_f1acb90f1949, data_course_2d0f67659d50, data_course_656342435f16, data_course_0180e6e165bd, data_course_605011f4fd44, data_course_299cde44c897, data_course_2be52e1e81d6, data_course_74649719c15f [EXTRACTED 1.00]

## Communities (12 total, 0 thin omitted)

### Community 0 - "신소재공학"
Cohesion: 0.04
Nodes (52): 반도체소자, X-선공학및설계, 재료의파괴와손상, 에너지재료설계, 기능금속재료, 재료안전실무, 철강재료, 재료과학2 (+44 more)

### Community 1 - "수리빅데이터·공통기초"
Cohesion: 0.05
Nodes (44): 1학년 9개 전공 공통 필수과목, Python을이용한통계프로그래밍, R을이용한통계프로그래밍, 시스템프로그래밍(CapstoneDesign), 선형대수학, 통계적학습, 다변수해석학, 통계학개론 (+36 more)

### Community 2 - "산업공학"
Cohesion: 0.05
Nodes (40): 산업안전공학, 제조시스템공학, 시스템최적화, 데이터분석, 데이터기반의사결정, 생산정보시스템, 제품및시스템디자인, 빅데이터의세계 (+32 more)

### Community 3 - "토목공학"
Cohesion: 0.05
Nodes (39): 도시환경수문학, 암반역학, 일반물리학2, 재료역학2, 토질역학및실험1, 졸업논문2(CapstoneDesign2), 컴퓨터수치해석, 토질역학및실험2 (+31 more)

### Community 4 - "화학생명소재"
Cohesion: 0.05
Nodes (38): 세포생물학1, 면역학, 구조화학, 재료화학2, 일반화학2, 화학생명소재실험2, 화학생명소재종합설계1, 화학생명소재실험1 (+30 more)

### Community 5 - "소재디자인"
Cohesion: 0.06
Nodes (35): 일반물리학실험2, NT융합소재, 패션텍스타일, 기능성어패럴제품설계, 일반화학실험1, 신소재탄소재료, 패션브랜딩, 신소재합성 (+27 more)

### Community 6 - "고분자공학"
Cohesion: 0.06
Nodes (34): 유기정보소재, 종합설계, 고분자기초실험, 물리화학1, 기능성고분자, 고분자분석설계, 고분자물성1, 고분자재료2 (+26 more)

### Community 7 - "건축공학"
Cohesion: 0.06
Nodes (32): 건축융합시스템설계1(종합설계), 건축법규, 건축프로젝트기획및실습, 스마트그린빌딩의이해, 건축구조시스템, 공학역학, 강구조, 건축토목환경공학개론 (+24 more)

### Community 8 - "화학공학"
Cohesion: 0.07
Nodes (30): 유체역학, 분리공정, 열및물질전달, 화공개론, 나노바이오공학, 반응공학, 화공프로그래밍기초, 화공양론 (+22 more)

### Community 9 - "학사운영·교육과정 규정"
Cohesion: 0.10
Nodes (27): 학문기초 교과목, 국립금오공과대학교 학사운영 규정, 공학교육인증 시행 대상 전공, 자율전공학부 전공 선택 및 배정, 전과, 전과자의 전입 학과 필수과목 이수 의무, 교육과정 이수, 입학년도별 교육과정 이수 기준표 (+19 more)

### Community 10 - "학년후반 MSC 공통과목"
Cohesion: 0.60
Nodes (5): 2~4학년 공통 MSC 필수과목, 공학수학2, 확률및통계, 공학수학1, 공학수학

### Community 11 - "수강신청·등록"
Cohesion: 0.67
Nodes (3): 수강신청, 수강신청 취소 및 삭제, 등록 완료 요건

## Knowledge Gaps
- **308 isolated node(s):** `3D어패럴캐드`, `3D프로토타이핑`, `CAD및실습`, `CAE`, `HCI` (+303 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `신소재공학전공` connect `신소재공학` to `수리빅데이터·공통기초`, `산업공학`, `토목공학`, `화학생명소재`, `소재디자인`, `고분자공학`, `건축공학`, `화학공학`, `학년후반 MSC 공통과목`?**
  _High betweenness centrality (0.242) - this node is a cross-community bridge._
- **Why does `토목공학전공` connect `토목공학` to `수리빅데이터·공통기초`, `학년후반 MSC 공통과목`, `산업공학`, `건축공학`?**
  _High betweenness centrality (0.176) - this node is a cross-community bridge._
- **Why does `산업공학전공` connect `산업공학` to `화학공학`, `수리빅데이터·공통기초`, `학년후반 MSC 공통과목`?**
  _High betweenness centrality (0.173) - this node is a cross-community bridge._
- **What connects `3D어패럴캐드`, `3D프로토타이핑`, `CAD및실습` to the rest of the system?**
  _308 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `신소재공학` be split into smaller, more focused modules?**
  _Cohesion score 0.038461538461538464 - nodes in this community are weakly interconnected._
- **Should `수리빅데이터·공통기초` be split into smaller, more focused modules?**
  _Cohesion score 0.0507399577167019 - nodes in this community are weakly interconnected._
- **Should `산업공학` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._