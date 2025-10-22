import { Socials } from "~/views/footer/socials";

import SmileFace from "./public/smile-face.png";
import NinjaIcon from "~/views/footer/ninjaIcon";

export default function Landing() {
  return (
    <>
      <footer>
        <div className="flex justify-center">
          <div className="flex flex-col justify-center align-center items-center relative container bg-[url(/public/dark-yellow.jpg)] rounded-4xl p-[30px]">
            <div className="text-5xl flex flex-col flex-nowrap text-black font-semibold">
              <span className="flex flex-nowrap">BEGIN YOUR</span>
              <span className="inline-block">
                <img
                  src={SmileFace}
                  alt="Smile Face"
                  className="float-right animate-[spin_5s_linear_infinite] h-36 w-36"
                />
                JOURNEY
                <br />
                WITH ME
              </span>
            </div>

            <Socials />
            <div className="text-black">
              <div className="flex flex-col items-center text-center mt-4">
                <span className="font-semibold">Support email:</span>
                youremail@company.org
                <div className="text-black font-semibold">
                  Privacy Policy: Terms of Conditions
                </div>
                <div>Created by BitNinja</div>
                <NinjaIcon />
                <span>© 2022-2025 Vladimir Shmondenko.</span>
                ALL RIGHTS RESERVED
              </div>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
}
