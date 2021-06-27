import React from "react";
import TextEdit from "./TextEdit";

const Texts = ({ texts }) => {
  return (
    <div className="texts">
      {texts.map((text) => (
        <TextEdit
          key={text.id}
          title={text.title}
          content={text.content}
          tagID={text.tagID}
        />
      ))}
    </div>
  );
};

export default Texts;
