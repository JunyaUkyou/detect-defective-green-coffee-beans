import './App.css';
import TopMenu from './TopMenu';
import UploadImage from './UploadImage';
import good1 from './assets/2EB011BF-CAA1-4470-9376-2E42A8B87CDE_1_105_c.jpeg';
import good2 from './assets/4A0389F9-050D-4FF2-9230-1B434ACB44DE_4_5005_c.jpeg';
import bad1 from './assets/bad1.jpg';
import bad2 from './assets/bad2.jpeg';

const App = () => {
  const images = [
    {
      src: good1,
      description: '良質豆 1個',
    },
    {
      src: good2,
      description: '良質豆 3個',
    },
    {
      src: bad1,
      description: '欠点豆 1個',
    },
    {
      src: bad2,
      description: '良質豆 1個 欠点豆 1個',
    },
  ];

  return (
    <>
      <div className="upload-container">
        {/* トップ画面 */}
        <TopMenu />
        {/* サンプル画面 */}
        {images.map((image, index) => (
          <UploadImage
            key={index}
            src={image.src}
            description={image.description}
            imageNumber={index + 1}
          />
        ))}
      </div>
    </>
  );
};

export default App;
