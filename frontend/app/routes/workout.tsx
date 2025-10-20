import type { Route } from "./+types/workout";
import { useContext, useEffect, useState } from "react";

import { AuthContext } from "~/context";
import { useParams } from "react-router";

import { WorkoutContainer } from "~/views/components/workouts/workoutContainer";

export function meta({}: Route.MetaArgs) {
  return [{ title: "My Subscriptions" }];
}

export default function Workout() {
  const auth = useContext(AuthContext);
  let params = useParams();
  const [weeklyWorkout, setWeeklyWorkout] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/v1/program/${params.workoutId}/exercise/list/1/`,
          {
            headers: {
              Authorization: `Bearer ${auth.access}`,
            },
          }
        );
        const data = await response.json();
        setWeeklyWorkout(data);
        console.log(data);
      } catch (error) {}
    };
    loadData();
  }, [auth]);

  return (
    <>
      {weeklyWorkout.length > 0 && (
        <div className="flex flex-row flex-wrap w-full justify-betweem p-[25px]">
          {weeklyWorkout.map((dailyWorkout: any) => (
            <WorkoutContainer
              key={dailyWorkout.day_of_week}
              day_of_week={dailyWorkout.day_of_week}
              workouts={dailyWorkout.exercises}
            ></WorkoutContainer>
          ))}
        </div>
      )}
    </>
  );
}
