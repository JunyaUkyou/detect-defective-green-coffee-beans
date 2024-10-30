import React, { useState } from 'react';
import { PredictImage } from './hooks/PredictImage';

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
  // ローディング表示フラグ、推論結果画像URL、推論実施関数
  const { isLoading, predictionImageUrl, runPrediction } = PredictImage();

  // 画像No
  const paddedImageNumber = String(imageNumber).padStart(2, '0');

  // 推論実施関数
  const onClickSubmit = async () => {
    runPrediction(src);
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
                src={
                  predictionImageUrl
                    ? predictionImageUrl
                    : '/public/images/no-image.png'
                }
                className={`ai-image ${
                  predictionImageUrl ? 'downloaded' : 'no-image'
                }`}
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
