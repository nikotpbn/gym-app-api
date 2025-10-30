import { useState, useEffect } from "react";

interface InputProps {
  placeholder: string;
  type: string;
  changeHandler: Function;
  extraClasses?: string;
  name: string;
  id: string;
}

export function Input(props: InputProps) {
  const [inputValue, setInputValue] = useState<string>();

  useEffect(() => {
    const element = document.getElementById(props.id);
    const timer = setTimeout(() => {
      if (props.type === "email") {
        let regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

        if (inputValue != null && inputValue != "" && element) {
          if (!regex.test(inputValue)) {
            element.classList.add("border-red-500");
          } else {
            element.classList.remove("border-red-500");
          }
        }
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [inputValue]);

  function onInputChange(e: React.ChangeEvent<HTMLInputElement>) {
    setInputValue(e.target.value);
    props.changeHandler(e.target.value);
  }

  return (
    <input
      className={
        `${props.extraClasses}` +
        " w-full text-black text-sm border-1 border-black-300 rounded-md mb-[4px] opacity-[.6] px-[10px] h-[42px] outline-hidden antialiased"
      }
      id={props.id}
      name={props.name}
      type={props.type}
      placeholder={props.placeholder}
      onChange={onInputChange}
    />
  );
}
