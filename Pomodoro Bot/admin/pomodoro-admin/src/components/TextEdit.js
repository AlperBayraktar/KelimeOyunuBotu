import React from "react";
import "../style/TextEdit.css";

const TextEdit = ({ title, content, tagID }) => {
  return (
    <div className="text-edit">
      <h2 className="text-edit-title">{title}</h2>
      <textarea
        className="text-edit-area"
        defaultValue={content}
        className={tagID}
      />
      <hr className="text-seperator" />
    </div>
  );
};

export default TextEdit;
