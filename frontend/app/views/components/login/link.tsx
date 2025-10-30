export function Link(props: {
  children: string;
  link: string;
  tailwindTextColor: string;
  tailwindTextSize: string;
}) {
  return (
    <a
      className={`${props.tailwindTextColor} ${props.tailwindTextSize}`}
      href={props.link}
    >
      {props.children}
    </a>
  );
}
