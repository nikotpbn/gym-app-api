export function Button(props: { children: string }) {
  return (
    <button className="bg-black text-xs rounded-[30px] py-[10px] w-[40%]">
      {props.children}
    </button>
  );
}
