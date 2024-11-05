import React, { useState, useEffect } from 'react';
import PredictionDescription from './PredictionDescription';
import ErrorMessage from './ErrorMessage';
import PredictionTarget from './PredictionTarget';
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
  const [predictionError, setPredictionError] = useState<string>(''); // プレビュー画像のURL

  // 推論中フラグ、推論結果画像URL、推論実施関数
  const { isPredicting, predictionImageUrl, runPrediction } = PredictImage();

  useEffect(() => {
    if (src) {
      setPreviewUrl(src);
    }
  }, []);

  // 推論実施関数
  const onClickSubmit = async () => {
    try {
      setPredictionError('');
      await runPrediction(previewUrl);
    } catch (e: unknown) {
      if (e instanceof Error) {
        setPredictionError(e.message);
      } else {
        setPredictionError('例外発生');
      }
    }
  };

  const onChangeFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPredictionError('');
    const files = e.target.files;
    if (files && files[0]) {
      const selectedFile = files[0];
      console.log({ selectedFile });
      const type = selectedFile.type.split('/');
      console.log({ type });
      if (type[0] !== 'image') {
        setPredictionError('画像ファイルをアップロードしてください');
        return;
      }
      setFile(selectedFile);
      const objectUrl = URL.createObjectURL(selectedFile); // プレビュー用のURLを生成
      setPreviewUrl(objectUrl);
    }
  };

  const fileUpload = () => {
    const uploadElement = document.getElementById('file-upload-element');
    uploadElement!.click();
  };

  const fileDelete = () => {
    setPreviewUrl('');
  };

  return (
    <>
      <div className="upload-image">
        {/* 推論の概要 */}
        <PredictionDescription
          imageNumber={imageNumber}
          description={description}
        />
        {/* エラーメッセージ */}
        <ErrorMessage message={predictionError} />

        <div className="upload-result">
          {/* 推論対象画像 */}
          <PredictionTarget
            onClickSubmit={onClickSubmit}
            onChangeFile={onChangeFile}
            fileUpload={fileUpload}
            fileDelete={fileDelete}
            src={src}
            previewUrl={previewUrl}
          />

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
