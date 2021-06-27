import React from "react";
import LastUse from "./LastUse";
import "../style/LastUses.css";

const LastUses = ({ uses }) => {
  return (
    <div className="last-30-use">
      {uses.map((use) => (
        <LastUse key={use.id} use={use} />
      ))}
    </div>
  );
};

export default LastUses;
