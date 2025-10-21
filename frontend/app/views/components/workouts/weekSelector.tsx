import { useState, useLayoutEffect } from "react";

import { WeekSelectorButton } from "~/views/components/workouts/selectorButton";

export function WeekSelector(props: { weekHandler: (event: number) => void }) {
  const [selected, setSelected] = useState<HTMLButtonElement>();

  useLayoutEffect(() => {
    const element = document.querySelector("#first-week");
    if (element) {
      element.setAttribute("data-active", "true");
      setSelected(element as HTMLButtonElement);
    }
  }, []);

  const activeHandler = (event: React.MouseEvent<HTMLButtonElement>) => {
    selected?.removeAttribute("data-active");
    event.currentTarget.setAttribute("data-active", "true");

    const weekNumber = parseInt(
      event.currentTarget.innerText.replace("Week ", "")
    );

    props.weekHandler(weekNumber);
    setSelected(event.currentTarget);
  };

  return (
    <div className="border-1 border-solid border-yellow-400/50 ml-[35px] mr-[35px] mt-[35px] rounded-md hidden sm:flex">
      <WeekSelectorButton
        weekOfPlan={1}
        activeHandler={activeHandler}
        id="first-week"
      />
      <WeekSelectorButton weekOfPlan={2} activeHandler={activeHandler} />
      <WeekSelectorButton weekOfPlan={3} activeHandler={activeHandler} />
      <WeekSelectorButton weekOfPlan={4} activeHandler={activeHandler} />
      <WeekSelectorButton weekOfPlan={5} activeHandler={activeHandler} />
      <WeekSelectorButton weekOfPlan={6} activeHandler={activeHandler} />
      <WeekSelectorButton weekOfPlan={7} activeHandler={activeHandler} />
      <WeekSelectorButton weekOfPlan={8} activeHandler={activeHandler} />
    </div>
  );
}
