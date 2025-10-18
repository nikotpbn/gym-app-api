import type { Route } from "./+types/workout";
import { useContext, useEffect, useState } from "react";

import { AuthContext } from "~/context";
import { useParams } from "react-router";

export function meta({}: Route.MetaArgs) {
  return [{ title: "My Subscriptions" }];
}

export default function Workout() {
  const auth = useContext(AuthContext);
  let params = useParams();
  const [programExercises, setProgramExercises] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/v1/program/${params.workoutId}/list_exercises/`,
          {
            headers: {
              Authorization: `Bearer ${auth.access}`,
            },
          }
        );
        const data = await response.json();
        console.log(data);
        setProgramExercises(data);
      } catch (error) {}
    };
    loadData();
  }, [auth]);

  return (
    <>
      {programExercises.length > 0 && (
        <ul>
          {programExercises.map((workout: any) => (
            <li key={workout.id}>
              <h2>{workout.name}</h2>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
