import React, { useState } from 'react';

const App = () => {
  const [file, setFile] = useState<File | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  const onChangeFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log({ e });
    const files = e.target.files;
    if (files && files[0]) {
      setFile(files[0]);
    }
  };

  const onClickSubmit = () => {
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
      <div>
        <input
          name="file"
          type="file"
          accept="image/*"
          onChange={onChangeFile}
        />
        <input
          type="button"
          disabled={!file}
          value="送信"
          onClick={onClickSubmit}
        />
      </div>
      {imageUrl && <img src={imageUrl} alt="Downloaded" />}
    </>
  );
};

export default App;
