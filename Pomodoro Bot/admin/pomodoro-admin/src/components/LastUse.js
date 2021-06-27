import React from "react";
import "../style/LastUse.css";

const LastUse = ({ use }) => {
  return (
    <div className="last-use">
      <h3 title={use.userID}>{use.user}</h3>
      <h3 className="last-use-time">
        {use.date} - {use.time}
      </h3>
    </div>
  );
};

export default LastUse;
