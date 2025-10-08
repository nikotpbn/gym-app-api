import { Input } from "../components/input";
import { Button } from "../components/button";
import { Link } from "../components/link";

export function Login() {
  return (
    <div className="flex-auto flex-col content-center h-full">
      <div className="container flex flex-col flex-nowrap mx-auto max-w-sm bg-white rounded-md py-[46px] px-[26px]">
        <div className="font-600 font-black mb-[30px] text-24 text-center text-black font-serif antialiased">
          Log In To Your Account
        </div>
        <form className="flex flex-auto flex-col items-center">
          <Input label="Email" placeholder="Enter your email" type="email" />
          <Input
            label="Password"
            placeholder="Enter your Password"
            type="password"
          />
          <div className="flex mt-[20px] w-[100%] justify-center">
            <Button>Log in</Button>
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
