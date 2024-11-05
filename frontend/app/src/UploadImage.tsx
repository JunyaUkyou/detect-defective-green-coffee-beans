import React, { useState, useEffect } from 'react';
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
  const [ApiError, setApiError] = useState<string>(''); // プレビュー画像のURL

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
    try {
      setApiError('');
      await runPrediction(previewUrl);
    } catch (e: unknown) {
      if (e instanceof Error) {
        setApiError(e.message);
      } else {
        setApiError('例外発生');
      }
    }
  };

  const onChangeFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    setApiError('');
    const files = e.target.files;
    if (files && files[0]) {
      const selectedFile = files[0];
      console.log({ selectedFile });
      const type = selectedFile.type.split('/');
      console.log({ type });
      if (type[0] !== 'image') {
        setApiError('画像ファイルをアップロードしてください');
        return;
      }
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
        {ApiError !== '' && (
          <div className="api-error">
            <p className="api-error-text">{ApiError}</p>
          </div>
        )}
        <div className="upload-result">
          {previewUrl === '' ? (
            <div className="upload-left">
              <label className="upload-label">
                <img
                  src="/public/images/upload.png"
                  alt="Uploaded"
                  className="ai-image"
                />
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
