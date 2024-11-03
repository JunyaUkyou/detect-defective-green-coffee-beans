const TopContent = () => {
  return (
    <>
      <div className="top-container">
        <div className="top-wrapper">
          <p className="top-text">
            コーヒー生豆の<span className="emphasis">欠点豆</span>
            を検出します
          </p>
          <div className="top-images">
            <img src="/public/images/4307_color.png" className="parson-image" />
            <img
              src="/public/images/1421_color.png"
              className="coffee-cap-image"
            />
            <img src="/public/images/4304_color.png" className="parson-image" />
          </div>
        </div>
      </div>
    </>
  );
};

export default TopContent;
