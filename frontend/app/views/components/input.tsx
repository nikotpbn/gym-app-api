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
    <label className="text-black font-100">
      {props.label}
      <input
        className="w-full text-black border-1 border-gray-300 rounded-md"
        type={props.type}
        placeholder={props.placeholder}
        onChange={emailHandler}
      />
    </label>
  );
}
