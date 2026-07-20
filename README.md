# PUBG 플레이어 성과 분석 프로젝트

PUBG(배틀그라운드) 플레이어의 최근 매치 데이터를 수집·분석하는 프로젝트입니다.
플레이어의 **킬 수, 생존 시간, 순위**를 기반으로 성과를 분석하고, 이 지표들 간의 상관관계를 살펴봅니다.

## 구성

이 프로젝트는 두 부분으로 이루어져 있습니다.

### 1. 데이터 분석 (Jupyter Notebook)
유명 스트리머 4명의 최근 매치 데이터를 수집해 킬 수·생존 시간·순위의 상관관계를 분석합니다.

- `Term_Project_MAIN.ipynb` : 메인 분석 노트북 (가설 정의 → 데이터 수집 → 가공 → 분석 → 결론)
- `match_data_get.py` : PUBG API로 플레이어의 매치 데이터를 수집해 CSV로 저장하는 스크립트
- `player_stats.csv` : 수집된 플레이어 통계 데이터 (name, kills, timeSurvived, rank)

### 2. 웹 페이지 (닉네임 검색 도구)
닉네임을 입력하면 해당 플레이어의 최근 매치별 성과를 조회·분석하는 웹 페이지입니다.

- `index.html` : 단일 HTML 파일. 닉네임 검색 → 매치별 킬 수/생존시간/순위 분석 → 평균 통계 및 CSV 다운로드

## 실행 방법

### Jupyter Notebook
```bash
pip install -r requirements.txt
jupyter notebook Term_Project_MAIN.ipynb
```

### 웹 페이지
1. [developer.pubg.com](https://developer.pubg.com)에서 API 키를 발급받습니다.
2. 프로젝트 폴더에 `config.csv` 파일을 만들고 아래처럼 키를 입력합니다.
   ```
   api_key
   여기에_발급받은_API_키
   ```
3. 로컬 서버를 실행합니다 (파일을 직접 열면 브라우저 보안 정책 때문에 config.csv를 읽지 못합니다).
   ```bash
   python -m http.server
   ```
4. 브라우저에서 `http://localhost:8000` 에 접속합니다.

> `config.csv`는 API 키가 담긴 파일이므로 `.gitignore`에 등록되어 깃허브에 올라가지 않습니다.

## 분석 지표

각 매치에서 다음 항목을 추출해 분석합니다.

| 항목 | 설명 |
|------|------|
| kills | 해당 매치의 킬 수 |
| timeSurvived | 생존 시간 (초) |
| rank | 최종 순위 (winPlace) |

## 참고

- PUBG Developer API: https://developer.pubg.com/
- 매치 데이터는 최근 14일치만 조회 가능합니다.
- 무료 API 키는 분당 10건의 요청 제한이 있습니다.
