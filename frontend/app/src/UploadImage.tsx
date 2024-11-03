import React, { useState, useEffect } from 'react';
import FreeUploadImage from './FreeUploadImage';
import PredictionResult from './PredictionResult';
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
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>(''); // プレビュー画像のURL

  // 推論中フラグ、推論結果画像URL、推論実施関数
  const { isPredicting, predictionImageUrl, runPrediction } = PredictImage();
  // 画像No
  const paddedImageNumber = String(imageNumber).padStart(2, '0');

  useEffect(() => {
    if (src) {
      setPreviewUrl(src);
      console.log('Hello world!', imageNumber);
    }
  }, []);

  // 推論実施関数
  const onClickSubmit = async () => {
    runPrediction(previewUrl);
  };

  const onChangeFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      const selectedFile = files[0];
      setFile(selectedFile);
      const objectUrl = URL.createObjectURL(selectedFile); // プレビュー用のURLを生成
      setPreviewUrl(objectUrl);
    }
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
          {previewUrl === '' ? (
            <div className="upload-left">
              <label className="upload-label">
                <input
                  name="file"
                  type="file"
                  className="image-upload"
                  accept="image/*"
                  onChange={onChangeFile}
                />
              </label>
            </div>
          ) : (
            <div className="upload-left">
              <img src={previewUrl} alt="Uploaded" className="ai-image" />
              <div className="run-prediction">
                <button
                  className="run-prediction-button"
                  onClick={onClickSubmit}
                >
                  推論する
                </button>
              </div>
            </div>
          )}
          {/* 推論結果 */}
          <PredictionResult
            isPredicting={isPredicting}
            predictionImageUrl={predictionImageUrl}
          />
        </div>
      </div>
    </>
  );
};

export default UploadImage;
