import React from 'react';

interface PredictionTargetPreviewProps {
  previewUrl: string;
  onClickSubmit: () => Promise<void>;
  fileDelete: () => void;
  src: string;
}

const PredictionTargetPreview: React.FC<PredictionTargetPreviewProps> = ({
  previewUrl,
  onClickSubmit,
  fileDelete,
  src,
}) => {
  return (
    <>
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
    </>
  );
};

export default PredictionTargetPreview;
