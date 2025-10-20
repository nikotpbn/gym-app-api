interface Workout {
  id: number;
  exercise: { name: string; image: string | null };
  sets: number;
  reps: number;
  instructions: string;
  notes: string;
}

interface WorkoutContainerProps {
  day_of_week: string;
  workouts: Workout[];
}

export function WorkoutContainer(props: WorkoutContainerProps) {
  return (
    <>
      <div className="flex flex-col flex-nowrap flex-grow text-center border-solid border-2 border-yellow-400/50 rounded-md p-[20px] m-[10px]">
        <div className="relative">
          <svg
            className="absolute right-0 max-w-[35px] max-h-[35px] rotate-315"
            xmlns="http://www.w3.org/2000/svg"
            width="147"
            height="164"
            viewBox="0 0 147 164"
            fill="none"
          >
            <path
              d="M8 82H139M139 82L65 8M139 82L65 156"
              stroke="#FFD200"
              stroke-width="15"
              stroke-linecap="round"
              stroke-linejoin="round"
            ></path>
          </svg>
        </div>

        <div className="mt-[10px] mb-[10px]">{props.day_of_week}</div>
        <div className="mb-[15px]">Add muscle group</div>
        <ul>
          {props.workouts.map((workout, index) => (
            <li key={workout.id}>
              <div className="flex justify-between mt-[7px] mb-[7px]">
                <span className="flex text-yellow-400 max-w-[70%]">
                  {index + 1}.&nbsp;&nbsp;
                  <span className="flex text-white text-left">
                    {workout.exercise.name}
                    {workout.instructions}
                    <br />
                    {workout.notes}
                  </span>
                </span>
                <span className="text-yellow-400">
                  {workout.sets}x{workout.reps}
                </span>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}
