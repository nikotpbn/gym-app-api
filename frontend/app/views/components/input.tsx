import { useState } from "react";

interface InputProps {
  label: string;
  placeholder: string;
  type: string;
}

export function Input(props: InputProps) {
  const [email, setEmail] = useState("");

  function emailHandler(e: React.ChangeEvent<HTMLInputElement>) {
    console.log(e.target.value);
    setEmail(e.target.value);
  }

  return (
    <label className="text-black text-xs w-[100%] font-100 opacity-60 antialiased">
      {props.label}
      <input
        className="w-full text-black text-sm border-1 border-gray-300 rounded-md mb-[4px] opacity-[.6] px-[10px] h-[42px] outline-hidden antialiased"
        type={props.type}
        placeholder={props.placeholder}
        onChange={emailHandler}
      />
    </label>
  );
}
