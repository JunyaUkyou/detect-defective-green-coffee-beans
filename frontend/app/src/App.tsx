import React, { useState } from 'react';
import './App.css';

const App = () => {
  //const [file, setFile] = useState<File | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  const onChangeFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log({ e });
    const files = e.target.files;
    if (files && files[0]) {
      //setFile(files[0]);
      onClickSubmit(files[0]);
    }
  };

  const onClickSubmit = (file: File) => {
    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('http://localhost:8000/ssd', {
      method: 'POST',
      body: formData, // ファイルを含めたFormDataを送信
    })
      .then((response) => response.blob()) // Blob 形式で画像を取得
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        console.log({ url });
        setImageUrl(url); // 画像を表示するためにURLを生成
      })
      .catch((error) => {
        console.error('リクエストエラー:', error);
      });
  };

  return (
    <>
      <div className="upload-container">
        <div className="fileUpload">
          <p className="aaa">
            コーヒーの欠点豆の画像をアップロードしてください
            <br className="br"></br>
            （※画像は幅と高さを同じにしてください）
          </p>

          <label className="bbb" htmlFor="sample1">
            ファイルを選択
            <input
              type="file"
              id="sample1"
              accept="image/*"
              onChange={onChangeFile}
            />
          </label>
        </div>

        <div className="upload-result">
          <p>アップロード済み</p>
          {imageUrl && <img src={imageUrl} alt="Downloaded" />}
        </div>
      </div>
    </>
  );
};

export default App;
