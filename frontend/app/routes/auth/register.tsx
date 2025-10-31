import type { Route } from "./+types/auth/register";

import { useState } from "react";
import { useNavigate } from "react-router";

import { Input } from "~/views/components/login/input";
import { PromoCodeInput } from "~/views/components/shared/promoCodeInput";
import { Button } from "~/views/components/login/button";
import { Link } from "~/views/components/login/link";

export function meta({}: Route.MetaArgs) {
  return [{ title: "Register" }];
}

export default function Login() {
  let navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [promotionCode, setpromotionCode] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  function emailHandler(value: string) {
    setEmail(value);
  }
  function passwordHandler(value: string) {
    setPassword(value);
  }
  function passwordConfirmHandler(value: string) {
    setPassword2(value);
  }
  function firstNameHandler(value: string) {
    setFirstName(value);
  }
  function lastNameHandler(value: string) {
    setLastName(value);
  }

  async function registerHandler() {
    if (password != password2) {
      const passwordInputs = document.querySelectorAll(".password-validator");
      passwordInputs.forEach((input) => {
        input.classList.add("border-red-500");
      });
    } else {
      try {
        let full_name = `${firstName} ${lastName}`;
        const response = await fetch("http://localhost:8000/api/v1/register/", {
          method: "POST",
          body: JSON.stringify({ full_name, email, password, password2 }),
          headers: { "Content-Type": "application/json" },
        });

        if (response.status === 200) {
          const data = await response.json();
          console.log(data.message);
          // data contains a success message, maybe use on a toast
          navigate("/login");
        }
      } catch (error) {
        console.log(error)
      }
    }
  }

  return (
    <div className="text-black flex flex-col w-full md:flex-row">
      <div className="flex w-[100%] md:w-[60%] h-full bg-yellow-500 items-center justify-center">
        <div className="flex flex-col align-center w-full p-12">
          <p>logo sgv</p>

          <div className="flex flex-row flex-no-wrap justify-between text-xs">
            <button
              className="flex items-center cursor-pointer"
              onClick={() => navigate(-1)}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 -960 960 960"
                width="24px"
                fill="#000000"
              >
                <path d="M560-280 360-480l200-200v400Z" />
              </svg>
              Back
            </button>
            <div className="flex gap-1 items-center">
              already have an account?
              <Link
                tailwindTextColor="text-black"
                tailwindTextSize="text-md"
                link="/"
              >
                sign in
              </Link>
            </div>
          </div>

          <div className="flex flex-no-wrap gap-2 mt-4 mb-4">
            <span className="bg-black rounded-md p-1 text-xs text-white">
              01
            </span>
            <span>Personal Data</span>
          </div>

          <form>
            <div className="flex gap-1">
              <Input
                changeHandler={firstNameHandler}
                extraClasses={"w-[50%]"}
                placeholder="First Name"
                type="text"
                name="first_name"
                id="first_name"
              />
              <Input
                changeHandler={lastNameHandler}
                extraClasses={"w-[50%]"}
                placeholder="Last Name"
                type="text"
                name="last_name"
                id="last_name"
              />
            </div>

            <Input
              changeHandler={emailHandler}
              extraClasses={"email-validator"}
              placeholder="Your Email"
              type="email"
              name="email"
              id="email"
            />

            <div className="flex gap-1">
              <Input
                changeHandler={passwordHandler}
                extraClasses={"password-validator w-[50%]"}
                placeholder="Your Password"
                type="password"
                name="password"
                id="passwword"
              />
              <Input
                changeHandler={passwordConfirmHandler}
                extraClasses={"password-validator w-[50%]"}
                placeholder="Password Confirmation"
                type="password"
                name="password2"
                id="passwor-confirm"
              />
            </div>
          </form>

          <div className="flex flex-no-wrap gap-2 mt-4 mb-4">
            <span className="bg-black rounded-md p-1 text-xs text-white">
              02
            </span>
            <span>Choose Your Plan</span>
          </div>
          <div>plan selector</div>

          <div className="flex w-full mt-5 mb-3">
            <PromoCodeInput placeholder="PROMO CODE" name="promocode" />
          </div>

          <div>
            <label className="text-xs">
              <input
                className="accent-black mr-2 w-[5%]"
                type="checkbox"
                checked
              />
              I agree to the&nbsp;
              <Link
                tailwindTextColor="font-semibold"
                tailwindTextSize="text-xs"
                link="/"
              >
                Privacy Policy
              </Link>
              &nbsp;and&nbsp;
              <a href="" className="font-semibold">
                Terms of Service
              </a>
            </label>
          </div>

          <div className="text-white font-semibold mt-2 mb-3">
            <Button handler={registerHandler}>JOIN NOW</Button>
          </div>

          <div className="flex gap-3 mt-2">
            <Link
              tailwindTextColor="text-gray-500"
              tailwindTextSize="text-[10px]"
              link="/"
            >
              Terms of Use
            </Link>
            <Link
              tailwindTextColor="text-gray-500"
              tailwindTextSize="text-[10px]"
              link="/"
            >
              Privacy policy (US)
            </Link>
            <Link
              tailwindTextColor="text-gray-500"
              tailwindTextSize="text-[10px]"
              link="/"
            >
              Privacy policy (EU)
            </Link>
          </div>
        </div>
      </div>

      <div className="flex w-[100%] md:w-[40%] h-full bg-red-500"></div>
    </div>
  );
}
