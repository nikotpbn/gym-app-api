export function Link(props: { children: string; link: string }) {
  return (
    <a className="text-black text-xs opacity-[50%]" href={props.link}>
      {props.children}
    </a>
  );
}
