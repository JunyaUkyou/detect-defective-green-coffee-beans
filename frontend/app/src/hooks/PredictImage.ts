import { useState } from 'react';

export const PredictImage = () => {
  // 推論結果画像
  const [predictionImageUrl, setPredictionImageUrl] = useState<string | null>(
    null
  );
  // ローディングフラグ
  const [isPredicting, setIsPredicting] = useState(false);

  // 画像推論関数
  const runPrediction = async (src: string) => {
    // ローディング表示
    setIsPredicting(true);

    // 画像を src からフェッチして Blob に変換
    const imgResponse = await fetch(src);
    const blob = await imgResponse.blob();

    // 画像パスからファイル名を取得
    const getFileName = (path: string) =>
      path.substring(path.lastIndexOf('/') + 1);
    const fileName = getFileName(src);

    // BlobからFileオブジェクトを作成
    const file = new File([blob], fileName, { type: blob.type });

    // フォームにFileオブジェクト追加
    const formData = new FormData();
    formData.append('file', file);

    // SSD推論実施
    const apiResponse = await fetch('http://localhost:8000/ssd', {
      method: 'POST',
      body: formData, // ファイルを含めたFormDataを送信
    });

    setIsPredicting(false);
    if (!apiResponse.ok) {
      const errorData = await apiResponse.json();
      console.log({ errorData });
      throw new Error(errorData.detail);
    }

    const apiBlob = await apiResponse.blob();
    const url = URL.createObjectURL(apiBlob);

    console.log({ url });
    setPredictionImageUrl(url); // 画像を表示するためにURLを生成

    // .then((response) => {
    //   if (response.status !== 200) {
    //     const errorData = await response.json();
    //     console.log({ response });
    //     throw new Error('SSD推論エラー');
    //   }
    //   return response.blob();
    // }) // Blob 形式で画像を取得
    // .then((blob) => {
    //   const url = URL.createObjectURL(blob);
    //   setIsPredicting(false);
    //   console.log({ url });
    //   setPredictionImageUrl(url); // 画像を表示するためにURLを生成
    // })
    // .catch((error) => {
    //   console.error(error);
    //   setIsPredicting(false);
    //   throw new Error(error);
    // });
  };

  return { isPredicting, predictionImageUrl, runPrediction };
};
