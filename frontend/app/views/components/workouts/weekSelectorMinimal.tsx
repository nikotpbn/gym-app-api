export function WeekSelectorMinimal(props: {
  weekHandler: (event: number) => void;
}) {
  const selectionHandler = (event: React.ChangeEvent<HTMLSelectElement>) => {
    let weekNumber = parseInt(event.currentTarget.value);
    props.weekHandler(weekNumber);
  };

  return (
    <div className="flex justfy-center align-center mr-[35px] ml-[35px] mt-[30px] sm:hidden">
      <select
        name=""
        id=""
        className="bg-yellow-500 text-black font-semibold rounded-md min-h-[35px] w-full p-[10px]"
        onChange={selectionHandler}
      >
        <option value="1">Week 1</option>
        <option value="2">Week 2</option>
        <option value="3">Week 3</option>
        <option value="4">Week 4</option>
        <option value="5">Week 5</option>
        <option value="6">Week 6</option>
        <option value="7">Week 7</option>
        <option value="8">Week 8</option>
      </select>
    </div>
  );
}
