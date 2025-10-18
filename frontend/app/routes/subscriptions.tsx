import type { Route } from "./+types/subscriptions";
import { useContext, useEffect, useState } from "react";
import { Link } from "react-router";

import { AuthContext } from "~/context";

export function meta({}: Route.MetaArgs) {
  return [{ title: "Workout Plan" }];
}

export default function Subscriptions() {
  const auth = useContext(AuthContext);

  const [workouts, setWorkouts] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/program/", {
          headers: {
            Authorization: `Bearer ${auth.access}`,
          },
        });
        const data = await response.json();
        setWorkouts(data);
      } catch (error) {}
    };
    loadData();
  }, [auth]);

  return (
    <>
      {workouts.length > 0 && (
        <ul>
          {workouts.map((workout: any) => (
            <li key={workout.id}>
              <h2>{workout.name}</h2>
              <Link to={`/workout/${workout.id}`}>View Exercises</Link>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
