# audioset
AudioSet Processing Pipeline
이 프로젝트는 AudioSet 데이터셋 내 특정 라벨에 해당하는 유튜브 오디오 클립을 다운로드, 트리밍, 리샘플링하고, 최종 정보를 CSV로 정리하며, 라벨별 오디오 길이 통계까지 제공하는 파이썬 스크립트 모음입니다.

파일 설명
1. sound.py
YouTube에서 AudioSet 클립을 다운로드하고 지정 구간으로 트리밍합니다.

ontology.json에서 라벨 이름과 ID를 불러와 data.txt의 라벨 ID 기반 클립 정보를 필터링합니다.

명령어 예시:

bash
복사
python sound.py --label "fire alarm" "explosion" --num 10 --exclude "speech"
다운로드한 전체 오디오는 full/, 트리밍된 클립은 Result/ 폴더에 저장됩니다.

2. resample.py
Result/ 폴더 내 WAV 파일을 읽어 최대 주파수를 추정한 후, 그에 맞게 샘플링 주파수를 조정하여 리샘플링합니다.

리샘플링 결과는 resample/ 폴더에 저장됩니다.

리샘플링 과정은 tqdm 진행 바를 통해 시각적으로 확인 가능.

3. information.py
resample/ 폴더 내 WAV 파일들을 스캔하여 각 파일의 절대 경로, 라벨명, 길이(초), 샘플링 레이트 정보를 추출합니다.

결과는 result_info.csv 파일로 저장됩니다.

4. summerize.py
information.py가 생성한 result_info.csv를 불러와 라벨별 오디오 길이 통계(개수, 평균, 분산, 최대, 최소)를 계산합니다.

전체 통계도 함께 포함되며, 결과는 콘솔 출력과 sum.csv 파일로 저장됩니다.

전체 워크플로우
sound.py 실행 → 특정 라벨 오디오 다운로드 및 구간별 트리밍

resample.py 실행 → Result/ 폴더 내 트리밍 오디오 리샘플링

information.py 실행 → resample/ 폴더 내 오디오 메타정보 CSV 생성

summerize.py 실행 → CSV 기반 라벨별 오디오 길이 통계 생성 및 저장

환경 및 의존성
Python 3.x

필요 라이브러리: soundfile, numpy, scipy, tqdm, pandas

외부 도구: yt-dlp, ffmpeg (시스템에 설치되어 있어야 함)

ontology.json 및 data.txt 파일이 스크립트 실행 경로에 있어야 함
