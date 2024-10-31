import { PredictImage } from './hooks/PredictImage';

interface Props {
  isPredicting: boolean;
  predictionImageUrl: string | null;
}

const PredictionResult: React.FC<Props> = ({
  isPredicting,
  predictionImageUrl,
}) => {
  // 推論中フラグ、推論結果画像URL

  return (
    <>
      <div className="upload-right">
        {/* 推論中はローディング表示 */}
        {isPredicting ? (
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
    </>
  );
};
export default PredictionResult;
