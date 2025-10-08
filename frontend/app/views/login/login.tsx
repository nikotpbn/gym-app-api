import { Input } from "../components/input";

export function Login() {
  return (
    <div className="flex-auto flex-col content-center align-center h-full">
      <div className="container flex flex-col flex-nowrap mx-auto max-w-sm bg-white rounded-md py-[46px] px-[26px]">
        <div className="font-600 font-black mb-[30px] text-24 text-center text-black font-serif antialiased">
          Log In To Your Account
        </div>
        <form>
          <Input label="Email" placeholder="Enter your email" type="email" />
          <Input
            label="Password"
            placeholder="Enter your Password"
            type="password"
          />
        </form>
      </div>
    </div>
  );
}
