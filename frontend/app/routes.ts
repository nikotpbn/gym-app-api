import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  route("login", "routes/login.tsx"),
  route("subscriptions", "routes/subscriptions.tsx"),
  route("workout/:workoutId", "routes/workout.tsx"),
] satisfies RouteConfig;
