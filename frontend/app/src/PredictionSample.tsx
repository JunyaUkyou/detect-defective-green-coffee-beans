interface Props {
  src: string;
  runPrediction: (src: string) => Promise<void>;
}

const PredictionSample: React.FC<Props> = ({ src, runPrediction }) => {
  // 推論中フラグ、推論結果画像URL

  return (
    <>
      <div className="upload-left">
        <img src={src} alt="Uploaded" className="ai-image" />
        <button onClick={() => runPrediction(src)}>推論する</button>
      </div>
    </>
  );
};
export default PredictionSample;
