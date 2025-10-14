import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  route("login", "routes/login.tsx"),
  route("gympro", "routes/workouts.tsx"),
] satisfies RouteConfig;
