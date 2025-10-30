import { Socials } from "~/views/footer/socials";
import CollapseContainer from "~/views/components/landing/collapseContainer";

import { SubscriptionCard } from "~/views/components/landing/subscriptionCard";

import NinjaIcon from "~/views/footer/ninjaIcon";

export default function Landing() {
  return (
    <div className="flex flex-col">
      <div className="flex flex-wrap justify-between mt-5 pl-[40px] pr-[40px]">
        <SubscriptionCard
          discount={null}
          price={19.99}
          billing="Billed at $19.00 / 1 month"
          perks={[
            "Unlimited training program",
            "Meal plans",
            "Fitness community access",
            "Progress tracking",
            "Video guidance",
            "Supplement and recovery guides",
            "Abs and core routines",
            "Supplement and vitamin tips",
          ]}
        />
        <SubscriptionCard
          discount={34}
          price={19.99}
          billing="Billed at $19.00 / 1 month"
          perks={[
            "Unlimited training program",
            "Meal plans",
            "Fitness community access",
            "Progress tracking",
            "Video guidance",
            "Supplement and recovery guides",
            "Abs and core routines",
            "Supplement and vitamin tips",
          ]}
        />
        <SubscriptionCard
          discount={46}
          price={19.99}
          billing="Billed at $19.00 / 1 month"
          perks={[
            "Unlimited training program",
            "Meal plans",
            "Fitness community access",
            "Progress tracking",
            "Video guidance",
            "Supplement and recovery guides",
            "Abs and core routines",
            "Supplement and vitamin tips",
          ]}
        />
      </div>

      <div className="text-center">
        <h2>FAQ's</h2>
      </div>

      <div className="flex flex-col md:flex-row flex-wrap pl-[40px] pr-[40px]">
        <CollapseContainer title="Question One" content="Answer One" id={1} />
        <CollapseContainer title="Question Two" content="Answer Two" id={2} />
        <CollapseContainer title="Question Two" content="Answer Two" id={3} />
        <CollapseContainer title="Question Two" content="Answer Two" id={4} />
        <CollapseContainer title="Question Two" content="Answer Two" id={5} />
        <CollapseContainer title="Question Two" content="Answer Two" id={6} />
        <CollapseContainer title="Question Two" content="Answer Two" id={7} />
        <CollapseContainer title="Question Two" content="Answer Two" id={8} />
        <CollapseContainer title="Question Two" content="Answer Two" id={9} />
        <CollapseContainer title="Question Two" content="Answer Two" id={10} />
      </div>
      <footer className="pt-10">
        <div className="flex justify-center">
          <div className="flex flex-col justify-center align-center items-center relative container bg-[url(/public/dark-yellow.jpg)] rounded-4xl p-[30px]">
            <div className="text-5xl flex flex-col flex-nowrap text-black font-semibold">
              <span className="flex flex-nowrap">BEGIN YOUR</span>
              <span className="inline-block">
                <img
                  src="/public/smile-face.png"
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
                <span>© 2022-2025 Your Corporation.</span>
                ALL RIGHTS RESERVED
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
