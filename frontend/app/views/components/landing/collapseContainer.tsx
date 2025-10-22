import { CollapseContainerButton } from "./collapseContainerButton";

export default function CollapseContainer(props: {
  id: number;
  title: string;
  content: string;
}) {
  const collapseHandler = (event: React.MouseEvent<HTMLButtonElement>) => {
    const elementId = event.currentTarget.dataset.collapsedId;
    const hiddenContainer = document.getElementById(`${elementId}`);
    if (hiddenContainer?.classList.contains("hidden")) {
      hiddenContainer.classList.remove("hidden");
    } else {
      hiddenContainer?.classList.add("hidden");
    }
  };

  return (
    <button
      type="button"
      className="flex flex-col basis-1/2 p-[15px] align-center"
      onClick={collapseHandler}
      data-collapsed-id={`collapsed-faq-${props.id}`}
    >
      <div className="flex flex-row justify-between">
        <span className="font-semibold">{props.title}</span>
        <CollapseContainerButton />
      </div>
      <div id={`collapsed-faq-${props.id}`} className="hidden">
        {props.content}
      </div>
    </button>
  );
}
