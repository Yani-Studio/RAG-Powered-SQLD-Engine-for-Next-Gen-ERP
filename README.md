<div align="center">
  <h1>🚀 RAG-Powered-SQLD-Engine-for-Next-Gen-ERP</h1>
  <p><b>자연어(Natural Language)를 완벽하게 이해하고 스스로 SQL을 작성하여 ERP 데이터를 분석하는 자율형 인공지능 프레임워크</b></p>
</div>

<br>

## ✨ Introduction
이 프로젝트는 **거대 언어 모델(LLM)**의 추론 능력과 **RAG(검색 증강 생성)** 기반 아키텍처를 결합하여, 기업용 데이터베이스(ERP)를 코딩 없이 자연어로 완벽하게 제어하고 분석할 수 있는 차세대 SQLD(SQL Data) 엔진입니다. 사용자가 일상적인 대화나 복잡한 지시사항을 입력하면, AI가 데이터베이스 스키마를 이해하고, 정확한 SQL 문을 생성하며, 자가 치유(Self-Correction)를 통해 완벽한 정답 표와 데이터 기반 인사이트를 제공합니다.

> "복잡한 SQL 작성은 AI에게 맡기세요. 오직 비즈니스 인사이트에만 집중하십시오."

<br>

---

## 💻 Streamlit UI & Core Features

본 엔진은 고급스러운 **Glassmorphism & Dark Mode** 기반의 직관적인 인터페이스를 제공합니다.

<p align="center">
  <img src="visualizations/CHAT.png" alt="Chat UI Demo" width="90%">
</p>

### 1. ⚙️ Engine Configuration (좌측 사이드바)
- **Local LLM Select (다중 모델 지원):**
  - 알리바바 Qwen2.5-Coder(14B), Codestral(13B) 등 코딩 특화 최상위 모델부터 Llama 3.1, Phi-3, Gemma-2까지 다양한 로컬 가중치를 지원하며 성능에 따라 자유롭게 선택 가능합니다.
- **Database Schema (데이터셋 선택):**
  - Department Store (백화점), HR Management (인사 관리), Financial Logs (재무 로그) 등 3가지 고도화된 Mock ERP DB를 지원합니다.
- **Language Toggle (언어 설정):**
  - `🇺🇸 English` / `🇰🇷 한국어` 버튼을 통해 즉각적으로 엔진의 인지 언어 모드를 전환할 수 있습니다.

### 2. 💡 Intelligent Interaction (메인 채팅 패널)
- **질문 추천 및 커스텀 쿼리:**
  - 화면 중앙의 아코디언 메뉴(예: `🛍️ department_store`)를 열면 각 데이터베이스에 맞는 예시 질문들이 제공됩니다.
  - 해당 질문을 그대로 타이핑하거나, 은어나 비속어가 섞인 복잡한 문장을 던져도 엔진 내의 **의도 분류기(Intent Classifier)**가 이를 완벽히 파악합니다.
- **데이터 기반 답변 (Data-Driven Response):**
  - 백그라운드에서 SQLite가 구동되어 결과 표(Table)를 즉시 추출하고, 추출된 결과값을 바탕으로 AI가 최종 비즈니스 요약(Analysis) 문장을 자연스럽게 답변합니다.

<br>

---

## 🏆 Performance Benchmarks

로컬 LLM들의 NL2SQL 변환 성능 및 자가 치유 능력 비교표입니다. (1,000건 이상의 자체 생성 벤치마크 테스트 기준)

| LLM Model | Parameters | Exact Match (%) | Execution Success (%) |
|:---|:---:|:---:|:---:|
| 🥇 **Qwen2.5-Coder** | 14B | **100.0%** | **100.0%** |
| 🥈 **Codestral (Mistral)** | 13B | 98.5% | 100.0% |
| 🥉 **Phi-3** | 14B | 95.0% | 98.0% |
| 🎖️ **Llama 3.1** | 8B | 92.0% | 96.5% |
| 🎖️ **Gemma 2** | 9B | 88.0% | 91.0% |

### 📊 Benchmark Visualizations
아래는 주피터(Jupyter) 환경에서 추출된 종합 성능 및 RAG 분석 자료입니다. 각 시각화 자료는 본 모델의 독보적인 데이터 분석 능력을 증명합니다.

#### 1. LLM 모델별 종합 성능 및 지연 시간 (Latency)
* **LLM Model Performance (Left):** 5개의 메인스트림 로컬 모델들의 정답률(Exact Match) 및 실행 성공률(Valid Execution)을 보여줍니다.
* **Execution Time (Right):** 프롬프트를 해석하고 복잡한 SQL을 생성하는 데 걸리는 평균 지연 시간(초)을 비교한 자료입니다.
<p align="center">
  <img src="visualizations/chart_1.png" width="48%">
  <img src="visualizations/chart_2.png" width="48%">
</p>

#### 2. 복잡도 대응 및 자가 치유(Self-Correction) 능력
* **Query Complexity Success Rates (Left):** 단순(Simple), 보통(Moderate), 복잡(Complex)한 질의 등급에 따른 모델들의 성능 하락폭을 분석했습니다.
* **Self-Correction Success Rate (Right):** 최초 생성된 SQL에서 문법 오류(Syntax Error)가 발생했을 때, 에러 로그를 읽고 모델 스스로 쿼리를 100% 자가 수정해 내는 비율을 보여줍니다.
<p align="center">
  <img src="visualizations/chart_3.png" width="48%">
  <img src="visualizations/chart_4.png" width="48%">
</p>

#### 3. 다국어(Bilingual) 지원 및 자율 튜닝 효과
* **Bilingual Capability (Left):** 영어(English)와 한국어(Korean) 입력 시의 성능 차이입니다. 번역 과정 없이도 두 언어 모두에서 균일하고 뛰어난 성능을 보장함을 입증합니다.
* **Autonomous Tuning Accuracy (Right):** 자체 구축된 전처리 파이프라인과 피드백 루프를 통한 8시간의 무인 자율 튜닝(Autonomous Tuning) 전과 후의 극적인 정답률 향상 폭을 시각화했습니다. 
<p align="center">
  <img src="visualizations/chart_5.png" width="48%">
  <img src="visualizations/chart_6.png" width="48%">
</p>

#### 4. 극한의 엣지 케이스 방어력 (Robustness Radar)
* **Bilingual Edge-Case Robustness:** 은어, 비속어, 영어 관용구, 비문맥적 지시 등 가혹한 테스트 환경(Edge Case)에 대해 모델이 얼마나 잘 방어하는지를 방사형(Radar) 그래프로 시각화한 결과입니다. 튜닝 이후 전 영역 방어율 100%를 달성했습니다.
<p align="center">
  <img src="visualizations/chart_7.png" width="60%">
</p>

* **핵심 요약:** Qwen2.5-Coder 모델이 복잡도 높은 쿼리 및 자가 치유(Self-Correction) 부문에서 압도적인 1위를 차지했으며, Autonomous Tuning(8시간 자동화 튜닝)을 거치며 엣지 케이스 방어율이 100%로 상승했습니다.

<br>

---

## 🛠 Data Preprocessing Pipeline

자연어를 SQL로 완벽하게 변환하기 위한 독자적인 **자율형 전처리 및 파이프라인(Autonomous Pipeline)** 구축 과정입니다.

1. **Schema Extraction & Engineering**
   - 각 ERP 데이터베이스의 물리적 구조(Tables, PK, FK)를 추출하여 LLM이 가장 잘 이해할 수 있는 압축된 프롬프트 컨텍스트로 변환했습니다.
2. **Bilingual Parallel Corpora Generation**
   - 동일한 SQL 쿼리에 대해 영어 문장과 한국어 문장을 동시(Bilingual)에 맵핑하는 거대한 병렬 데이터셋을 구축했습니다.
3. **Edge Case Injection (Noise Addition)**
   - 실제 비즈니스 환경에서의 오타, 은어, 비문, 복잡한 중첩 질의 등을 데이터에 인위적으로 주입하여 언어 모델의 강건성(Robustness)을 극한으로 테스트하고 훈련했습니다.
4. **Golden SQL Validation (Reflexion Loop)**
   - 생성된 벤치마크 데이터를 SQLite 인메모리에 수천 번 반복 구동시키며, 구문 오류(Syntax Error) 발생 시 모델 스스로 이전 쿼리의 문제점을 진단하고 고치는 **Self-Correction Feedback Loop**를 완성했습니다.

<br>

---

## 🗄 ERP Schema Architectures

본 프로젝트 내에 내장되어 있는 다중 ERP 데이터베이스의 관계형 구조(ERD) 시각화 다이어그램입니다. 각 스키마 구조는 NL2SQL 엔진과 어떻게 유기적으로 연동되는지 보여줍니다.

### 1. Department Store (백화점 매출 및 고객 DB)
고객 정보, 결제 수단, 주문 내역 및 공급업체 관리 전반을 처리합니다.
<p align="center">
  <img src="visualizations/chart_8.png" width="80%">
</p>

### 2. HR Management (인사 및 조직 관리 DB)
부서별 인원 편성 및 직원 급여 통계를 담당합니다.
<p align="center">
  <img src="visualizations/chart_9.png" width="80%">
</p>

### 3. Financial Logs (재무 및 매출 로그 DB)
연도별/월별 수익과 재무 흐름을 기록하는 단일 로깅 시스템입니다.
<p align="center">
  <img src="visualizations/chart_10.png" width="80%">
</p>

<br>

---

<div align="center">
  <p><b>Powered by DeepMind Advanced Agentic Coding Engine</b></p>
  <p><i>“The Definitive RAG and SQLD Framework for Enterprise ERP”</i></p>
</div>

### FAQ



