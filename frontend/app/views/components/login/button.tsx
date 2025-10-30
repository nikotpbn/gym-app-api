export function Button(props: { children: string; handler: React.MouseEventHandler }) {
  return (
    <button
      onClick={props.handler}
      type="button"
      className="bg-black text-xs rounded-sm py-[10px] w-[100%] cursor-pointer"
    >
      {props.children}
    </button>
  );
}
