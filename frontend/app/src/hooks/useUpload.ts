// hooks/useUpload.ts
import { useState } from 'react';

export const useUpload = () => {
  // 画像URL
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  // ローディングフラグ
  const [isLoading, setIsLoading] = useState(false);

  // 画像アップロード関数
  const uploadFile = async (src: string) => {
    // ローディング表示
    setIsLoading(true);

    // 画像を src からフェッチして Blob に変換
    const response = await fetch(src);
    const blob = await response.blob();

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
    fetch('http://localhost:8000/ssd', {
      method: 'POST',
      body: formData, // ファイルを含めたFormDataを送信
    })
      .then((response) => response.blob()) // Blob 形式で画像を取得
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        setIsLoading(false);
        console.log({ url });
        setImageUrl(url); // 画像を表示するためにURLを生成
      })
      .catch((error) => {
        console.error('リクエストエラー:', error);
        setIsLoading(false);
      });
  };

  return { isLoading, imageUrl, uploadFile };
};
