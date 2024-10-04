import React, { useState } from 'react';

interface UploadImageProps {
  src: string;
  description: string;
  imageNumber: number;
}

const UploadImage: React.FC<UploadImageProps> = ({
  src,
  description,
  imageNumber,
}) => {
  const getFileName = (path: string) =>
    path.substring(path.lastIndexOf('/') + 1);

  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const paddedImageNumber = String(imageNumber).padStart(2, '0');

  const onClickSubmit = async () => {
    setIsLoading(true);
    // 画像を src からフェッチして Blob に変換
    const response = await fetch(src);
    const blob = await response.blob();

    // Blob から File オブジェクトを作成
    const fileName = getFileName(src);
    const file = new File([blob], fileName, { type: blob.type });

    const formData = new FormData();
    formData.append('file', file);

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

  return (
    <>
      <div className="upload-image">
        <div className="description">
          <h3 className="heading" data-number={paddedImageNumber}>
            <span>{description}</span>
          </h3>
        </div>
        <div className="upload-result">
          <div className="upload-left">
            <img src={src} alt="Uploaded" className="ai-image" />
            <button onClick={onClickSubmit}>推論する</button>
          </div>

          <div className="upload-right">
            {isLoading ? (
              <img
                src="/public/images/loading.gif"
                className="upload-loading ai-image"
              />
            ) : (
              <img
                src={imageUrl ? imageUrl : '/public/images/no-image.png'}
                className={`ai-image ${imageUrl ? 'downloaded' : 'no-image'}`}
                alt="Downloaded"
              />
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default UploadImage;
