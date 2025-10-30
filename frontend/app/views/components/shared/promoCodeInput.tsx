import { useState, useEffect } from "react";

export function PromoCodeInput(props: { placeholder: string; name: string }) {
  const [promoCode, setPromoCode] = useState<string>();

  useEffect(() => {
    const timer = setTimeout(() => {
      if (promoCode != null && promoCode != "") {
        console.log(`send fetch to check the promo code ${promoCode}`);
      }
    }, 2000);

    return () => clearTimeout(timer);
  }, [promoCode]);

  function changeHandler(event: React.ChangeEvent<HTMLInputElement>) {
    setPromoCode(event.currentTarget.value);
  }

  return (
    <input
      className="w-full text-black text-sm border-1 border-black-300 rounded-md mb-[4px] opacity-[.6] px-[10px] h-[42px] outline-hidden antialiased"
      type="text"
      placeholder={props.placeholder}
      name={props.name}
      onChange={changeHandler}
    />
  );
}
