import { useState, useContext } from "react";
import type { Route } from "./+types/auth/login";

import { Input } from "~/views/components/login/input";
import { Button } from "~/views/components/login/button";
import { Link } from "~/views/components/login/link";

import { AuthContext } from "~/context";

import { useNavigate, Navigate } from "react-router";

export function meta({}: Route.MetaArgs) {
  return [{ title: "Login" }];
}

export default function Login() {
  let navigate = useNavigate();
  const auth = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function emailHandler(value: string) {
    setEmail(value);
  }

  function passwordHandler(value: string) {
    setPassword(value);
  }

  async function logIn() {
    try {
      const response = await fetch("http://localhost:8000/api/v1/token/", {
        method: "POST",
        body: JSON.stringify({ email, password }),
        headers: { "Content-Type": "application/json" },
      });

      if (response.status == 200) {
        const data = await response.json();
        auth.login(data.access, data.refresh, data.subscriptions);
        navigate("/subscriptions");
      }
    } catch (error) {}
  }

  if (auth.isLoggedIn) {
    return <Navigate replace to="/subscriptions"></Navigate>;
  }

  return (
    <div className="flex w-full">
      <div className="flex w-[0%] lg:w-[50%]">
        <img src="" alt="img" />
      </div>

      <div className="flex w-[100%] lg:w-[50%] items-center bg-white">
        <div className="flex flex-col flex-nowrap mx-auto w-[55%]">
          <div className="font-600 font-black mb-3 text-3xl text-center text-black font-serif antialiased">
            LOGIN
          </div>
          <form className="flex flex-auto flex-col items-center">
            <Input
              changeHandler={emailHandler}
              placeholder="Your Email"
              type="email"
            />
            <Input
              changeHandler={passwordHandler}
              placeholder="Your Password"
              type="password"
            />
            <div className="flex m-2 flex-row-reverse w-full">
              <Link
                tailwindTextColor="text-black"
                tailwindTextSize="text-xs"
                link="/"
              >
                Forgot password?
              </Link>
            </div>

            <div className="flex m-2 w-[100%] justify-center">
              <Button handler={logIn}>Log in</Button>
            </div>
            <div className="flex mt-[20px] w-[100%] justify-center gap-2 text-gray-500 text-xs">
              Don't have an account?
              <Link
                tailwindTextColor="text-black"
                tailwindTextSize="text-xs"
                link="/"
              >
                Create one now
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
