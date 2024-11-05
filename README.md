# detect-defective-green-coffee-beans

<div id="top"></div>

![localhost_5173_](https://github.com/user-attachments/assets/4b0e66cc-2794-4b73-9b63-c568f7fbc921)

## 目次

1. [プロジェクトについて](#プロジェクトについて)
2. [環境構築](#環境構築)
3. [アプリケーションの操作方法](#アプリケーションの操作方法)
4. [ディレクトリ構成](#ディレクトリ構成)
5. [トラブルシューティング](#トラブルシューティング)

## 1. プロジェクトについて

### SSD を用いたコーヒー生豆欠点豆の検出

- コーヒー生豆の画像を使用し、欠点豆の検出を行う
- コーヒー豆は表と裏で形状や色が異なるため、表裏の画像を用意する
- 実装時点（2024.11）では色が不正のコーヒー豆が集まらなかった為、形状が不正の欠点豆を検出する

### 検出するコーヒー豆

- 良質豆（表）
- 良質豆（裏）
- 欠点豆 形が不正（表）
- 欠点豆 形が不正（表）

### モデル

- torchvision.models.detection.ssd300_vgg16

### 今後の実装

- 欠点豆 色不正の検出（色不正のコーヒー豆が集まれば実装）
- ファインチューニング等、精度向上（現状は転移学習で一定の精度が出たため、転移学習としてる。）

## 2. 環境構築

detect-defective-green-coffee-beans 直下（docker-compose.yml がある所）で以下コマンドを実行する

### 初回起動

```
docker compose build

docker compose run --entrypoint "poetry install --no-root" backend

docker compose run --rm frontend npm install

docker compose up -d

↓不要
docker compose run \
 --entrypoint "poetry init \
 --name api \
 --dependency fastapi \
 --dependency uvicorn[standard]" \
 api
```

### 2 回目以降起動

```
docker compose up -d
```

### アプリケーション終了

```
docker compose down
```

## 3. アプリケーションの操作方法

### 画面 URL

```
http://localhost:5173/
```

### API doc

```
http://localhost:8000/docs
```

## 4. ディレクトリ構成

```
.
├── README.md
├── backend                       # バックエンド
│   ├── .env
│   ├── .gitignore
│   ├── .venv
│   ├── Dockerfile
│   ├── api
│   │   ├── __init__.py
│   │   ├── events
│   │   │   └── startup.py        # startupイベント処理
│   │   ├── main.py               # ルーティング定義
│   │   ├── routers
│   │   │   └── ssd.py            # SSD系のAPI処理
│   │   └── validate.py           # バリデーションチェック処理
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py
│   ├── fonts
│   │   └── NotoSansCJKjp-Bold.otf
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── services
│   │   └── ssd                   # SSD推論処理
│   │       ├── SSD_weights.pth   # 学習済みモデルの重みファイル
│   │       ├── __init__.py
│   │       ├── constants.py      # 規定値
│   │       ├── net.py            # ネットワークモデル
│   │       └── ssd_predictor.py  # 推論処理
│   └── tests
│       ├── __init__.py
│       └── test_main.py
├── docker-compose.yml
└── frontend                      # フロントエンド
    ├── Dockerfile
    └── app
        ├── .gitignore
        ├── eslint.config.js
        ├── index.html
        ├── package-lock.json
        ├── package.json
        ├── public
        │   ├── images
        │   │   ├── 1421_color.png
        │   │   ├── 4304_color.png
        │   │   ├── 4307_color.png
        │   │   ├── loading.gif
        │   │   ├── no-image.png
        │   │   └── upload.png
        │   └── vite.svg
        ├── src                      # 画面描画処理（フォルダ分けしたい、、）
        │   ├── App.css
        │   ├── App.tsx
        │   ├── ErrorMessage.tsx
        │   ├── FreeUploadImage.tsx
        │   ├── HowToUseContent.tsx
        │   ├── PredictionDescription.tsx
        │   ├── PredictionResult.tsx
        │   ├── PredictionSample.tsx
        │   ├── PredictionTargetEmpty.tsx
        │   ├── PredictionTargetPreview.tsx
        │   ├── TopContent.tsx
        │   ├── UploadImage.tsx
        │   ├── assets
        │   │   ├── 2EB011BF-CAA1-4470-9376-2E42A8B87CDE_1_105_c.jpeg
        │   │   ├── 4A0389F9-050D-4FF2-9230-1B434ACB44DE_4_5005_c.jpeg
        │   │   ├── bad1.jpg
        │   │   ├── bad2.jpeg
        │   │   └── react.svg
        │   ├── hooks
        │   │   └── PredictImage.ts
        │   ├── index.css
        │   ├── main.tsx
        │   └── vite-env.d.ts
        ├── tsconfig.app.json
        ├── tsconfig.json
        ├── tsconfig.node.json
        └── vite.config.ts

```

## 5. トラブルシューティング

- mac の場合、Docker の設定で「Use Virtualization framework」にチェックがついていると起動しない場合があります<a href="https://qiita.com/takumisenaha00/items/62f0a8f184240c2b3aca">参考</a>
