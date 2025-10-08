import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";
import { Login } from "../views/login/login";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "MegaTitle" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  return <Login />;
}
