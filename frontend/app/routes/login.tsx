import { useState, useContext } from "react";
import type { Route } from "./+types/login";

import { Input } from "~/views/components/input";
import { Button } from "~/views/components/button";
import { Link } from "~/views/components/link";

import { AuthContext } from "~/context";
import { useNavigate } from "react-router";

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
        console.log(data);
        auth.login(data.access, data.refresh, data.subscriptions);
        navigate("/gympro");
      }
    } catch (error) {}
  }

  return (
    <div className="flex-auto flex-col content-center h-full">
      <div className="container flex flex-col flex-nowrap mx-auto max-w-sm bg-white rounded-md py-[46px] px-[26px]">
        <div className="font-600 font-black mb-[30px] text-24 text-center text-black font-serif antialiased">
          Log In To Your Account
        </div>
        <form className="flex flex-auto flex-col items-center">
          <Input
            handler={emailHandler}
            label="Email"
            placeholder="Enter your email"
            type="email"
          />
          <Input
            handler={passwordHandler}
            label="Password"
            placeholder="Enter your Password"
            type="password"
          />
          <div className="flex mt-[20px] w-[100%] justify-center">
            <Button handler={logIn}>Log in</Button>
          </div>
          <div className="flex mt-[20px] w-[100%] justify-around">
            <Link link="/">Create an account</Link>
            <Link link="/">Forgot password?</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
