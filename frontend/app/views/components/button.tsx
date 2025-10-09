export function Button(props: { children: string; handler: React.MouseEventHandler }) {
  return (
    <button
      onClick={props.handler}
      type="button"
      className="bg-black text-xs rounded-[30px] py-[10px] w-[40%] cursor-pointer"
    >
      {props.children}
    </button>
  );
}
