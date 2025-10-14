import type { Route } from "./+types/workouts";
import { useContext } from "react";

import { AuthContext } from "~/context";

export function meta({}: Route.MetaArgs) {
  return [{ title: "Workouts" }];
}

export default function Workouts() {
  const auth = useContext(AuthContext);

  return (
    <>
      <h2>{auth.access}Workouts after login should be protected</h2>
    </>
  );
}
