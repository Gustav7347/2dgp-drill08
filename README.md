# Drill #8 — 애니메이션 뷰어

## 실행 (Windows / Python 3.10 이상)

압축을 풀고 `Drill08` 폴더에서 터미널을 연다.

```powershell
py -m pip install -r LEC08/requirements.txt
py LEC08/animation_viewer.py
```

설치 후에는 `LEC08/run.bat`을 더블 클릭해도 된다. 종료는 ESC 또는 창 닫기.
인터넷은 최초 패키지 설치에만 필요하며, 실행에 필요한 스프라이트는 포함되어 있다.
Linux/macOS에서는 `py` 대신 `python3`를 사용한다.

## 과제 요구사항 대응

| 요구사항 | 구현 |
|---|---|
| Sprite Sheet 사용 | CC0 Sora 스프라이트를 가변 크기 atlas로 재배치 |
| 애니메이션 4종 이상 | Idle(대기), Run(달리기), Melee(근접 공격), Ranged(원거리 공격) |
| 충분한 확대 | 720×600 화면에 7배 확대, 실제 이미지 높이 364~385px |
| 파일 위치 | `LEC08/animation_viewer.py` |
| 화면 중앙 재생 | 원본 피벗을 기준으로 중앙 고정, 이동 애니메이션도 제자리 재생 |
| 5회 재생 → 1초 정지 | 마지막 프레임을 1초 유지한 뒤 다음 동작 |
| 순서대로 무한 반복 | Idle → Run → Melee → Ranged → Idle |
| 가변 프레임 크기 (+2) | 투명 여백을 제거한 서로 다른 w/h와 피벗을 JSON에 저장 |
| 가변 프레임 개수 (+2) | 8 / 4 / 5 / 4개, 각 애니메이션의 실제 길이로 재생 |
| 커밋 20개 이상 | 실제 단계별 변경을 담은 Git 저장소와 복원용 bundle 제공 |

※ 확대는 화면 **높이** 기준이다. 캐릭터 비율을 유지한다.
※ 추가점수 최종 인정 여부는 담당 교원의 평가에 따른다.

## 제출 시 기능 설명 (붙여넣기용)

Pico2D를 사용하여 대기, 달리기, 근접 공격, 원거리 공격의 4가지 애니메이션을 구현했습니다.
캐릭터를 화면 중앙에서 7배 확대하여 표시하고, 각 애니메이션을 5회 재생한 뒤 마지막
프레임에서 1초간 멈추고 다음 애니메이션으로 넘어가도록 했습니다.
마지막 애니메이션 이후 처음으로 돌아가 무한 반복합니다.
투명 여백을 잘라 프레임 크기가 서로 다른 복잡한 Sprite Sheet를 만들었으며,
프레임별 좌표·크기·피벗을 사용하여 캐릭터 기준 위치를 유지했습니다.
애니메이션별 프레임 수가 8, 4, 5, 4개로 달라도 개별 데이터에 따라 재생되도록 했습니다.
AI(Codex)를 활용하여 구현하고, 원본 스프라이트는 Danilo Mattos의 CC0 에셋을 사용했습니다.

## 파일 안내

- `LEC08/animation_viewer.py`: 재생 상태, 클리핑, 확대, Pico2D 메인 루프.
- `LEC08/assets/atlas.png`, `atlas.json`: 실제 재생에 사용하는 스프라이트와 좌표.
- `LEC08/assets/source/`: 원본 이미지 4개.
- `LEC08/assets/CREDITS.md`: 출처와 라이선스.
- `LEC08/tools/rebuild_atlas.py`: 원본을 투명 여백 제거 후 재배치하는 도구.
- `LEC08/tests/test_viewer.py`: 반복/정지/순환/좌표 검증.
- `LEC08/docs/preview.gif`: 실제 Pico2D 렌더러로 생성한 한 바퀴 미리보기.
- `.git/`: 실제 Git 저장소. 압축을 풀 때 포함하여 유지할 것.

## 검증

```powershell
py -m unittest discover -s LEC08/tests -v
git log --oneline --reverse
git rev-list --count HEAD
```

원본 재배치가 필요할 때만 Pillow를 추가 설치한다. 일반 실행에는 필요 없다.

```powershell
py -m pip install Pillow
py LEC08/tools/rebuild_atlas.py
```

## Git 이력을 유지하는 방법

이 결과물은 기존 저장소가 제공되지 않은 상태에서 생성한 **별도 저장소**이다.
커밋 작성자는 `Codex <codex@local.invalid>`이며 사용자 작성 이력으로 가장하지 않았다.
단순히 `LEC08`만 기존 저장소에 복사하면 이 저장소의 커밋 이력은 따라가지 않는다.
20개 이상의 이력이 채점에 필요한 경우 제공된 저장소 자체를 사용하거나 이력을 병합해야 한다.

압축에 함께 제공된 bundle로 저장소를 복원할 수 있다.

```powershell
git clone Drill08-history.bundle Drill08-restored
```

기존 수업 저장소에 병합할 경우 먼저 기존 파일을 확인하고 작업 내용을 커밋 또는
백업한 후 진행한다. 여기서는 기존 저장소 병합, 원격 GitHub push, LMS 제출은 하지 않았다.
원격 주소와 기존 저장소가 주어지지 않았기 때문이다.
