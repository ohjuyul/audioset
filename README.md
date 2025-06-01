# AudioSet 오디오 처리 파이프라인

유튜브 AudioSet 오디오 데이터를 쉽고 체계적으로 다운로드하고, 필요한 구간만큼 잘라내며, 리샘플링과 메타정보 추출, 통계 요약까지 한 번에 처리하는 파이썬 스크립트 모음입니다.  
복잡한 오디오 데이터 준비 과정을 단순화해, 분석과 연구에 집중할 수 있도록 돕습니다.

---

## 주요 기능

### 1. `sound.py` — 오디오 다운로드 및 트리밍  
`sound.py`는 AudioSet 라벨을 기반으로 유튜브에서 오디오 클립을 다운로드합니다.  
다운로드한 원본 오디오는 `full/` 폴더에 저장되고, 지정한 구간만큼 잘라낸 클립은 `Result/` 폴더에 저장됩니다.  
라벨과 클립 정보는 `ontology.json`, `data.txt`에서 불러와 사용합니다.  
예를 들어, 아래처럼 실행합니다:

```bash
python sound.py --label "fire alarm" "explosion" --num 10 --exclude "speech"
```

위 명령어는 `"fire alarm"`과 `"explosion"` 라벨 중 10개씩 다운로드하며 `"speech"` 라벨은 제외합니다.

---

### 2. `resample.py` — 최적화된 리샘플링  
`resample.py`는 `Result/` 폴더 내 오디오 클립들을 불러와 각 파일의 최대 주파수를 분석합니다.  
그에 맞는 최적 샘플링 레이트로 리샘플링해 품질 저하를 최소화하고 파일 용량을 줄입니다.  
리샘플링된 파일은 `resample/` 폴더에 저장되며, 진행 상황은 프로그래스바로 확인할 수 있습니다.

---

### 3. `information.py` — 메타정보 자동 추출  
리샘플링된 오디오 파일들을 스캔해, 절대 경로, 라벨명, 오디오 길이(초), 샘플링 레이트 정보를 CSV 파일로 정리합니다.  
라벨명은 파일명에서 자동 추출되어 수작업 없이 분류가 가능합니다.

---

### 4. `summerize.py` — 라벨별 오디오 길이 통계  
생성된 CSV를 불러와 라벨별 오디오 길이 통계를 계산합니다.  
통계항목은 개수, 평균, 분산, 최대/최소 길이를 포함하며, 전체 데이터 통계도 함께 출력합니다.  
결과는 콘솔 출력과 `sum.csv` 파일 저장으로 제공합니다.

---

## 전체 작업 흐름 예시

1. 오디오 다운로드 및 트리밍  
   원하는 라벨로 `sound.py`를 실행해 유튜브에서 오디오를 받고, 필요한 구간만큼 잘라냅니다.

2. 리샘플링  
   `resample.py`로 `Result/` 폴더 내 오디오들을 불러와 최적 샘플링 주파수로 변환합니다.

3. 메타정보 생성  
   `information.py`로 리샘플링된 파일들의 메타데이터(경로, 라벨, 길이, 샘플링 레이트)를 CSV로 정리합니다.

4. 통계 확인 및 저장  
   `summerize.py`로 CSV를 분석해 라벨별 길이 분포를 확인하고, 결과를 파일로 저장합니다.

---

## 설치 및 환경 준비

Python 3.x

가상환경(venv)에서 작업하는 것을 권장합니다.

### 가상환경 생성 및 활성화

```bash
python -m venv venv```
macOS / Linux 활성화
```source venv/bin/activate```
Windows (PowerShell) 활성화
```.\venv\Scripts\activate```
필수 패키지 설치
```pip install -r requirements.txt```


requirements.txt에는 soundfile, numpy, scipy, tqdm, pandas 등이 포함되어 있습니다.

    시스템에 yt-dlp와 ffmpeg 설치 필수 (유튜브 다운로드 및 오디오 편집 도구)

    프로젝트 루트에 ontology.json과 data.txt 파일이 있어야 정상 작동합니다.

