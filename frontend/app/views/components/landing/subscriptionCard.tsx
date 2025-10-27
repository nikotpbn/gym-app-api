import ThunderIcon from "./thunderIcon";

export function SubscriptionCard(props: {
  price: number;
  billing: string;
  perks: string[];
  discount: number | null;
}) {
  return (
    <div className="relative flex-1 p-2 m-5 bg-white text-black rounded-lg min-w-[250px]">
      <div className="flex flex-row justify-between mb-5">
        <span className="bg-black text-white p-[5px] rounded-lg text-[7px]">
          MOMENTUM
        </span>
        <span className="text-[7px]">1-MONTH</span>
      </div>
      {props.discount ? (
        <span className="flex justify-center items-center absolute top-15 left-45 bg-[url(/public/sale-bg-black.png)] bg-contain bg-no-repeat text-white w-[36px] h-[36px]">
          <p className="text-md font-karantina">-{props.discount}%</p>
        </span>
      ) : null}
      <div className="text-5xl font-bold font-karantina">${props.price}/MO</div>
      <p className="text-gray-500 text-xs">{props.billing}</p>
      <button className="rounded-lg mt-5 mb-5 group transition-all ease-in-out duration-1000 flex justify-center bg-yellow-500 w-[70%] items-center p-2 hover:flex">
        <div className="flex-1 text-nowrap max-w-fit font-semibold text-xs mr-2">
          Get Started
        </div>
        <div className="flex-1 justify-end transition-all ease-in-out duration-1000 group-hover:flex-0 group-hover:text-white">
          <ThunderIcon className="stroke-black stroke-1 h-3 justify-self-end text-white transition-all ease-in-out duration-1000 group-hover:fill-black" />
        </div>
      </button>
      <hr className="border-0 bg-gray-200 h-px" />
      <div className="width-[33%] p-[10px] bg-white text-black b-rounded-lg">
        <div className="flex flex-col gap-1 mb-2">
          {props.perks.map((perk) => (
            <label className="text-xs font-semibold">
              <input
                className="accent-black mr-2 w-[5%]"
                type="checkbox"
                checked
              />
              {perk}
            </label>
          ))}
        </div>
      </div>
    </div>
  );
}
