export function WeekSelectorButton(props: {
  weekOfPlan: number;
  activeHandler: (event: React.MouseEvent<HTMLButtonElement>) => void;
  id?: string;
}) {
  return (
    <button
      id={props.id}
      type="button"
      onClick={props.activeHandler}
      className="w-[12.5%] min-h-[30px] text-xs data-[active=true]:bg-yellow-500 data-[active=true]:text-black"
    >
      Week {props.weekOfPlan}
    </button>
  );
}
