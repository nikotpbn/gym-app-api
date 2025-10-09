import { useState } from "react";

import { Input } from "../components/input";
import { Button } from "../components/button";
import { Link } from "../components/link";

export function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function emailHandler(value: string) {
    setEmail(value);
  }

  function passwordHandler(value: string) {
    setPassword(value);
  }

  async function logIn() {
    let body = new FormData();
    body.append("email", email);
    body.append("password", password);

    console.log(password);

    try {
      const response = await fetch("http://localhost:8000/api/v1/token/", {
        method: "POST",
        body: body,
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      console.log(data);
      console.log(response.status);
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
