import React from 'react';

interface PredictionTargetEmptyProps {
  fileInputRef: React.RefObject<HTMLInputElement>;
  onChangeFile: (e: React.ChangeEvent<HTMLInputElement>) => void;
  fileUpload: () => void;
}

const PredictionTargetEmpty: React.FC<PredictionTargetEmptyProps> = ({
  fileInputRef,
  onChangeFile,
  fileUpload,
}) => {
  return (
    <>
      {/* 推論対象のプレビュー画像が無い場合、ファイルアップロードを表示 */}
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
    </>
  );
};

export default PredictionTargetEmpty;
