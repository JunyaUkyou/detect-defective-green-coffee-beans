import React from 'react';

interface PredictionDescriptionProps {
  imageNumber: number;
  description: string;
}

const PredictionDescription: React.FC<PredictionDescriptionProps> = ({
  imageNumber,
  description,
}) => {
  // 画像No 0埋めする
  const paddedImageNumber = String(imageNumber).padStart(2, '0');

  return (
    <div className="description">
      <h3 className="heading" data-number={paddedImageNumber}>
        <span>{description}</span>
      </h3>
    </div>
  );
};

export default PredictionDescription;
