const HowToUseContent = () => {
  return (
    <>
      <div className="how-to-use-container">
        <div className="description">
          <h3 className="heading" data-number="??">
            <span>使い方</span>
          </h3>
        </div>
        <ul className="how-to-use-list">
          <li className="how-to-use-list-item">
            サンプル画像用紙しています。「推論する」で右側に推論結果を表示します
          </li>
          <li className="how-to-use-list-item">
            お持ちの画像をアップロードできます。
          </li>
          <li className="how-to-use-list-item">
            アップロードできるのは高さと幅が等しいサイズが1MBの画像です。
          </li>
        </ul>
      </div>
    </>
  );
};
export default HowToUseContent;
