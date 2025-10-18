interface WorkoutContainerProps {
  id: number;
  week_of_plan: number;
  day_of_week: string;
  environment: string;
  instruction: string;
  notes: string;
}

export function WorkoutContainer(props: WorkoutContainerProps) {
  return (
    <div>
        {props.day_of_week}
    </div>
  );
}
