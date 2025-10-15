import type { Route } from "./+types/workouts";
import { useContext } from "react";
import { Navigate } from "react-router";

import { AuthContext } from "~/context";

export function meta({}: Route.MetaArgs) {
  return [{ title: "Workouts" }];
}

export default function Workouts() {
  const auth = useContext(AuthContext);

  if (auth.isLoggedIn == false) {
    return <Navigate replace to="/login"></Navigate>;
  }
  return (
    <>
      <h2>Workouts after login should be protected</h2>
    </>
  );
}
