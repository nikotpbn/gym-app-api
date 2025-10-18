interface InputProps {
  label: string;
  placeholder: string;
  type: string;
  handler: Function;
}

export function Input(props: InputProps) {
  function onInputChange(e: React.ChangeEvent<HTMLInputElement>) {
    props.handler(e.target.value);
  }

  return (
    <label className="text-black text-xs w-[100%] font-100 opacity-60 antialiased">
      {props.label}
      <input
        className="w-full text-black text-sm border-1 border-gray-300 rounded-md mb-[4px] opacity-[.6] px-[10px] h-[42px] outline-hidden antialiased"
        type={props.type}
        placeholder={props.placeholder}
        onChange={onInputChange}
      />
    </label>
  );
}
