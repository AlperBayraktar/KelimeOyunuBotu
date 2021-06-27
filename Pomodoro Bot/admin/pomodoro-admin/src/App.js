import LastUses from "./components/LastUses";
import Texts from "./components/Texts";
import { useState } from "react";
import { useEffect } from "react";

function App() {
  const [texts, setTexts] = useState([]);
  const [uses, setUses] = useState([]);

  const dbURL = "http://localhost:5000/";
  useEffect(() => {
    const func = async () => {
      const request = await fetch(dbURL + "texts");
      setTexts(await request.json());
    };
    func();
  }, []);

  useEffect(() => {
    const func2 = async () => {
      const request = await fetch(dbURL + "last_30_use");
      setUses(await request.json());
    };
    func2();
  }, []);

  const saveChanges = async () => {
    const text1 = document.getElementsByClassName("help")[0].value;
    const text2 = document.getElementsByClassName("info")[0].value;

    const x = async (endpoint, body) => {
      var a = await fetch(dbURL + endpoint, {
        method: "PUT",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(body),
      });

      console.log(await a.json());
    };

    texts[0]["content"] = text1;
    texts[1]["content"] = text2;

    x("texts/1", texts[0]);
    x("texts/2", texts[1]);

    alert("Değişiklikler yapıldı.");
  };

  return (
    <div className="containers">
      <div className="container container-1">
        <h1 className="title">Son 30 Kullanım</h1>

        {uses.length > 1 ? (
          <LastUses uses={uses} />
        ) : (
          <h3>Son kullanım yok.</h3>
        )}
      </div>

      <div className="container container-2">
        <h1 className="title-2">Metinler</h1>
        <hr className="text-seperator" />
        <Texts texts={texts} />
        <button className="btn" onClick={saveChanges}>
          Değişiklikleri Kaydet
        </button>
      </div>
    </div>
  );
}

export default App;
