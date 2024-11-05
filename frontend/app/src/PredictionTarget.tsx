import React from 'react';

interface PredictionTargetProps {
  fileInputRef: React.RefObject<HTMLInputElement>;
  previewUrl: string;
  onChangeFile: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onClickSubmit: () => Promise<void>;
  fileUpload: () => void;
  fileDelete: () => void;
  src: string;
}

const PredictionTarget: React.FC<PredictionTargetProps> = ({
  fileInputRef,
  previewUrl,
  onChangeFile,
  onClickSubmit,
  fileUpload,
  fileDelete,
  src,
}) => {
  return (
    <>
      {/* 推論対象のプレビュー画像が無い場合、ファイルアップロードを表示 */}
      {previewUrl === '' ? (
        <div className="upload-left">
          <label className="upload-label">
            <img
              src="/public/images/upload.png"
              alt="Uploaded"
              className="ai-image"
            />
          </label>
          <div className="run-prediction">
            <label>
              <input
                ref={fileInputRef}
                id="file-upload-element"
                name="file"
                type="file"
                className="image-upload"
                accept="image/*"
                onChange={onChangeFile}
                style={{ display: 'none' }}
              />
              <button className="run-prediction-button" onClick={fileUpload}>
                ファイルアップロード
              </button>
            </label>
          </div>
        </div>
      ) : (
        <div className="upload-left">
          <img src={previewUrl} alt="Uploaded" className="ai-image" />
          <div className="run-prediction">
            <button className="run-prediction-button" onClick={onClickSubmit}>
              推論する
            </button>
            {src === '' && (
              <button className="run-prediction-button" onClick={fileDelete}>
                ファイル削除
              </button>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default PredictionTarget;
